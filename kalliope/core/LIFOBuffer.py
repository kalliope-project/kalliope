import logging

from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.Models import Singleton
from kalliope.core.Models.APIResponse import APIResponse

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Serialize(Exception):
    """
    When raised, the LIFO class return the current API response to the caller
    """
    pass


class SynapseListAddedToLIFO(Exception):
    """
    When raised, a synapse list to process has been added to the LIFO list. 
    The LIFO must start over and process the last synapse list added
    """
    pass


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
    logger.debug("[LIFOBuffer] LIFO buffer created")
    answer = None
    is_api_call = False

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
    def clean(cls):
        """
        Clean the LIFO by creating a new list
        """
        cls.lifo_list = list()

    @classmethod
    def _return_serialized_api_response(cls):
        # we prepare a json response
        returned_api_response = cls.api_response.serialize()
        # we clean up the API response object for the next call
        cls.api_response = APIResponse()
        return returned_api_response

    @classmethod
    def execute(cls, answer=None, is_api_call=False):
        """
        Process the LIFO list.
        
        The LIFO list contains multiple list of matched synapses.        
        For each list of matched synapse we process synapses inside        
        For each synapses we process neurons.        
        If a neuron add a Synapse list to the lifo, this synapse list is processed before executing the first list 
        in which we were in.
        
        :param answer: String answer to give the the last neuron which whas waiting for an answer
        :param is_api_call: Boolean passed to all neuron in order to let them know if the current call comes from API
        :return: serialized APIResponse object
        """
        # store the answer if present
        cls.answer = answer
        cls.is_api_call = is_api_call

        try:
            # we keep looping over the LIFO til we have synapse list to process in it
            while cls.lifo_list:
                logger.debug("[LIFOBuffer] number of synapse list to process: %s" % len(cls.lifo_list))
                try:
                    cls._process_synapse_list()
                except SynapseListAddedToLIFO:
                    continue
            raise Serialize

        except Serialize:
            cls._return_serialized_api_response()

    @classmethod
    def _process_synapse_list(cls):
        # if we are back here because of an synapse_list_added_to_lifo switched to true,
        # get the last list of matched synapse in the LIFO
        last_synapse_fifo_list = cls.lifo_list[-1]
        # we keep processing til we have synapse in the FIFO to process
        while last_synapse_fifo_list:
            # get the first matched synapse in the list
            matched_synapse = last_synapse_fifo_list[0]
            # add the synapse to the API response so the user will get the status if the synapse was not already
            # in the response
            if matched_synapse not in cls.api_response.list_processed_matched_synapse:
                cls.api_response.list_processed_matched_synapse.append(matched_synapse)
            # while we have synapse to process in the list of synapse
            while matched_synapse.neuron_fifo_list:
                cls._process_neuron_list(matched_synapse=matched_synapse)

            # The synapse has been processed we can remove it from the list.
            last_synapse_fifo_list.remove(matched_synapse)

        # remove the synapse list from the LIFO
        cls.lifo_list.remove(last_synapse_fifo_list)

    @classmethod
    def _process_neuron_list(cls, matched_synapse):
        logger.debug("[LIFOBuffer] number of neuron to process: %s" % len(matched_synapse.neuron_fifo_list))
        # get the first neuron in the FIFO neuron list
        neuron = matched_synapse.neuron_fifo_list[0]
        # from here, we are back into the last neuron we were processing.
        if cls.answer is not None:  # we give the answer if exist to the first neuron
            neuron.parameters["answer"] = cls.answer
            # the next neuron should not get this answer
            cls.answer = None
        # todo fix this when we have a full client/server call. The client would be the voice or api call
        neuron.parameters["is_api_call"] = cls.is_api_call
        # execute the neuron
        instantiated_neuron = NeuronLauncher.start_neuron(neuron=neuron,
                                                          parameters_dict=matched_synapse.parameters)

        # the status of an execution is "complete" if no neuron are waiting for an answer
        cls.api_response.status = "complete"
        if instantiated_neuron.is_waiting_for_answer:  # the neuron is waiting for an answer
            logger.debug("[LIFOBuffer] Wait for answer mode")
            cls.api_response.status = "waiting_for_answer"
            raise Serialize
        else:
            logger.debug("[LIFOBuffer] complete mode")
            # we add the instantiated neuron to the neuron_module_list.
            # This one contains info about generated text
            matched_synapse.neuron_module_list.append(instantiated_neuron)
            # the neuron is fully processed we can remove it from the list
            matched_synapse.neuron_fifo_list.remove(neuron)

        if instantiated_neuron.pending_synapse:  # the last executed neuron want to run a synapse
            # add the synapse to the lifo (inside a list as expected by the lifo)
            cls.add_synapse_list_to_lifo([instantiated_neuron.pending_synapse])
            # we have added a list of synapse to the LIFO ! this one must start over.
            # break all while loop until the execution is back to the LIFO loop
            raise SynapseListAddedToLIFO
