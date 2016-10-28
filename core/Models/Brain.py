from core.Models import Singleton


@Singleton
class Brain:

    def __init__(self, synapses=None, brain_file=None, brain_yaml=None):
        self.synapses = synapses
        self.brain_file = brain_file
        self.brain_yaml = brain_yaml
        self.is_loaded = False
