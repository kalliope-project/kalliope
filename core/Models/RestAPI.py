class RestAPI(object):
    def __init__(self, password_protected=None, login=None, password=None):
        self.password_protected = password_protected
        self.login = login
        self.password = password

    def __str__(self):
        return "%s: RestAPI: password_protected: %s, login: %s, password: %s" % (self.__class__.__name__,
                                                                                 self.password_protected,
                                                                                 self.login,
                                                                                 self.password)
