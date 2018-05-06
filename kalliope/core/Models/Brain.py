import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Brain:
    """
    This Class is a Singleton Representing the Brain.yml file with synapse
    .. note:: the is_loaded Boolean is True when the Brain has been properly loaded.
    """

    def __init__(self, synapses=None, brain_file=None, brain_yaml=None):
        self.synapses = synapses
        self.brain_file = brain_file
        self.brain_yaml = brain_yaml

    def get_synapse_by_name(self, synapse_name):
        """
        Get the synapse, using its synapse name, from the synapse list
        :param synapse_name: the name of the synapse to get
        :type synapse_name: str
        :return: The Synapse corresponding to the name
        :rtype: Synapse
        """
        synapse_launched = None
        for synapse in self.synapses:
            if synapse.name == synapse_name:
                synapse_launched = synapse
                # we found the synapse, we don't need to check the rest of the list
                break
        return synapse_launched

    def disable_synapse_by_name(self, synapse_name):
        """
        disable a synapse from the brain by its name
        :param synapse_name: the name of the synapse to disable
        :return: True if the synapse has been disabled
        """
        for synapse in self.synapses:
            if synapse.name == synapse_name:
                logger.debug("[Brain] disable synapse name: %s" % synapse_name)
                synapse.enabled = False
                return True
        logger.debug("[Brain] Cannot disable synapse name: %s. Synapse not found" % synapse_name)
        return False

    def enable_synapse_by_name(self, synapse_name):
        """
        enable a synapse from the brain by its name
        :param synapse_name: the name of the synapse to enable
        :return: True if the synapse has been enabled
        """
        for synapse in self.synapses:
            if synapse.name == synapse_name:
                logger.debug("[Brain] enable synapse name: %s" % synapse_name)
                synapse.enabled = True
                return True
        logger.debug("[Brain] Cannot enable synapse name: %s. Synapse not found" % synapse_name)
        return False

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
