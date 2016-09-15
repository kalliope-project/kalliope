from neurons import Say


class OrderListener:
    """
    This class is called after we catch the hotword that have woke up JARVIS.
    We now wait for an order spoken out loud by the user, translate the order into a text and run the action
     attached to this order from settings
    """
    def __init__(self, main_controller):
        """

        :param main_controller:
        :type main_controller: MainController
        """
        self.main_controller = main_controller

    def hotword_detected(self):
        # we have detected the hotword, we can now pause the Jarvis Trigger for a while
        # The user can speak out loud his order during this time.
        self.main_controller.pause_jarvis_trigger()
        print "Start listening for order"
        Say("oui monsieur?")
