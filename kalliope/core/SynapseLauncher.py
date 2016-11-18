from kalliope.core.NeuroneLauncher import NeuroneLauncher


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
        synapse_name_launch = name
        # get the brain
        cls.brain = brain

        # check if we have found and launched the synapse
        synapse_launched = False
        for synapse in cls.brain.synapses:
            if synapse.name == synapse_name_launch:
                cls._run_synapse(synapse)
                synapse_launched = True
                # we found the synapse, we don't need to check the rest of the list
                break

        if not synapse_launched:
            raise SynapseNameNotFound("The synapse name \"%s\" does not exist in the brain file" % name)

    @classmethod
    def _run_synapse(cls, synapse):
        """
        Start all neurons in the synapse
        :param synapse: Synapse for which we run neurons
        :return:
        """
        for neuron in synapse.neurons:
            NeuroneLauncher.start_neurone(neuron)
        return True
