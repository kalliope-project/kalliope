import logging

from kalliope import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SignalLauncher:

    def __init__(self):
        pass

    @classmethod
    def launch_signal_class_by_name(cls, signal_name, brain=None, settings=None):
        """
        load the signal class from the given name, pass the brain and settings to the signal
        :param signal_name: name of the signal class to load
        :param brain: Brain Object
        :param settings: Settings Object
        """
        signal_folder = None
        if settings.resources:
            signal_folder = settings.resources.signal_folder

        return Utils.get_dynamic_class_instantiation(package_name="signals",
                                                     module_name=signal_name,
                                                     resources_dir=signal_folder)
