from core.JarvisTrigger import JarvisTrigger
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from core.ConfigurationManager.ConfigurationManager import ConfigurationManager

from neurons import Say


class MainController:
    def __init__(self):
        # Manage Global Configuration
        self.conf = ConfigurationManager().get_settings()

        # create an order listener object
        self.order_listener = OrderListener(self)
        # Wait that the jarvis trigger is pronounced by the user
        self.jarvis_triger = JarvisTrigger(self)

    def get_order_listenner(self):
        return self.order_listener

    def start(self):
        self.jarvis_triger.start()

    def pause_jarvis_trigger(self):
        """
        The hotwork to wake up jarvis has been detected, we pause the snowboy process
        :return:
        """
        self.jarvis_triger.pause()

    def unpause_jarvis_trigger(self):
        self.jarvis_triger.unpause()

    def hotword_detected(self):
        """
        # we have detected the hotword, we can now pause the Jarvis Trigger for a while
        # The user can speak out loud his order during this time.
        :return:
        """
        # pause the snowboy process
        self.pause_jarvis_trigger()
        print "Start listening for order"
        random_answers = self.conf["random_wake_up_answers"]
        Say(message=random_answers)
        self.order_listener.load_stt_plugin()

    def analyse_order(self, order):
        """
        Receive an order, try to retreive it in the brain.yml to launch to attached plugins
        :return:
        """
        order_analyser = OrderAnalyser(order, main_controller=self)
        order_analyser.start()

