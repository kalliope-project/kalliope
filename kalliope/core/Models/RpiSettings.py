

class RpiSettings(object):

    def __init__(self, pin_mute_button=None, pin_led_started=None, pin_led_muted=None,
                 pin_led_talking=None, pin_led_listening=None):
        self.pin_mute_button = pin_mute_button
        self.pin_led_started = pin_led_started
        self.pin_led_muted = pin_led_muted
        self.pin_led_talking = pin_led_talking
        self.pin_led_listening = pin_led_listening

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        """
        This method allows to serialize in a proper way this object        
        """

        return {
            'pin_mute_button': self.pin_mute_button,
            'pin_led_started': self.pin_led_started,
            'pin_led_muted': self.pin_led_muted,
            'pin_led_talking': self.pin_led_talking,
            'pin_led_listening': self.pin_led_listening,
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
