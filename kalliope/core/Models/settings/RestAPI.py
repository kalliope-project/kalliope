from kalliope.core.Models.settings.SettingsEntry import SettingsEntry


class RestAPI(SettingsEntry):
    """
    This Class is representing the rest API with all its configuration.
    """

    def __init__(self,
                 password_protected=None,
                 login=None, password=None,
                 active=None,
                 port=None,
                 allowed_cors_origin=None):
        """
        :param password_protected: If true, the rest api will ask for an authentication
        :param login: login used if auth is activated
        :param password: password used if auth is activated
        :param active: specify if the rest api is loaded on start with Kalliope
        :param allowed_cors_origin: specify allowed origins
        """
        super(RestAPI, self).__init__("RestAPI")
        self.password_protected = password_protected
        self.login = login
        self.password = password
        self.active = active
        self.port = port
        self.allowed_cors_origin = allowed_cors_origin

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of order
        :rtype: Dict
        """

        return {
            'password_protected': self.password_protected,
            'login': self.login,
            'password': self.password,
            'active': self.active,
            'port': self.port,
            'allowed_cors_origin': self.allowed_cors_origin
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
