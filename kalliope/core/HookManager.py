from kalliope._version import version_str
from kalliope.core.ConfigurationManager import SettingLoader
import logging

from kalliope.core.Utils.google_tracking import GoogleTracking

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
        sl = SettingLoader()
        if sl.settings.send_anonymous_usage_stats > 0:  # the user allow to send hit
            gt = GoogleTracking(cid=sl.settings.send_anonymous_usage_stats,
                                kalliope_version=version_str,
                                category='synapse',
                                action='execute')
            gt.start()
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
    def on_processed_synapses(cls):
        return cls.execute_synapses_in_hook_name("on_processed_synapses")

    @classmethod
    def on_deaf(cls):
        return cls.execute_synapses_in_hook_name("on_deaf")

    @classmethod
    def on_undeaf(cls):
        return cls.execute_synapses_in_hook_name("on_undeaf")

    @classmethod
    def on_mute(cls):
        return cls.execute_synapses_in_hook_name("on_mute")

    @classmethod
    def on_unmute(cls):
        return cls.execute_synapses_in_hook_name("on_unmute")

    @classmethod
    def on_start_speaking(cls):
        return cls.execute_synapses_in_hook_name("on_start_speaking")

    @classmethod
    def on_stop_speaking(cls):
        return cls.execute_synapses_in_hook_name("on_stop_speaking")

    @classmethod
    def on_stt_error(cls):
        return cls.execute_synapses_in_hook_name("on_stt_error")

    @classmethod
    def execute_synapses_in_hook_name(cls, hook_name):
        # need to import SynapseLauncher from here to avoid cross import
        from kalliope.core.SynapseLauncher import SynapseLauncher

        logger.debug("[HookManager] calling synapses in hook name: %s" % hook_name)

        settings = SettingLoader().settings

        # list of synapse to execute
        try:
            list_synapse = settings.hooks[hook_name]
            logger.debug("[HookManager] hook: %s , type: %s" % (hook_name, type(list_synapse)))
        except KeyError:
            # the hook haven't been set in setting. just skip the execution
            logger.debug("[HookManager] hook not set: %s" % hook_name)
            return None

        if isinstance(list_synapse, str):
            list_synapse = [list_synapse]
        return SynapseLauncher.start_synapse_by_list_name(list_synapse, new_lifo=True)