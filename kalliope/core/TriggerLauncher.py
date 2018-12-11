import logging

from kalliope.core import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TriggerLauncher(object):
    def __init__(self):
        pass

    @staticmethod
    def get_trigger(settings, callback):
        """
        Start a trigger module
        :param trigger: trigger object to instantiate
        :type trigger: Trigger
        :param callback: Callback function to call when the trigger catch the magic word
        :return: The instance of Trigger 
        :rtype: Trigger
        """
        trigger_folder = None
        if settings.resources:
            trigger_folder = settings.resources.trigger_folder
            
        trigger_instance = None
        for trigger in settings.triggers:
            if trigger.name == settings.default_trigger_name:
                # add the callback method to parameters
                trigger.parameters["callback"] = callback
                logger.debug(
                    "TriggerLauncher: Start trigger %s with parameters: %s" % (trigger.name, trigger.parameters))
                trigger_instance = Utils.get_dynamic_class_instantiation(package_name="trigger",
                                                                         module_name=trigger.name,
                                                                         parameters=trigger.parameters,
                                                                         resources_dir=trigger_folder)
                break
        return trigger_instance