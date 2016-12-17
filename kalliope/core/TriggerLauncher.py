import logging

from kalliope.core import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TriggerLauncher(object):
    def __init__(self):
        pass

    @classmethod
    def get_trigger(cls, trigger, callback):
        """
        Start a trigger module
        :param trigger: trigger object to instantiate
        :type trigger: Trigger
        :param callback: Callback function to call when the trigger
        catch the magic word
        :return:
        """
        # add the callback method to parameters
        trigger.parameters["callback"] = callback
        logger.debug("TriggerLauncher: Start trigger %s with parameters: %s" % (trigger.name, trigger.parameters))
        return Utils.get_dynamic_class_instantiation(package_name="trigger",
                                                     module_name=trigger.name,
                                                     parameters=trigger.parameters)
