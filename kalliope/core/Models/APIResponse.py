import sys

class APIResponse(object):

    def __init__(self):
        self.user_order = None
        self.list_processed_matched_synapse = list()
        self.status = None

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        """
        This method allows to serialize in a proper way this object
        :return: A dict of name and parameters
        :rtype: Dict
        """
        if sys.version_info[0] < 3:
            if isinstance(self.user_order, unicode):
                self.user_order = self.user_order.encode("utf-8")
        return {
            'user_order': self.user_order,
            'matched_synapses': [e.serialize() for e in self.list_processed_matched_synapse],
            'status': self.status
        }
