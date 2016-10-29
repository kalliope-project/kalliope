from core.Models import Singleton


@Singleton
class Brain:
    # TODO review the Singleton, should be Instantiate at the BrainLoader level
    """
    This Class is a Singleton Representing the Brain.yml file with synapse
    .. note:: the is_loaded Boolean is True when the Brain has been properly loaded.
    """

    def __init__(self, synapses=None, brain_file=None, brain_yaml=None):
        self.synapses = synapses
        self.brain_file = brain_file
        self.brain_yaml = brain_yaml
        self.is_loaded = False
