import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Topic(object):
    def __init__(self, name=None, synapses=None, is_json=False):
        self.name = name
        self.synapses = synapses
        self.is_json = is_json

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """
        return {
            'name': self.name,
            'is_json': self.is_json,
            'synapses': [e.serialize() for e in self.synapses],
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


class Broker(object):
    def __init__(self, broker_ip=None, topics=None, port=1883, client_id="kalliope", keepalive=60,
                 username=None, password=None, protocol="MQTTv311", ca_cert=None, certfile=None, keyfile=None,
                 tls_insecure=False):
        self.broker_ip = broker_ip
        self.topics = topics
        if self.topics is None:
            self.topics = list()

        # optional value
        self.port = port
        self.client_id = client_id
        self.keepalive = keepalive
        self.username = username
        self.password = password
        self.protocol = protocol
        self.ca_cert = ca_cert
        self.certfile = certfile
        self.keyfile = keyfile
        self.tls_insecure = tls_insecure

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """
        return {
            'broker_ip': self.broker_ip,
            'port': self.port,
            'client_id': self.client_id,
            'keepalive': self.keepalive,
            'username': self.username,
            'password': self.password,
            'protocol': self.protocol,
            'ca_cert': self.ca_cert,
            'certfile': self.certfile,
            'keyfile': self.keyfile,
            'tls_insecure': self.tls_insecure,
            'topics': [e.serialize() for e in self.topics],
        }

    def __str__(self):
        return str(self.serialize())

    def build_from_signal_dict(self, dict_parameters):
        """
        Build the Broker object from a received dict of parameters
        :param dict_parameters: dict of parameters used to build the Broker object
        """
        logger.debug("[Broker] Build broker object from received parameters: %s" % dict_parameters)

        self.broker_ip = dict_parameters["broker_ip"]

        if "broker_port" in dict_parameters:
            self.port = dict_parameters["broker_port"]
            # keep alive must be an integer
            if not isinstance(self.keepalive, int):
                try:
                    self.port = int(self.port)
                except ValueError:
                    logger.debug("[Broker] Invalid port value, fallback to 1883")
                    self.port = 1883
        else:
            # set default port
            self.port = 1883

        if "client_id" in dict_parameters:
            self.client_id = dict_parameters["client_id"]
        else:
            self.client_id = "kalliope"

        if "username" in dict_parameters:
            self.username = dict_parameters["username"]

        if "password" in dict_parameters:
            self.password = dict_parameters["password"]

        if "keepalive" in dict_parameters:
            self.keepalive = dict_parameters["keepalive"]
            # keep alive must be an integer
            if not isinstance(self.keepalive, int):
                try:
                    self.keepalive = int(self.keepalive)
                except ValueError:
                    logger.debug("[Broker] Invalid keepalive value, fallback to 60")
                    self.keepalive = 60
        else:
            # set default value
            self.keepalive = 60

        if "protocol" in dict_parameters:
            if dict_parameters["protocol"] not in ["MQTTv31", "MQTTv311"]:
                logger.debug("[Broker] Invalid protocol value, fallback to MQTTv311")
                self.protocol = "MQTTv311"
            else:
                self.protocol = dict_parameters["protocol"]
        else:
            self.protocol = "MQTTv311"

        if "ca_cert" in dict_parameters:
            self.ca_cert = dict_parameters["ca_cert"]

        if "certfile" in dict_parameters:
            self.certfile = dict_parameters["certfile"]

        if "keyfile" in dict_parameters:
            self.keyfile = dict_parameters["keyfile"]

        if "tls_insecure" in dict_parameters:
            self.tls_insecure = dict_parameters["tls_insecure"]
            self.tls_insecure = bool(self.tls_insecure)
        else:
            self.tls_insecure = False

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
