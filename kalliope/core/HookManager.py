from kalliope.core.ConfigurationManager import SettingLoader
import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class HookManager(object):

    @classmethod
    def on_start(cls):
        return cls.execute_synapses_in_hook_name("on_start")

    @classmethod
    def on_waiting_for_trigger(cls):
        return cls.execute_synapses_in_hook_name("on_waiting_for_trigger")

    @classmethod
    def on_triggered(cls):
        return cls.execute_synapses_in_hook_name("on_triggered")

    @classmethod
    def on_start_listening(cls):
        return cls.execute_synapses_in_hook_name("on_start_listening")

    @classmethod
    def on_stop_listening(cls):
        return cls.execute_synapses_in_hook_name("on_stop_listening")

    @classmethod
    def on_order_found(cls):
        return cls.execute_synapses_in_hook_name("on_order_found")

    @classmethod
    def on_order_not_found(cls):
        return cls.execute_synapses_in_hook_name("on_order_not_found")

    @classmethod
    def on_mute(cls):
        return cls.execute_synapses_in_hook_name("on_mute")

    @classmethod
    def on_unmute(cls):
        return cls.execute_synapses_in_hook_name("on_unmute")

    @classmethod
    def execute_synapses_in_hook_name(cls, hook_name):
        logger.debug("[HookManager] calling synapses in hook name: %s" % hook_name)
        settings = SettingLoader().settings
        from kalliope.core.SynapseLauncher import SynapseLauncher
        # list of synapse to execute
        list_synapse = settings.hooks[hook_name]

        print("hook: %s , type: %s" % (hook_name, type(list_synapse)))

        if isinstance(list_synapse, list):
            if list_synapse is not None:
                for synapse in list_synapse:
                    return SynapseLauncher.start_synapse_by_name(synapse)

        if isinstance(list_synapse, str):
            print("here")
            return SynapseLauncher.start_synapse_by_name(list_synapse)
