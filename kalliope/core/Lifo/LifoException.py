

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
    def __init__(self, message=None):
        # Call the base class constructor with the parameters it needs
        super(SynapseListAddedToLIFO, self).__init__(message)
        self.message = message
        print(message)