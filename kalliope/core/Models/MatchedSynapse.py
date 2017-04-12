import copy

from kalliope.core.NeuronParameterLoader import NeuronParameterLoader


class MatchedSynapse(object):
    """
    This class represent a synapse that has matched an order send by an User.
    """

    def __init__(self, matched_synapse=None, matched_order=None, user_order=None):
        """
        
        :param matched_synapse: The synapse that has matched in the brain
        :param matched_order: The order from the synapse that have matched
        """
        # create a copy of the synapse. the received synapse come from the brain.
        self.synapse = matched_synapse
        # create a fifo list that contains all neurons to process.
        # Create a copy to be sure when we remove a neuron from this list it will not be removed from the synapse's
        # neuron list
        self.neuron_fifo_list = copy.deepcopy(self.synapse.neurons)
        self.matched_order = matched_order
        self.parameters = dict()
        if matched_order is not None:
            self.parameters = NeuronParameterLoader.get_parameters(synapse_order=self.matched_order,
                                                                   user_order=user_order)

        # list of Neuron Module
        self.neuron_module_list = list()

    def __str__(self):
        returned_string = str()
        returned_string += str(self.synapse)
        returned_string += "answers: "
        for neuron_module in self.neuron_module_list:
            returned_string += str(neuron_module)

        return returned_string

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """
        return {
            'synapse_name': self.synapse.name,
            'matched_order': self.matched_order,
            'neuron_module_list': [e.serialize() for e in self.neuron_module_list]
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
