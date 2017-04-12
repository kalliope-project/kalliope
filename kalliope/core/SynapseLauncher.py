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

    @classmethod
    def start_synapse_by_name(cls, name, brain=None):
        """
        Start a synapse by it's name
        :param name: Name (Unique ID) of the synapse to launch
        :param brain: Brain instance
        """
        logger.debug("[SynapseLauncher] start_synapse_by_name called with synapse name: %s " % name)
        # check if we have found and launched the synapse
        synapse = brain.get_synapse_by_name(synapse_name=name)

        if not synapse:
            raise SynapseNameNotFound("The synapse name \"%s\" does not exist in the brain file" % name)
        else:
            # get our singleton LIFO
            lifo_buffer = LIFOBuffer()
            list_synapse_to_process = list()
            new_matching_synapse = MatchedSynapse(matched_synapse=synapse,
                                                  matched_order=None,
                                                  user_order=None)
            list_synapse_to_process.append(new_matching_synapse)
            lifo_buffer.add_synapse_list_to_lifo(list_synapse_to_process)
            return lifo_buffer.execute(is_api_call=True)

    @classmethod
    def run_matching_synapse_from_order(cls, order_to_process, brain, settings, is_api_call=False):
        """
        
        :param order_to_process: the spoken order sent by the user
        :param brain: Brain object
        :param settings: Settings object
        :param is_api_call: if True, the current call come from the API. This info must be known by launched Neuron
        :return: list of matched synapse
        """

        # get our singleton LIFO
        lifo_buffer = LIFOBuffer()

        # if the LIFO is not empty, so, the current order is passed to the current processing synapse as an answer
        if len(lifo_buffer.lifo_list) > 0:
            # the LIFO is not empty, this is an answer to a previous call
            return lifo_buffer.execute(answer=order_to_process, is_api_call=is_api_call)

        else:  # the LIFO is empty, this is a new call
            # get a list of matched synapse from the order
            list_synapse_to_process = OrderAnalyser.get_matching_synapse(order=order_to_process, brain=brain)

            if not list_synapse_to_process:  # the order analyser returned us an empty list
                # add the default synapse if exist into the lifo
                if settings.default_synapse:
                    logger.debug("[SynapseLauncher] No matching Synapse-> running default synapse ")
                    # get the default synapse
                    default_synapse = BrainLoader().get_brain().get_synapse_by_name(settings.default_synapse)

                    new_matching_synapse = MatchedSynapse(matched_synapse=default_synapse,
                                                          matched_order=None,
                                                          user_order=order_to_process)
                    list_synapse_to_process.append(new_matching_synapse)
                else:
                    logger.debug("[SynapseLauncher] No matching Synapse and no default synapse ")

            lifo_buffer.add_synapse_list_to_lifo(list_synapse_to_process)
            lifo_buffer.api_response.user_order = order_to_process

            return lifo_buffer.execute(is_api_call=is_api_call)
