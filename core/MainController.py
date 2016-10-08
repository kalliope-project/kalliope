import logging
import os
import random

from core import AudioPlayer
from core import Utils
from core.ConfigurationManager import SettingLoader
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from core.TriggerLauncher import TriggerLauncher

from neurons import Say

logging.basicConfig()
logger = logging.getLogger("jarvis")

class MainController:
    def __init__(self, brain_file=None):
        self.brain_file = brain_file
        # get global configuration
        self.settings = SettingLoader.get_settings()

        # create an order listener object. This last will the trigger callback before starting
        self.order_listener = OrderListener(self.analyse_order)
        # Wait that the jarvis trigger is pronounced by the user
        self.trigger_instance = self._get_default_trigger()
        self.trigger_instance.start()
        Utils.print_info("Waiting for trigger detection")

    def callback(self):
        """
        # we have detected the hotword, we can now pause the Jarvis Trigger for a while
        # The user can speak out loud his order during this time.
        :return:
        """
        # pause the snowboy process
        self.trigger_instance.pause()
        # start listening for an order
        self.order_listener.start()
        # if random wake answer sentence are present, we play this
        if self.settings.random_wake_up_answers is not None:
            Say(message=self.settings.random_wake_up_answers)
        else:
            ap = AudioPlayer()
            ap.init_play()
            random_sound_to_play = self._get_random_sound(self.settings.random_wake_up_sounds)
            ap.play_audio(random_sound_to_play)

    def analyse_order(self, order):
        """
        Receive an order, try to retreive it in the brain.yml to launch to attached plugins
        :return:
        """
        order_analyser = OrderAnalyser(order, main_controller=self, brain_file=self.brain_file)
        order_analyser.start()
        # restart the trigger when the order analyser has finish his job
        Utils.print_info("Waiting for trigger detection")
        self.trigger_instance.unpause()
        # create a new order listener that will wait for start
        self.order_listener = OrderListener(self.analyse_order)
        # restart the trigger to catch the hotword
        self.trigger_instance.start()

    def _get_default_trigger(self):
        """
        Return an instance of the default trigger
        :return:
        """
        for trigger in self.settings.triggers:
            if trigger.name == self.settings.default_trigger_name:
                return TriggerLauncher.get_trigger(trigger, callback=self.callback)

    def unpause_jarvis_trigger(self):
        print "call unpause"
        self.trigger_instance.unpause()

    @staticmethod
    def _get_random_sound(random_wake_up_sounds):
        """
        Return a path of a sound to play
        If the path is absolute, test if file exist
        If the path is relative, we check if the file exist in the sound folder
        :param random_wake_up_sounds:
        :return:
        """
        # take first randomly a path
        random_path = random.choice(random_wake_up_sounds)
        logger.debug("Selected sound: %s" % random_path)
        if os.path.isabs(random_path):
            logger.debug("Path of file %s is absolute" % random_path)
            return random_path
        else:
            logger.debug("Path of file %s is relative" % random_path)
            return "sounds" + os.sep + random_path
