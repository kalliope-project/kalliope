import logging
import os
import random

from flask import Flask

from kalliope.core import Utils
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.OrderAnalyser import OrderAnalyser
from kalliope.core.OrderListener import OrderListener
from kalliope.core.Players import Mplayer
from kalliope.core.RestAPI.FlaskAPI import FlaskAPI
from kalliope.core.TriggerLauncher import TriggerLauncher
from kalliope.neurons.say.say import Say

logging.basicConfig()
logger = logging.getLogger("kalliope")


class MainController:
    """
    This Class is the global controller of the application.
    """
    def __init__(self, brain=None):
        self.brain = brain
        # get global configuration
        sl = SettingLoader()
        self.settings = sl.settings

        # run the api if the user want it
        if self.settings.rest_api.active:
            Utils.print_info("Starting REST API Listening port: %s" % self.settings.rest_api.port)
            app = Flask(__name__)
            flask_api = FlaskAPI(app, port=self.settings.rest_api.port, brain=self.brain)
            flask_api.daemon = True
            flask_api.start()

        # create an order listener object. This last will the trigger callback before starting
        self.order_listener = OrderListener(self.analyse_order)
        # Wait that the kalliope trigger is pronounced by the user
        self.trigger_instance = self._get_default_trigger()
        self.trigger_instance.start()
        Utils.print_info("Waiting for trigger detection")

    def callback(self):
        """
        we have detected the hotword, we can now pause the Trigger for a while
        The user can speak out loud his order during this time.
        """
        # pause the trigger process
        self.trigger_instance.pause()
        # start listening for an order
        self.order_listener.start()
        # if random wake answer sentence are present, we play this
        if self.settings.random_wake_up_answers is not None:
            Say(message=self.settings.random_wake_up_answers)
        else:
            random_sound_to_play = self._get_random_sound(self.settings.random_wake_up_sounds)
            Mplayer.play(random_sound_to_play)

    def analyse_order(self, order):
        """
        Receive an order, try to retrieve it in the brain.yml to launch to attached plugins
        :param order: the sentence received
        :type order: str
        """
        if order is not None:   # maybe we have received a null audio from STT engine
            order_analyser = OrderAnalyser(order, brain=self.brain)
            order_analyser.start()

        # restart the trigger when the order analyser has finish his job
        Utils.print_info("Waiting for trigger detection")
        self.trigger_instance.unpause()
        # create a new order listener that will wait for start
        self.order_listener = OrderListener(self.analyse_order)

    def _get_default_trigger(self):
        """
        Return an instance of the default trigger
        :return: Trigger
        """
        for trigger in self.settings.triggers:
            if trigger.name == self.settings.default_trigger_name:
                return TriggerLauncher.get_trigger(trigger, callback=self.callback)

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
        logger.debug("Selected sound: %s" % random_path)
        return Utils.get_real_file_path(random_path)
