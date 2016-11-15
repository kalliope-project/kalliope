class Order(object):
    """
    This Class is representing an Order which is raised by when an entry (Vocal/REST/ anything ...) is matching it.

    .. note:: Order are defined in the brain file for each synapse.
    """

    def __init__(self, sentence):
        self.sentence = sentence

    def __str__(self):
        return "%s: Sentence: %s" % (self.__class__.__name__, self.sentence)

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of order
        :rtype: Dict
        """

        return {
            'order': self.sentence
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
