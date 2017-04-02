

class APIResponse(object):

    def __init__(self):
        self.user_order = None
        self.list_processed_matched_synapse = list()
        self.status = None

    def __str__(self):
        returned_string = ""
        for el in self.list_processed_matched_synapse:
            returned_string += str(el)

        return returned_string

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """

        return {
            'user_order': self.user_order,
            'list_processed_matched_synapse': [e.serialize() for e in self.list_processed_matched_synapse],
            'status': self.status
        }
