import logging

from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.NeuronParameterLoader import NeuronParameterLoader
from kalliope.core.OrderAnalyser2 import OrderAnalyser2


logging.basicConfig()
logger = logging.getLogger("kalliope")


class SynapseNameNotFound(Exception):
    """
    The Synapse has not been found

    .. seealso: Synapse
    """
    pass


class SynapseLauncher(object):

    def __init__(self):
        pass

    @classmethod
    def start_synapse(cls, name, brain=None):
        """
        Start a synapse by it's name
        :param name: Name (Unique ID) of the synapse to launch
        :param brain: Brain instance
        """

        # check if we have found and launched the synapse
        synapse = brain.get_synapse_by_name(synapse_name=name)

        if not synapse:
            raise SynapseNameNotFound("The synapse name \"%s\" does not exist in the brain file" % name)
        else:
            cls._run_synapse(synapse=synapse)

    @classmethod
    def _run_synapse(cls, synapse):
        """
        Start all neurons in the synapse
        :param synapse: Synapse for which we run neurons
        :return:
        """
        for neuron in synapse.neurons:
            NeuronLauncher.start_neuron(neuron)
        return True

    @classmethod
    def run_matching_synapse_or_default(cls, order_to_process, brain, settings):
        no_synapse_match = False
        if order_to_process is not None:  # maybe we have received a null audio from STT engine
            oa2 = OrderAnalyser2.get_matching_synapse(order=order_to_process, brain=brain)

            # oa2 contains the list Named tuple of synapse to run with the associated order that has matched
            # for each synapse, get neurons, et for each neuron, get parameters
            if not oa2:
                no_synapse_match = True
            else:
                # the order match one or more synapses
                for tuple_el in oa2:
                    logger.debug("Get parameter for %s " % tuple_el.synapse.name)
                    parameters = NeuronParameterLoader.get_parameters(synapse_order=tuple_el.order,
                                                                      user_order=order_to_process).next()
                    # start the neuron list
                    NeuronLauncher.start_neuron_list(neuron_list=tuple_el.synapse.neurons,
                                                     parameters_dict=parameters)
        else:
            no_synapse_match = True

        if no_synapse_match:  # then run the default synapse
            if settings.default_synapse is not None:
                SynapseLauncher.start_synapse(name=settings.default_synapse, brain=brain)
