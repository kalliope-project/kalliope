import logging
from core import ConfigurationManager


class OrderListener:

    def __init__(self, main_controller=None):
        """
        This class is called after we catch the hotword that have woke up JARVIS.
        We now wait for an order spoken out loud by the user, translate the order into a text and run the action
         attached to this order from settings
        :param main_controller:
        :type main_controller: MainController
        """
        self.main_controller = main_controller
        # self.settings = main_controller.conf.settingLoader.get_config()
        self.settings = ConfigurationManager().get_settings()

    def load_stt_plugin(self):
        default_stt_plugin = ConfigurationManager.get_default_speech_to_text()

        stt_args = ConfigurationManager.get_stt_args(default_stt_plugin)

        # capitalizes the first letter (because classes have first letter upper case)
        default_stt_plugin = default_stt_plugin.capitalize()
        self._run_stt_plugin(default_stt_plugin, stt_args)

    def _run_stt_plugin(self, stt_plugin, parameters=None):
        """
        Dynamic loading of a STT module
        :param plugin: Module name to load
        :param parameters: Parameter of the module
        :return:
        """
        logging.debug("Running STT %s with parameter %s" % (stt_plugin, parameters))
        mod = __import__('stt', fromlist=[stt_plugin])

        klass = getattr(mod, stt_plugin)

        if klass is not None:
            # run the plugin
            if not parameters:
                klass(self.main_controller)
            elif isinstance(parameters, dict):
                klass(self.main_controller, **parameters)
            else:
                klass(self.main_controller, parameters)


