

class OrderListener:
    """
    This class is called after we catch the hotword that have woke up JARVIS.
    We now wait for an order spoken out loud by the user, translate the order into a text and run the action
     attached to this order from settings
    """
    def __init__(self):
        pass