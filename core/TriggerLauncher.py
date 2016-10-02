import logging

logging.basicConfig()
logger = logging.getLogger("jarvis")


class TriggerLauncher(object):
    def __init__(self):
        pass

    @classmethod
    def start_trigger(cls, trigger_name, callback, parameters=None):
        """

        :param trigger_name: Name of the trigger class to instantiate
        :param callback: Callback function to call when the trigger
        catch the magic word
        :param parameters: Dict of parameter to send to the trigger
        :return:
        """
        pass
        # plugin = neuron.name.capitalize()
        # plugin = plugin.capitalize()
        # _run_plugin(plugin, neuron.parameters)
