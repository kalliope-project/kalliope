import logging
from threading import Thread
from time import sleep

from kalliope.core.SignalModule import SignalModule
from kalliope.core.Cortex import Cortex
from kalliope.core.SynapseLauncher import SynapseLauncher

from kalliope.core.OrderListener import OrderListener

from kalliope import Utils, BrainLoader

from kalliope.core.TriggerLauncher import TriggerLauncher
from transitions import Machine

from kalliope.core.PlayerLauncher import PlayerLauncher

from kalliope.core.ConfigurationManager import SettingLoader

from kalliope.core.HookManager import HookManager

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Order(SignalModule, Thread):

    states = ['init',
              'starting_trigger',
              'unpausing_trigger',
              'waiting_for_trigger_callback',
              'pausing_trigger',
              'start_order_listener',
              'waiting_for_order_listener_callback',
              'analysing_order']

    def __init__(self):
        super(SignalModule, self).__init__()
        Thread.__init__(self, name=Order)
        Utils.print_info('Starting order signal')
        # load settings and brain from singleton
        sl = SettingLoader()
        self.settings = sl.settings
        self.brain = BrainLoader().brain

        # keep in memory the order to process
        self.order_to_process = None

        # get the player instance
        self.player_instance = PlayerLauncher.get_player(settings=self.settings)

        # save an instance of the trigger
        self.trigger_instance = None
        self.trigger_callback_called = False

        # variable from notifications
        self.skip_trigger = False       # keep the status of the trigger, if true we can skip it in the statue machine
        self.counter_max_retry = 0      # 0 means disabled

        # save the current order listener
        self.order_listener = None
        self.order_listener_callback_called = False

        # Initialize the state machine
        self.machine = Machine(model=self, states=Order.states, initial='init', queued=True)

        # define transitions
        self.machine.add_transition('start_trigger', 'init', 'starting_trigger')
        self.machine.add_transition('unpause_trigger',  'analysing_order', 'unpausing_trigger')
        self.machine.add_transition('wait_trigger_callback', 'unpausing_trigger', 'waiting_for_trigger_callback')
        self.machine.add_transition('pause_trigger', 'waiting_for_trigger_callback', 'pausing_trigger')
        self.machine.add_transition('wait_for_order', 'pausing_trigger', 'waiting_for_order_listener_callback')
        self.machine.add_transition('analyse_order', 'waiting_for_order_listener_callback', 'analysing_order')
        self.machine.add_transition('start_order_listener', 'analysing_order', 'start_order_listener')

        self.machine.add_ordered_transitions()

        # add method which are called when changing state
        self.machine.on_enter_starting_trigger('start_trigger_process')
        self.machine.on_enter_unpausing_trigger('unpausing_trigger_process')
        self.machine.on_enter_waiting_for_trigger_callback('waiting_for_trigger_callback_thread')
        self.machine.on_enter_pausing_trigger('pause_trigger_process')
        self.machine.on_enter_start_order_listener('start_order_listener_thread')
        self.machine.on_enter_waiting_for_order_listener_callback('waiting_for_order_listener_callback_thread')
        self.machine.on_enter_analysing_order('analysing_order_thread')
        
    def run(self):
        # run hook on_start
        self.start_trigger()

    def start_trigger_process(self):
        """
        This function will start the trigger thread that listen for the hotword
        """
        logger.debug("[Order] Entering state: %s" % self.state)
        self.trigger_instance = TriggerLauncher.get_trigger(settings=self.settings, callback=self.trigger_callback)
        self.trigger_callback_called = False
        self.trigger_instance.daemon = True
        # Wait that the kalliope trigger is pronounced by the user
        self.trigger_instance.start()
        HookManager.on_start()
        self.next_state()

    def unpausing_trigger_process(self):    
        """ 
        If the trigger was in pause, this method will unpause it to listen again for the hotword    
        """ 
        logger.debug("Entering state: %s" % self.state) 
        HookManager.on_waiting_for_trigger()
        self.trigger_instance.unpause()  
        self.trigger_callback_called = False    
        self.next_state()

    def waiting_for_trigger_callback_thread(self):
        """
        Method to print in debug that the main process is waiting for a trigger detection
        """
        logger.debug("[Order] Entering state: %s" % self.state)
        if self.settings.options.deaf:  # the user asked to deaf inside the deaf neuron
            Utils.print_info("Kalliope is deaf")
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
        logger.debug("[Order] Entering state: %s" % self.state)
        # this loop is used to keep the main thread alive
        while not self.order_listener_callback_called:
            sleep(0.1)
        # TODO on end listening here
        self.next_state()

    def trigger_callback(self):
        """
        we have detected the hotword, we can now pause the Trigger for a while
        The user can speak out loud his order during this time.
        """
        logger.debug("[Order] Trigger callback called, switching to the next state")
        self.trigger_callback_called = True

    def pause_trigger_process(self):
        """
        The trigger has been awaken, we pause it
        :return:
        """
        logger.debug("[Order] Entering state: %s" % self.state)
        self.trigger_instance.pause()
        # if here, then the trigger has been called and paused
        HookManager.on_triggered()
        self.next_state()

    def start_order_listener_thread(self):
        """
        Start the STT engine thread
        """
        logger.debug("[Order] Entering state: %s" % self.state)

        # start listening for an order
        self.order_listener_callback_called = False
        self.order_listener = OrderListener(callback=self.order_listener_callback)
        self.order_listener.daemon = True
        self.order_listener.start()
        self.next_state()

    def order_listener_callback(self, order):
        """
        Receive an order, try to retrieve it in the brain.yml to launch to attached plugins
        :param order: the sentence received
        :type order: str
        """
        logger.debug("[Order] Order listener callback called. Order to process: %s" % order)
        self.order_to_process = order
        self.order_listener_callback_called = True
        # save in kalliope memory the last order
        Cortex.save('kalliope_last_order', order)

    def analysing_order_thread(self):
        """
        Start the order analyser with the caught order to process
        """
        if self.order_to_process is None or self.order_to_process == "":
            logger.debug("[Order] No audio caught from analysing_order_thread")
            HookManager.on_stt_error()
        else:
            logger.debug("[Order] order in analysing_order_thread %s" % self.order_to_process)
            SynapseLauncher.run_matching_synapse_from_order(self.order_to_process,
                                                            self.brain,
                                                            self.settings,
                                                            is_api_call=False)

        if self.skip_trigger:
            self.start_order_listener()
        else:
            self.unpause_trigger()

    def on_notification_received(self, notification=None, payload=None):
        logger.debug("[Order] received notification, notification: %s, payload: %s" % (notification, payload))

        # skip_trigger: change the trigger status
        if notification == "skip_trigger":
            self.switch_trigger(payload)

        if notification == "skip_trigger_max_retry":
            self.set_counter_max_retry(payload)

        if notification == "skip_trigger_decrease_max_retry":
            self.decrease_max_retry()

    def set_counter_max_retry(self, payload):
        """
        set a 'counter_max_retry' for max retry before switching automatically the skip_trigger flag to False
        :param payload: payload that contains the max_retry counter value to set
        """
        if "max_retry" in payload:
            if payload["max_retry"] > 0:
                self.counter_max_retry = payload["max_retry"]
                logger.debug("[Order] max_retry set to %s" % self.counter_max_retry)

    def decrease_max_retry(self):
        """
        will decrease the current value of 'counter_max_retry' if the current is > 0
        If the new value == 0, then the skip_trigger flag is automatically switched to False
        """
        logger.debug("[Order] current max_retry: %s" % self.counter_max_retry)
        if self.counter_max_retry > 0:
            self.counter_max_retry = self.counter_max_retry - 1
            logger.debug("[Order] new max_retry value after decrease: %s" % self.counter_max_retry)
            if self.counter_max_retry == 0:
                logger.debug("[Order] max_retry reached '0'. Set skip_trigger to False")
                # the counter raised 0, we can stop to skip the trigger
                self.skip_trigger = False
            
        else:
            logger.debug("[Order] cannot decrease max_retry because current value is <= 0")

    def switch_trigger(self, payload):
        """
        switch the skip_trigger flag
        :param payload: payload dict that contains the new status of the skip_trigger flag
        """
        if "status" in payload:
            status = Utils.str_to_bool(payload["status"])
            if status:
                logger.debug("[Order] switch signals to True")
                self.skip_trigger = True
            else:
                logger.debug("[Order] switch signals to False")
                self.skip_trigger = False
