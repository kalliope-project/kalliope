
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
        self.settings = main_controller.conf.settingLoader.get_config()


    def _getSTTPlugin(self):
        return self.settings["speechToText"]["name"]

    def _getSTTArgs(self):
        args = None
        if 'args' in self.settings["speechToText"]:
            args = self.settings["speechToText"]["args"]
        return args

    def loadSTTPlugin(self):
        sttPlugin = self._getSTTPlugin()
        sttArgs = self._getSTTArgs()

        # capitalizes the first letter (because classes have first letter upper case)
        sttPlugin = sttPlugin.capitalize()
        self._runSTTPPlugin(sttPlugin, sttArgs)


    def _runSTTPPlugin(self, sttPlugin, parameters=None):
        """
           Dynamic loading of a STT module
           :param plugin: Module name to load
           :param parameters: Parameter of the module
           :return:
           """
        print "Running STT %s with parameter %s" % (sttPlugin, parameters)
        mod = __import__('stt', fromlist=[sttPlugin])

        klass = getattr(mod, sttPlugin)

        if klass is not None:
            # run the plugin
            if not parameters:
                klass(self.main_controller)
            elif isinstance(parameters, dict):
                klass(self.main_controller, **parameters)
            else:
                klass(self.main_controller, parameters)


