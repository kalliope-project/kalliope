import logging

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.LIFOBuffer import LIFOBuffer
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.OrderAnalyser import OrderAnalyser


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
            return cls._run_synapse(synapse=synapse)

    @classmethod
    def _run_synapse(cls, synapse):
        """
        Start all neurons in the synapse
        :param synapse: Synapse for which we run neurons
        :return:
        """
        for neuron in synapse.neurons:
            instantiated_neuron = NeuronLauncher.start_neuron(neuron)
            # add the generated message to the synapse
            synapse.answers.append(instantiated_neuron.tts_message)
        return synapse

    @classmethod
    def run_matching_synapse_from_order(cls, order_to_process, brain, settings, is_api_call=False):
        """
        
        :param order_to_process: the spoken order sent by the user
        :param brain: Brain object
        :param settings: Settings object
        :param is_api_call: if True, the current call come from the API. This info must be known by launched Neuron
        :return: list of matched synapse
        """

        # get our single ton LIFO
        lifo_buffer = LIFOBuffer()

        # if the LIFO is not empty, so, the current order is passed to the current processing synapse as an answer
        if len(lifo_buffer.lifo_list) > 0:
            # the LIFO is not empty, this is an answer to a previous call
            return lifo_buffer.execute(answer=order_to_process, is_api_call=is_api_call)

        else:
            # the LIFO is empty, this is a new call

            # get a tuple of (synapse, order) that match in the brain
            synapses_to_launch_tuple = OrderAnalyser.get_matching_synapse(order=order_to_process, brain=brain)

            # we transform the tuple in a MatchedSynapse list
            list_synapse_to_process = list()

            if synapses_to_launch_tuple:  # the order analyser returned us a list
                for tuple_el in synapses_to_launch_tuple:
                    new_matching_synapse = MatchedSynapse(matched_synapse=tuple_el.synapse,
                                                          matched_order=tuple_el.order,
                                                          user_order=order_to_process)
                    list_synapse_to_process.append(new_matching_synapse)
            else:
                # execute the default synapse if exist
                if settings.default_synapse:
                    logger.debug("[SynapseLauncher] No matching Synapse-> running default synapse ")
                    # get the default synapse
                    default_synapse = BrainLoader().get_brain().get_synapse_by_name(settings.default_synapse)

                    new_matching_synapse = MatchedSynapse(matched_synapse=default_synapse,
                                                          matched_order=None,
                                                          user_order=order_to_process)
                    list_synapse_to_process.append(new_matching_synapse)

            lifo_buffer.add_synapse_list_to_lifo(list_synapse_to_process)

            lifo_buffer.api_response.user_order = order_to_process
            return lifo_buffer.execute(is_api_call=is_api_call)
