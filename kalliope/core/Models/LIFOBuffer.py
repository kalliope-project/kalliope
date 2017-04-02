import logging

from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.Models import Singleton
from kalliope.core.Models.APIResponse import APIResponse

logging.basicConfig()
logger = logging.getLogger("kalliope")


class LIFOBuffer(object):
    """
    This class is a LIFO list of synapse to process where the last synapse list to enter will be the first synapse
    list to be processed.
    This design is needed in order to use Kalliope from the API. 
    Because we want to return an information when a Neuron is still processing and waiting for an answer from the user
    like with the Neurotransmitter neuron.
    
    """
    __metaclass__ = Singleton

    api_response = APIResponse()
    lifo_list = list()
    synapse_list_added_to_lifo = False
    logger.debug("[LIFOBuffer] LIFO buffer created")

    @classmethod
    def add_synapse_list_to_lifo(cls, matched_synapse_list):
        """
        Add a synapse list to process to the lifo
        :param matched_synapse_list: List of Matched Synapse
        :return: 
        """
        logger.debug("[LIFOBuffer] Add a new synapse list to process to the LIFO")
        cls.lifo_list.append(matched_synapse_list)

    @classmethod
    def execute(cls, answer=None):

        # we keep looping over the LIFO til we have synapse list to process in it
        while cls.lifo_list:
            logger.debug("[LIFOBuffer] number of synapse list to process: %s" % len(cls.lifo_list))
            # if we are back here because of an synapse_list_added_to_lifo switched to true,
            # we reset it in order to pass through all while loop again and check all synapse list and neuron list
            cls.synapse_list_added_to_lifo = False
            # get the last list of matched synapse in the LIFO
            last_synapse_fifo_list = cls.lifo_list[-1]
            # we keep processing til we have synapse in the FIFO to process
            while last_synapse_fifo_list:
                # a synapse list has been added to the LIFO. we break this loop to go up into the lifo list loop
                if cls.synapse_list_added_to_lifo:
                    break
                # get the first matched synapse in the list
                matched_synapse = last_synapse_fifo_list[0]
                # add the synapse to the API response so the user will get the status
                cls.api_response.list_processed_matched_synapse.append(matched_synapse)
                # while we have synapse to process in the list of synapse
                while matched_synapse.neuron_fifo_list:
                    if cls.synapse_list_added_to_lifo:
                        break
                    logger.debug("[LIFOBuffer] number of neuron to process: %s" % len(matched_synapse.neuron_fifo_list))
                    # get the first neuron in the FIFO neuron list
                    neuron = matched_synapse.neuron_fifo_list[0]
                    # from here, we are back into the last neuron we were processing.
                    if answer is not None:  # we give the answer if exist to the first neuron
                        neuron.parameters["answer"] = answer
                        # the next neuron should not get this answer
                        answer = None
                    # todo fix this when we have a full client/server call. The client would be the voice or api call
                    neuron.parameters["is_api_call"] = True
                    # execute the neuron
                    instantiated_neuron = NeuronLauncher.start_neuron_list_refacto(
                        neuron=neuron,
                        parameters_dict=matched_synapse.parameters)

                    # by default, the status of an execution is "complete" if no neuron are waiting for an answer
                    cls.api_response.status = "complete"
                    if not instantiated_neuron.is_waiting_for_answer:  # the neuron is not waiting for an answer
                        # we add the instantiated neuron to the neuron_module_list.
                        # This one contains info about generated text
                        matched_synapse.neuron_module_list.append(instantiated_neuron)
                        # the neuron is fully processed we can remove it from the list
                        matched_synapse.neuron_fifo_list.remove(neuron)
                    else:
                        print "Wait for answer mode"
                        cls.api_response.status = "waiting_for_answer"
                        # we prepare a json response
                        will_be_returned = cls.api_response.serialize()
                        # we clean up the API response object for the next call
                        cls.api_response = APIResponse()
                        return will_be_returned

                    if instantiated_neuron.pending_synapse:  # the last executed neuron want to run a synapse
                        # add the synapse to the lifo (inside a list as expected by the lifo)
                        cls.add_synapse_list_to_lifo([instantiated_neuron.pending_synapse])
                        # we have added a list of synapse to the LIFO ! this one must start over.
                        # The following boolean will break all while loop until the execution is back to the LIFO loop
                        cls.synapse_list_added_to_lifo = True

                # we can only remove the matched synapse from the list if all neuron in it have been executed
                if not cls.synapse_list_added_to_lifo:
                    # remove the synapse
                    last_synapse_fifo_list .remove(matched_synapse)

            # we can only remove the list of synapse from the LIFO if all synapse in it have been executed
            if not cls.synapse_list_added_to_lifo:
                # remove the synapse list from the LIFO
                cls.lifo_list.remove(last_synapse_fifo_list)

        return cls.api_response.serialize()
