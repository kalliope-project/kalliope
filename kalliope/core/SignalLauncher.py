import logging

from kalliope import Utils
from kalliope.signals.order import Order

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SignalLauncher:

    # keep a list of instantiated signals
    list_launched_signals = list()

    def __init__(self):
        pass

    @classmethod
    def launch_signal_class_by_name(cls, signal_name, settings=None):
        """
        load the signal class from the given name, pass the brain and settings to the signal
        :param signal_name: name of the signal class to load
        :param settings: Settings Object
        """
        signal_folder = None
        if settings.resources:
            signal_folder = settings.resources.signal_folder

        launched_signal = Utils.get_dynamic_class_instantiation(package_name="signals",
                                                                module_name=signal_name,
                                                                resources_dir=signal_folder)

        cls.add_launched_signals_to_list(launched_signal)

        return launched_signal

    @classmethod
    def add_launched_signals_to_list(cls, signal):
        cls.list_launched_signals.append(signal)

    @classmethod
    def get_launched_signals_list(cls):
        return cls.list_launched_signals

    @classmethod
    def get_order_instance(cls):
        """
        Return the Order instance from the list of launched signals if exist
        :return:
        """
        for signal in cls.list_launched_signals:
            if isinstance(signal, Order):
                return signal
        return None
