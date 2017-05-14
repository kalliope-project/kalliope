from threading import Thread

try:
    # only import if we are on a Rpi
    import RPi.GPIO as GPIO
except RuntimeError:
    pass
import time

import logging

from kalliope.core.Models.RpiSettings import RpiSettings

logging.basicConfig()
logger = logging.getLogger("kalliope")


class RpiUtils(Thread):

    def __init__(self, rpi_settings=None, callback=None):
        """
        
        :param rpi_settings: Settings object with GPIO pin number to use
        :type rpi_settings: RpiSettings
        :param callback: Callback function from the main controller to call when the mute button is pressed
        """
        super(RpiUtils, self).__init__()
        GPIO.setmode(GPIO.BCM)  # Use GPIO name
        GPIO.setwarnings(False)
        self.rpi_settings = rpi_settings
        self.callback = callback
        self.init_gpio(self.rpi_settings)

    def run(self):
        # run the main thread
        try:
            while True:  # keep the thread alive
                time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            self.destroy()
        self.destroy()

    def switch_kalliope_mute_led(self, event):
        """
        Switch the state of the MUTE LED
        :param event: 
        :return: 
        """
        logger.debug("[RpiUtils] Event button caught. Switching mute led")
        # get led status
        led_mute_kalliope = GPIO.input(self.rpi_settings.pin_led_muted)
        # switch state
        if led_mute_kalliope == GPIO.HIGH:
            logger.debug("[RpiUtils] Switching pin_led_muted to OFF")
            self.switch_pin_to_off(self.rpi_settings.pin_led_muted)
            self.callback(muted=False)
        else:
            logger.debug("[RpiUtils] Switching pin_led_muted to ON")
            self.switch_pin_to_on(self.rpi_settings.pin_led_muted)
            self.callback(muted=True)

    def destroy(self):
        logger.debug("[RpiUtils] Cleanup GPIO configuration")
        GPIO.cleanup()

    def init_gpio(self, rpi_settings):
        # All led are off by default
        if self.rpi_settings.pin_led_muted:
            GPIO.setup(rpi_settings.pin_led_muted, GPIO.OUT, initial=GPIO.LOW)
        if self.rpi_settings.pin_led_started:
            GPIO.setup(rpi_settings.pin_led_started, GPIO.OUT, initial=GPIO.LOW)
        if self.rpi_settings.pin_led_listening:
            GPIO.setup(rpi_settings.pin_led_listening, GPIO.OUT, initial=GPIO.LOW)
        if self.rpi_settings.pin_led_talking:
            GPIO.setup(rpi_settings.pin_led_talking, GPIO.OUT, initial=GPIO.LOW)

        # MUTE button
        GPIO.setup(rpi_settings.pin_mute_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(rpi_settings.pin_mute_button, GPIO.FALLING,
                              callback=self.switch_kalliope_mute_led,
                              bouncetime=500)

    @classmethod
    def switch_pin_to_on(cls, pin_number):
        logger.debug("[RpiUtils] Switching pin number %s to ON" % pin_number)
        GPIO.output(pin_number, GPIO.HIGH)

    @classmethod
    def switch_pin_to_off(cls, pin_number):
        logger.debug("[RpiUtils] Switching pin number %s to OFF" % pin_number)
        GPIO.output(pin_number, GPIO.LOW)
