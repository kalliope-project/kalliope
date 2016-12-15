from kalliope.core.NeuronLauncher import NeuronLauncher


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
