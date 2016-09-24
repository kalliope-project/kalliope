import logging
from core import ConfigurationManager


class DefaultSpeechToTextNotFound(Exception):
    pass


class DefaultSpeechNull(Exception):
    pass


class NoSpeechToTextConfiguration(Exception):
    pass


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
        default_stt_plugin = self._get_stt_plugins()

        stt_args = self._get_stt_args(default_stt_plugin)

        # capitalizes the first letter (because classes have first letter upper case)
        default_stt_plugin = default_stt_plugin.capitalize()
        self._run_stt_plugin(default_stt_plugin, stt_args)

    def _get_stt_plugins(self):
        try:
            default_speech_to_text = self.settings["default_speech_to_text"]
            if default_speech_to_text is None:
                raise DefaultSpeechNull("Attribute default_speech_to_text is null")
            logging.info("Default STT: %s" % default_speech_to_text)
            return default_speech_to_text
        except KeyError:
            raise DefaultSpeechToTextNotFound("Attribute default_speech_to_text not found in settings")

    def _get_stt_args(self, default_stt_plugin_name):
        """
        Return argument set for the current STT engine
        :param default_stt_plugin: Name of the STT engine
        :return:
        """
        def find(lst, key):
            """
            Find a key name in a list
            :param lst: list()
            :param key: key name to find i the list
            :return: Return the dict
            """
            for el in lst:
                try:
                    if el[key]:
                        return el[key]
                except TypeError:
                    pass
                except KeyError:
                    pass
            return None

        try:
            speechs_to_text = self.settings["speech_to_text"]
        except KeyError:
            raise NoSpeechToTextConfiguration("No speech_to_text in settings")

        logging.debug("Settings file content: %s" % speechs_to_text)
        # get args
        args = find(speechs_to_text, default_stt_plugin_name)

        logging.debug("Args for %s STT: %s" % (default_stt_plugin_name, args))

        return args

    def _run_stt_plugin(self, stt_plugin, parameters=None):
        """
        Dynamic loading of a STT module
        :param plugin: Module name to load
        :param parameters: Parameter of the module
        :return:
        """
        print "Running STT %s with parameter %s" % (stt_plugin, parameters)
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


