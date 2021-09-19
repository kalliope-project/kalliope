import logging

from kalliope.core.Cortex import Cortex
from kalliope.core.NeuronLauncher import NeuronLauncher
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

    def __init__(self):
        logger.debug("[LIFOBuffer] LIFO buffer created")
        self.api_response = APIResponse()
        self.lifo_list = list()
        self.answer = None
        self.is_api_call = False
        self.is_running = False
        self.reset_lifo = False

    def set_answer(self, value):
        self.answer = value

    def set_api_call(self, value):
        self.is_api_call = value

    def add_synapse_list_to_lifo(self, matched_synapse_list, high_priority=False):
        """
        Add a synapse list to process to the lifo
        :param matched_synapse_list: List of Matched Synapse
        :param high_priority: If True, the synapse list added is executed directly
        :return:
        """
        logger.debug("[LIFOBuffer] Add a new synapse list to process to the LIFO")
        self.lifo_list.append(matched_synapse_list)
        self.reset_lifo = high_priority

    def clean(self):
        """
        Clean the LIFO by creating a new list
        """
        self.lifo_list = list()
        self.api_response = APIResponse()

    def _return_serialized_api_response(self):
        """
        Serialize Exception has been raised by the execute process somewhere, return the serialized API response
        to the caller. Clean up the APIResponse object for the next call
        :return:
        """
        # we prepare a json response
        returned_api_response = self.api_response.serialize()
        # we clean up the API response object for the next call
        self.api_response = APIResponse()
        return returned_api_response

    def execute(self, answer=None, is_api_call=False):
        """
        Process the LIFO list.

        The LIFO list contains multiple list of matched synapses.
        For each list of matched synapse we process synapses inside
        For each synapses we process neurons.
        If a neuron add a Synapse list to the lifo, this synapse list is processed before executing the first list
        in which we were in.

        :param answer: String answer to give the the last neuron which was waiting for an answer
        :param is_api_call: Boolean passed to all neuron in order to let them know if the current call comes from API
        :return: serialized APIResponse object
        """
        # store the answer if present
        self.answer = answer
        self.is_api_call = is_api_call

        try:
            if not self.is_running:
                self.is_running = True

                # we keep looping over the LIFO til we have synapse list to process in it
                while self.lifo_list:
                    logger.debug("[LIFOBuffer] number of synapse list to process: %s" % len(self.lifo_list))
                    try:
                        # get the last list of matched synapse in the LIFO
                        last_synapse_fifo_list = self.lifo_list[-1]
                        self._process_synapse_list(last_synapse_fifo_list)
                    except SynapseListAddedToLIFO:
                        continue
                    # remove the synapse list from the LIFO
                    self.lifo_list.remove(last_synapse_fifo_list)
                    # clean the cortex from value loaded from order as all synapses have been processed
                    Cortex.clean_parameter_from_order()
                self.is_running = False
                raise Serialize

        except Serialize:
            return self._return_serialized_api_response()

    def _process_synapse_list(self, synapse_list):
        """
        Process a list of matched synapse.
        Execute each neuron list for each synapse.
        Add info in the API response object after each processed synapse
        Remove the synapse from the synapse_list when it has been fully executed
        :param synapse_list: List of MatchedSynapse
        """
        # we keep processing til we have synapse in the FIFO to process
        while synapse_list:
            # get the first matched synapse in the list
            matched_synapse = synapse_list[0]
            # add the synapse to the API response so the user will get the status if the synapse was not already
            # in the response
            if matched_synapse not in self.api_response.list_processed_matched_synapse:
                self.api_response.list_processed_matched_synapse.append(matched_synapse)

            self._process_neuron_list(matched_synapse=matched_synapse)

            # The synapse has been processed we can remove it from the list.
            synapse_list.remove(matched_synapse)

    def _process_neuron_list(self, matched_synapse):
        """
        Process the neuron list of the matched_synapse
        Execute the Neuron
        Executing a Neuron creates a NeuronModule object. This one can have 3 status:
        - waiting for an answer: The neuron wait for an answer from the caller. The api response object is returned.
                                 The neuron is not removed from the matched synapse to be executed again
        - want to execute a synapse: The neuron add a list of synapse to execute to the lifo. 
                                     The LIFO restart over to process it.The neuron is removed from the matched synapse
        - complete: The neuron has been executed and its not waiting for an answer and doesn't want to start a synapse
                    The neuron is removed from the matched synapse
        :param matched_synapse: MatchedSynapse object to process
        """

        logger.debug("[LIFOBuffer] number of neuron to process: %s" % len(matched_synapse.neuron_fifo_list))
        # while we have synapse to process in the list of synapse
        while matched_synapse.neuron_fifo_list:
            # get the first neuron in the FIFO neuron list
            neuron = matched_synapse.neuron_fifo_list[0]
            # from here, we are back into the last neuron we were processing.
            if self.answer is not None:  # we give the answer if exist to the first neuron
                neuron.parameters["answer"] = self.answer
                # the next neuron should not get this answer
                self.answer = None
            # todo fix this when we have a full client/server call. The client would be the voice or api call
            neuron.parameters["is_api_call"] = self.is_api_call
            logger.debug("[LIFOBuffer] process_neuron_list: is_api_call: %s" % self.is_api_call)
            # execute the neuron
            instantiated_neuron = NeuronLauncher.start_neuron(neuron=neuron,
                                                              parameters_dict=matched_synapse.parameters)

            # the status of an execution is "complete" if no neuron are waiting for an answer
            self.api_response.status = "complete"
            if instantiated_neuron is not None:
                if instantiated_neuron.is_waiting_for_answer:  # the neuron is waiting for an answer
                    logger.debug("[LIFOBuffer] Wait for answer mode")
                    self.api_response.status = "waiting_for_answer"
                    self.is_running = False
                    raise Serialize
                else:
                    logger.debug("[LIFOBuffer] complete mode")
                    # we add the instantiated neuron to the neuron_module_list.
                    # This one contains info about generated text
                    matched_synapse.neuron_module_list.append(instantiated_neuron)
                    # the neuron is fully processed we can remove it from the list
                    matched_synapse.neuron_fifo_list.remove(neuron)

                if self.reset_lifo:  # the last executed neuron want to run a synapse
                    logger.debug("[LIFOBuffer] Last executed neuron want to run a synapse. Restart the LIFO")
                    # we have added a list of synapse to the LIFO ! this one must start over.
                    # break all while loop until the execution is back to the LIFO loop
                    self.reset_lifo = False
                    raise SynapseListAddedToLIFO
            else:
                # the neuron has not been processed but we still need to remove it from the list
                matched_synapse.neuron_fifo_list.remove(neuron)
