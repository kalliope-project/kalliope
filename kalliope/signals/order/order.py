import logging
import random
from threading import Thread
from time import sleep

from kalliope.core.Utils.RpiUtils import RpiUtils

from kalliope.core.SynapseLauncher import SynapseLauncher

from kalliope.core.OrderListener import OrderListener

from kalliope import Utils, BrainLoader
from kalliope.neurons.say import Say

from kalliope.core.TriggerLauncher import TriggerLauncher
from transitions import Machine

from kalliope.core.PlayerLauncher import PlayerLauncher

from kalliope.core.ConfigurationManager import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Order(Thread):
    states = ['init',
              'starting_trigger',
              'playing_ready_sound',
              'waiting_for_trigger_callback',
              'stopping_trigger',
              'playing_wake_up_answer',
              'start_order_listener',
              'waiting_for_order_listener_callback',
              'analysing_order']

    def __init__(self):
        super(Order, self).__init__()
        Utils.print_info('Starting voice order manager')
        # load settings and brain from singleton
        sl = SettingLoader()
        self.settings = sl.settings
        self.brain = BrainLoader().get_brain()

        # keep in memory the order to process
        self.order_to_process = None

        # get the player instance
        self.player_instance = PlayerLauncher.get_player(settings=self.settings)

        # save an instance of the trigger
        self.trigger_instance = None
        self.trigger_callback_called = False
        self.is_trigger_muted = False

        # If kalliope is asked to start muted
        #self.set_mute_status(self.settings.start_muted)
        if self.settings.start_options['muted'] is True:
            self.is_trigger_muted = True

        # save the current order listener
        self.order_listener = None
        self.order_listener_callback_called = False

        # boolean used to know id we played the on ready notification at least one time
        self.on_ready_notification_played_once = False

        # rpi setting for led and mute button
        self.init_rpi_utils()

        # Initialize the state machine
        self.machine = Machine(model=self, states=Order.states, initial='init', queued=True)

        # define transitions
        self.machine.add_transition('start_trigger', ['init', 'analysing_order'], 'starting_trigger')
        self.machine.add_transition('play_ready_sound', 'starting_trigger', 'playing_ready_sound')
        self.machine.add_transition('wait_trigger_callback', 'playing_ready_sound', 'waiting_for_trigger_callback')
        self.machine.add_transition('stop_trigger', 'waiting_for_trigger_callback', 'stopping_trigger')
        self.machine.add_transition('play_wake_up_answer', 'stopping_trigger', 'playing_wake_up_answer')
        self.machine.add_transition('wait_for_order', 'playing_wake_up_answer', 'waiting_for_order_listener_callback')
        self.machine.add_transition('analyse_order', 'playing_wake_up_answer', 'analysing_order')

        self.machine.add_ordered_transitions()

        # add method which are called when changing state
        self.machine.on_enter_starting_trigger('start_trigger_process')
        self.machine.on_enter_playing_ready_sound('play_ready_sound_process')
        self.machine.on_enter_waiting_for_trigger_callback('waiting_for_trigger_callback_thread')
        self.machine.on_enter_playing_wake_up_answer('play_wake_up_answer_thread')
        self.machine.on_enter_stopping_trigger('stop_trigger_process')
        self.machine.on_enter_start_order_listener('start_order_listener_thread')
        self.machine.on_enter_waiting_for_order_listener_callback('waiting_for_order_listener_callback_thread')
        self.machine.on_enter_analysing_order('analysing_order_thread')

    def run(self):
        self.start_trigger()

    def start_trigger_process(self):
        """
        This function will start the trigger thread that listen for the hotword
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        self.trigger_instance = TriggerLauncher.get_trigger(settings=self.settings, callback=self.trigger_callback)
        self.trigger_callback_called = False
        self.trigger_instance.daemon = True
        # Wait that the kalliope trigger is pronounced by the user
        self.trigger_instance.start()
        self.next_state()

    def play_ready_sound_process(self):
        """
        Play a sound when Kalliope is ready to be awaken at the first start
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        if (not self.on_ready_notification_played_once and self.settings.play_on_ready_notification == "once") or \
                        self.settings.play_on_ready_notification == "always":
            # we remember that we played the notification one time
            self.on_ready_notification_played_once = True
            # here we tell the user that we are listening
            if self.settings.on_ready_answers is not None:
                Say(message=self.settings.on_ready_answers)
            elif self.settings.on_ready_sounds is not None:
                random_sound_to_play = self._get_random_sound(self.settings.on_ready_sounds)
                self.player_instance.play(random_sound_to_play)
        self.next_state()

    def waiting_for_trigger_callback_thread(self):
        """
        Method to print in debug that the main process is waiting for a trigger detection
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        if self.is_trigger_muted:  # the user asked to mute inside the mute neuron
            Utils.print_info("Kalliope is muted")
            self.trigger_instance.pause()
        else:
            Utils.print_info("Waiting for trigger detection")
        # this loop is used to keep the main thread alive
        while not self.trigger_callback_called:
            sleep(0.1)
        self.next_state()

    def waiting_for_order_listener_callback_thread(self):
        """
        Method to print in debug that the main process is waiting for an order to analyse
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        # this loop is used to keep the main thread alive
        while not self.order_listener_callback_called:
            sleep(0.1)
        if self.settings.rpi_settings:
            if self.settings.rpi_settings.pin_led_listening:
                RpiUtils.switch_pin_to_off(self.settings.rpi_settings.pin_led_listening)
        self.next_state()

    def trigger_callback(self):
        """
        we have detected the hotword, we can now pause the Trigger for a while
        The user can speak out loud his order during this time.
        """
        logger.debug("[MainController] Trigger callback called, switching to the next state")
        self.trigger_callback_called = True

    def stop_trigger_process(self):
        """
        The trigger has been awaken, we don't needed it anymore
        :return:
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        self.trigger_instance.stop()
        self.next_state()

    def start_order_listener_thread(self):
        """
        Start the STT engine thread
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        # start listening for an order
        self.order_listener_callback_called = False
        self.order_listener = OrderListener(callback=self.order_listener_callback)
        self.order_listener.daemon = True
        self.order_listener.start()
        self.next_state()

    def play_wake_up_answer_thread(self):
        """
        Play a sound or make Kalliope say something to notify the user that she has been awaken and now
        waiting for order
        """
        logger.debug("[MainController] Entering state: %s" % self.state)
        # if random wake answer sentence are present, we play this
        if self.settings.random_wake_up_answers is not None:
            Say(message=self.settings.random_wake_up_answers)
        else:
            random_sound_to_play = self._get_random_sound(self.settings.random_wake_up_sounds)
            self.player_instance.play(random_sound_to_play)
        self.next_state()

    def order_listener_callback(self, order):
        """
        Receive an order, try to retrieve it in the brain.yml to launch to attached plugins
        :param order: the sentence received
        :type order: str
        """
        logger.debug("[MainController] Order listener callback called. Order to process: %s" % order)
        self.order_to_process = order
        self.order_listener_callback_called = True

    def analysing_order_thread(self):
        """
        Start the order analyser with the caught order to process
        """
        logger.debug("[MainController] order in analysing_order_thread %s" % self.order_to_process)
        SynapseLauncher.run_matching_synapse_from_order(self.order_to_process,
                                                        self.brain,
                                                        self.settings,
                                                        is_api_call=False)

        # return to the state "unpausing_trigger"
        self.start_trigger()

    @staticmethod
    def _get_random_sound(random_wake_up_sounds):
        """
        Return a path of a sound to play
        If the path is absolute, test if file exist
        If the path is relative, we check if the file exist in the sound folder
        :param random_wake_up_sounds: List of wake_up sounds
        :return: path of a sound to play
        """
        # take first randomly a path
        random_path = random.choice(random_wake_up_sounds)
        logger.debug("[MainController] Selected sound: %s" % random_path)
        return Utils.get_real_file_path(random_path)

    def set_mute_status(self, muted=False):
        """
        Define is the trigger is listening or not
        :param muted: Boolean. If true, kalliope is muted
        """
        logger.debug("[MainController] Mute button pressed. Switch trigger process to muted: %s" % muted)
        if muted:
            self.trigger_instance.pause()
            self.is_trigger_muted = True
            Utils.print_info("Kalliope now muted")
        else:
            self.trigger_instance.unpause()
            self.is_trigger_muted = False
            Utils.print_info("Kalliope now listening for trigger detection")

    def get_mute_status(self):
        """
        return the current state of the trigger (muted or not)
        :return: Boolean
        """
        return self.is_trigger_muted

    def init_rpi_utils(self):
        """
        Start listening on GPIO if defined in settings
        """
        if self.settings.rpi_settings:
            # the user set GPIO pin, we need to instantiate the RpiUtils class in order to setup GPIO
            rpi_utils = RpiUtils(self.settings.rpi_settings, self.set_mute_status)
            if self.settings.rpi_settings.pin_mute_button:
                # start the listening for button pressed thread only if the user set a pin
                rpi_utils.daemon = True
                rpi_utils.start()
        # switch high the start led, as kalliope is started. Only if the setting exist
        if self.settings.rpi_settings:
            if self.settings.rpi_settings.pin_led_started:
                logger.debug("[MainController] Switching pin_led_started to ON")
                RpiUtils.switch_pin_to_on(self.settings.rpi_settings.pin_led_started)
