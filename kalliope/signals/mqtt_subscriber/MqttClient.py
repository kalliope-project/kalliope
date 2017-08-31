import json
import logging
import socket
from threading import Thread

import paho
import paho.mqtt.client as mqtt
from kalliope.core.SynapseLauncher import SynapseLauncher

logging.basicConfig()
logger = logging.getLogger("kalliope")


class MqttClient(Thread):

    def __init__(self, broker=None, brain=None):
        """
        Class used to instantiate mqtt client
        Thread used to be non blocking when called from parent class
        :param broker: broker object
        :type broker: Broker
        """
        super(MqttClient, self).__init__()
        self.broker = broker
        self.brain = brain

        self.client = mqtt.Client(client_id=self.broker.client_id, protocol=self._get_protocol(self.broker.protocol))
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe

        if self.broker.username is not None and self.broker.password is not None:
            logger.debug("[MqttClient] Username and password are set")
            self.client.username_pw_set(self.broker.username, self.broker.password)

        if self.broker.ca_cert is not None and self.broker.certfile is not None and self.broker.keyfile is not None:
            logger.debug("[MqttClient] Active TLS with client certificate authentication")
            self.client.tls_set(ca_certs=self.broker.ca_cert,
                                certfile=self.broker.certfile,
                                keyfile=self.broker.keyfile)
            self.client.tls_insecure_set(self.broker.tls_insecure)

        elif self.broker.ca_cert is not None:
            logger.debug("[MqttClient] Active TLS with server CA certificate only")
            self.client.tls_set(ca_certs=self.broker.ca_cert)
            self.client.tls_insecure_set(self.broker.tls_insecure)

    def run(self):
        logger.debug("[MqttClient] Try to connect to broker: %s, port: %s, "
                     "keepalive: %s, protocol: %s" % (self.broker.broker_ip,
                                                      self.broker.port,
                                                      self.broker.keepalive,
                                                      self.broker.protocol))
        try:
            self.client.connect(self.broker.broker_ip, self.broker.port, self.broker.keepalive)
            self.client.loop_forever()
        except socket.error:
            logger.debug("[MqttClient] Unable to connect to broker %s" % self.broker.broker_ip)

    def on_connect(self, client, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from the server.
        """
        logger.debug("[MqttClient] Broker %s connection result code %s" % (self.broker.broker_ip, str(rc)))

        if rc == 0:  # success connection
            logger.debug("[MqttClient] Successfully connected to broker %s" % self.broker.broker_ip)
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            for topic in self.broker.topics:
                logger.debug("[MqttClient] Trying to subscribe to topic %s" % topic.name)
                client.subscribe(topic.name)
        else:
            logger.debug("[MqttClient] Broker %s connection failled. Disconnect" % self.broker.broker_ip)
            self.client.disconnect()

    def on_message(self, client, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the server
        """
        logger.debug("[MqttClient] " + msg.topic + ": " + str(msg.payload))

        self.call_concerned_synapses(msg.topic, msg.payload)

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        """
        The callback for when the client successfully subscribe to a topic on the server
        """
        logger.debug("[MqttClient] Successfully subscribed to topic")

    def call_concerned_synapses(self, topic_name, message):
        """
        Call synapse launcher class for each synapse concerned by the subscribed topic
        convert the message to json if needed before.
        The synapse is loaded with a parameter called "mqtt_subscriber_message" that can be used in neurons
        :param topic_name: name of the topic that received a message from the broker
        :param message: string message received from the broker
        """
        # find concerned topic by name
        target_topic = next(topic for topic in self.broker.topics if topic.name == topic_name)
        # convert payload to a dict if necessary
        if target_topic.is_json:
            message = json.loads(message)
            logger.debug("[MqttClient] Payload message converted to JSON dict: %s" % message)
        else:
            logger.debug("[MqttClient] Payload message is plain text: %s" % message)

        # run each synapse
        for synapse in target_topic.synapses:
            logger.debug("[MqttClient] start synapse name %s" % synapse.name)
            overriding_parameter_dict = dict()
            overriding_parameter_dict["mqtt_subscriber_message"] = message
            SynapseLauncher.start_synapse_by_name(synapse.name,
                                                  brain=self.brain,
                                                  overriding_parameter_dict=overriding_parameter_dict)

    @staticmethod
    def _get_protocol(protocol):
        """
        return the right protocol version number from the lib depending on the string protocol
        """
        if protocol == "MQTTv31":
            return paho.mqtt.client.MQTTv31
        return paho.mqtt.client.MQTTv311
