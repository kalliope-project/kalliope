
class OrderListener:

    def __init__(self, main_controller):
        """
        This class is called after we catch the hotword that have woke up JARVIS.
        We now wait for an order spoken out loud by the user, translate the order into a text and run the action
         attached to this order from settings
        :param main_controller:
        :type main_controller: MainController
        """
        self.main_controller = main_controller

    def start(self):
        """
        Start recording the microphone
        :return:
        """
        pass