from core.JarvisTrigger import JarvisTrigger
from core.OrderListener import OrderListener


class MainController:
    def __init__(self):
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
        pass