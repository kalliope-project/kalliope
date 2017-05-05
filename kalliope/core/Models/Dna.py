

class Dna(object):

    def __init__(self, name=None, module_type=None, author=None, kalliope_supported_version=None, tags=None):
        self.name = name
        self.module_type = module_type  # type is a reserved python
        self.author = author
        self.kalliope_supported_version = kalliope_supported_version
        self.tags = tags

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """
        return {
            'name': self.name,
            'type': self.module_type,
            'author': self.author,
            'kalliope_supported_version': self.kalliope_supported_version,
            'tags': self.tags
        }

    def __str__(self):
        return str(self.serialize())

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
