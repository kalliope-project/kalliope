from core.ConfigurationManager import SettingLoader
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from core.TriggerLauncher import TriggerLauncher

from neurons import Say


class MainController:
    def __init__(self, brain_file=None):
        self.brain_file = brain_file
        # get global configuration
        self.settings = SettingLoader.get_settings()

        # create an order listener object
        self.order_listener = OrderListener(self.analyse_order)
        # Wait that the jarvis trigger is pronounced by the user
        self.trigger_instance = self._get_default_trigger()
        self.trigger_instance.start()

    def callback(self):
        """
        # we have detected the hotword, we can now pause the Jarvis Trigger for a while
        # The user can speak out loud his order during this time.
        :return:
        """
        # pause the snowboy process
        self.trigger_instance.pause()
        Say(message=self.settings.random_wake_up_answers)
        self.order_listener.load_stt_plugin()

    def analyse_order(self, order):
        """
        Receive an order, try to retreive it in the brain.yml to launch to attached plugins
        :return:
        """
        order_analyser = OrderAnalyser(order, main_controller=self, brain_file=self.brain_file)
        order_analyser.start()
        # restart the trigger when the order analyser has finish his job
        self.trigger_instance.unpause()

    def _get_default_trigger(self):
        """
        Return an instance of the default trigger
        :return:
        """
        for trigger in self.settings.triggers:
            if trigger.name == self.settings.default_trigger_name:
                return TriggerLauncher.get_trigger(trigger, callback=self.callback)
