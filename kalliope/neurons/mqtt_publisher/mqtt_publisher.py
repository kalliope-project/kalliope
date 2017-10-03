import logging
import socket

import paho
import paho.mqtt.client as mqtt

from kalliope.core.NeuronModule import NeuronModule

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Mqtt_publisher(NeuronModule):
    def __init__(self, **kwargs):
        super(Mqtt_publisher, self).__init__(**kwargs)

        logger.debug("[mqtt_publisher] neuron called with parameters: %s" % kwargs)

        # get parameters
        self.broker_ip = kwargs.get('broker_ip', None)
        self.port = kwargs.get('port', 1883)
        self.topic = kwargs.get('topic', None)
        self.payload = kwargs.get('payload', None)
        self.qos = kwargs.get('qos', 0)
        self.retain = kwargs.get('retain', False)
        self.client_id = kwargs.get('client_id', 'kalliope')
        self.keepalive = kwargs.get('keepalive', 60)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.ca_cert = kwargs.get('ca_cert', None)
        self.certfile = kwargs.get('certfile', None)
        self.keyfile = kwargs.get('keyfile', None)
        self.protocol = kwargs.get('protocol', 'MQTTv311')
        self.tls_insecure = kwargs.get('tls_insecure', False)

        if not self._is_parameters_ok():
            logger.debug("[mqtt_publisher] One or more invalid parameters, neuron will not be launched")
        else:
            # string must be converted
            self.protocol = self._get_protocol(self.protocol)

            self.client = mqtt.Client(client_id=self.broker_ip, protocol=self.protocol)

            if self.username is not None and self.password is not None:
                logger.debug("[mqtt_publisher] Username and password are set")
                self.client.username_pw_set(self.username, self.password)

            if self.ca_cert is not None and self.certfile is not None and self.keyfile is not None:
                logger.debug("[mqtt_publisher] Active TLS with client certificate authentication")
                self.client.tls_set(ca_certs=self.ca_cert,
                                    certfile=self.certfile,
                                    keyfile=self.keyfile)
                self.client.tls_insecure_set(self.tls_insecure)

            elif self.ca_cert is not None:
                logger.debug("[mqtt_publisher] Active TLS with server CA certificate only")
                self.client.tls_set(ca_certs=self.ca_cert)
                self.client.tls_insecure_set(self.tls_insecure)

            try:
                self.client.connect(self.broker_ip, port=self.port, keepalive=self.keepalive)
                self.client.publish(topic=self.topic, payload=self.payload, qos=int(self.qos), retain=self.retain)
                logger.debug("[mqtt_publisher] Message published to topic %s: %s" % (self.topic, self.payload))
                self.client.disconnect()
            except socket.error:
                logger.debug("[mqtt_publisher] Unable to connect to broker %s" % self.broker_ip)

    def _is_parameters_ok(self):
        if self.broker_ip is None:
            print("[mqtt_publisher] ERROR: broker_ip is not set")
            return False

        if self.port is not None:
            if not isinstance(self.port, int):
                try:
                    self.port = int(self.port)
                except ValueError:
                    print("[mqtt_publisher] ERROR: port must be an integer")
                    return False

        if self.topic is None:
            print("[mqtt_publisher] ERROR: topic is not set")
            return False

        if self.payload is None:
            print("[mqtt_publisher] ERROR: payload is not set")
            return False

        if self.qos:
            if not isinstance(self.qos, int):
                try:
                    self.qos = int(self.qos)
                except ValueError:
                    print("[mqtt_publisher] ERROR: qos must be an integer")
                    return False
            if self.qos not in [0, 1, 2]:
                print("[mqtt_publisher] ERROR: qos must be 0,1 or 2")
                return False

        if self.keepalive:
            if not isinstance(self.keepalive, int):
                try:
                    self.keepalive = int(self.keepalive)
                except ValueError:
                    print("[mqtt_publisher] ERROR: keepalive must be an integer")
                    return False

        if self.username is not None and self.password is None:
            print("[mqtt_publisher] ERROR: password must be set when using username")
            return False
        if self.username is None and self.password is not None:
            print("[mqtt_publisher] ERROR: username must be set when using password")
            return False

        if self.protocol:
            if self.protocol not in ["MQTTv31", "MQTTv311"]:
                print("[mqtt_publisher] Invalid protocol value, fallback to MQTTv311")
                self.protocol = "MQTTv311"

        # if the user set a certfile, the key and ca cert must be set to
        if self.certfile is not None and self.keyfile is None:
            print("[mqtt_publisher] ERROR: keyfile must be set when using certfile")
            return False
        if self.certfile is None and self.keyfile is not None:
            print("[mqtt_publisher] ERROR: certfile must be set when using keyfile")
            return False

        if self.certfile is not None and self.keyfile is not None:
            if self.ca_cert is None:
                print("[mqtt_publisher] ERROR: ca_cert must be set when using keyfile and certfile")
                return False

        return True

    def _get_protocol(self, protocol):
        """
        Return the right code depending on the given string protocol name
        :param protocol: string name of the protocol to use.
        :return: integer
        """
        if protocol == "MQTTv31":
            return paho.mqtt.client.MQTTv31
        return paho.mqtt.client.MQTTv311
