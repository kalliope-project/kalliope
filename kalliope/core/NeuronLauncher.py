import logging

from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NeuronLauncher:

    def __init__(self):
        pass

    @classmethod
    def start_neuron(cls, neuron):
        """
        Start a neuron plugin
        :param neuron: neuron object
        :type neuron: Neuron
        :return:
        """
        logger.debug("Run neuron: \"%s\"" % (neuron.__str__()))
        sl = SettingLoader()
        settings = sl.settings
        neuron_folder = None
        if settings.resources:
            neuron_folder = settings.resources.neuron_folder

        return Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                     module_name=neuron.name,
                                                     parameters=neuron.parameters,
                                                     resources_dir=neuron_folder)

    @classmethod
    def start_neuron_list(cls, neuron_list, parameters_dict):
        """
        Execute each neuron from the received neuron_list.
        Replace parameter if existe in the received dict of parameters_dict
        :param neuron_list: list of Neuron object to run
        :param parameters_dict: dict of parameter to load in each neuron if expecting a parameter
        :return:
        """
        for neuron in neuron_list:

            problem_in_neuron_found = False
            if isinstance(neuron.parameters, dict):
                # print neuron.parameters
                if "args" in neuron.parameters:
                    logger.debug("The neuron waits for parameter")
                    # check that the user added parameters to his order
                    if parameters_dict is None:
                        # we don't raise an error and break the program but we don't run the neuron
                        problem_in_neuron_found = True
                        Utils.print_danger("Error: The neuron %s is waiting for argument. "
                                           "Argument found in bracket in the given order" % neuron.name)
                    else:
                        # we add wanted arguments the existing neuron parameter dict
                        for arg in neuron.parameters["args"]:
                            if arg in parameters_dict:
                                logger.debug("Parameter %s added to the current parameter "
                                             "of the neuron: %s" % (arg, neuron.name))
                                neuron.parameters[arg] = parameters_dict[arg]
                            else:
                                # we don't raise an error and break the program but
                                # we don't run the neuron
                                problem_in_neuron_found = True
                                Utils.print_danger("Error: Argument \"%s\" not found in the"
                                                   " order" % arg)

            # if no error detected, we run the neuron
            if not problem_in_neuron_found:
                cls.start_neuron(neuron)
            else:
                Utils.print_danger("A problem has been found in the Synapse.")
