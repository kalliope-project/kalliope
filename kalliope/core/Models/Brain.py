
class Brain:
    """
    This Class is a Singleton Representing the Brain.yml file with synapse
    .. note:: the is_loaded Boolean is True when the Brain has been properly loaded.
    """

    def __init__(self, synapses=None, brain_file=None, brain_yaml=None):
        self.synapses = synapses
        self.brain_file = brain_file
        self.brain_yaml = brain_yaml

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
