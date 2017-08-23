import logging
from threading import Thread

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.signals.mqtt_subscriber.MqttClient import MqttClient
from kalliope.signals.mqtt_subscriber.models import Broker, Topic

CLIENT_ID = "kalliope"

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Mqtt_subscriber(Thread):

    def __init__(self, brain=None):
        super(Mqtt_subscriber, self).__init__()
        logger.debug("[Mqtt_subscriber] Mqtt_subscriber class created")
        # variables
        self.broker_ip = None
        self.topic = None
        self.json_message = False

        self.brain = brain
        if self.brain is None:
            self.brain = BrainLoader().get_brain()

    def run(self):
        logger.debug("[Mqtt_subscriber] Starting Mqtt_subscriber")
        # get the list of synapse that use Mqtt_subscriber as signal
        list_synapse_with_mqtt_subscriber = self.get_list_synapse_with_mqtt_subscriber(brain=self.brain)

        # we need to sort broker URL by ip, then for each broker, we sort by topic and attach synapses name to run to it
        list_broker_to_instantiate = self.get_list_broker_to_instantiate(list_synapse_with_mqtt_subscriber)

        # now instantiate a MQTT client for each broker object
        self.instantiate_mqtt_client(list_broker_to_instantiate)

    def get_list_synapse_with_mqtt_subscriber(self, brain):
        """
        return the list of synapse that use Mqtt_subscriber as signal in the provided brain
        :param brain: Brain object that contain all synapses loaded
        :type brain: Brain
        :return: list of synapse that use Mqtt_subscriber as signal
        """
        for synapse in brain.synapses:
            for signal in synapse.signals:
                # if the signal is an event we add it to the task list
                if signal.name == "mqtt_subscriber":
                    if self.check_mqtt_dict(signal.parameters):
                        yield synapse

    @staticmethod
    def check_mqtt_dict(mqtt_signal_parameters):
        """
        receive a dict of parameter from a mqtt_subscriber signal and them
        :param mqtt_signal_parameters: dict of parameters
        :return: True if parameters are valid
        """
        # check mandatory parameters
        mandatory_parameters = ["broker_ip", "topic"]
        if not all(key in mqtt_signal_parameters for key in mandatory_parameters):
            return False

        return True

    @staticmethod
    def get_list_broker_to_instantiate(list_synapse_with_mqtt_subscriber):
        """
        return a list of Broker object from the given list of synapse
        :param list_synapse_with_mqtt_subscriber: list of Synapse object
        :return: list of Broker
        """
        returned_list_of_broker = list()

        for synapse in list_synapse_with_mqtt_subscriber:
            for signal in synapse.signals:
                # check if the broker exist in the list
                if not any(x.broker_ip == signal.parameters["broker_ip"] for x in returned_list_of_broker):
                    logger.debug("[Mqtt_subscriber] Create new broker: %s" % signal.parameters["broker_ip"])
                    # create a new broker object
                    new_broker = Broker()
                    new_broker.build_from_signal_dict(signal.parameters)
                    # add the current topic
                    logger.debug("[Mqtt_subscriber] Add new topic to broker %s: %s" % (new_broker.broker_ip,
                                                                                       signal.parameters["topic"]))
                    new_topic = Topic()
                    new_topic.name = signal.parameters["topic"]
                    # add the current synapse to the topic
                    new_topic.synapses = list()
                    new_topic.synapses.append(synapse)
                    new_broker.topics.append(new_topic)

                    logger.debug("[Mqtt_subscriber] Add new synapse to topic %s :%s" % (new_topic.name, synapse.name))
                    returned_list_of_broker.append(new_broker)
                else:
                    # the broker exist. get it from the list of broker
                    broker_to_edit = next((broker for broker in returned_list_of_broker
                                           if signal.parameters["broker_ip"] == broker.broker_ip))
                    # check if the topic already exist
                    if not any(topic.name == signal.parameters["topic"] for topic in broker_to_edit.topics):
                        new_topic = Topic()
                        new_topic.name = signal.parameters["topic"]
                        logger.debug("[Mqtt_subscriber] Add new topic to existing broker "
                                     "%s: %s" % (broker_to_edit.broker_ip, signal.parameters["topic"]))
                        # add the current synapse to the topic
                        logger.debug("[Mqtt_subscriber] Add new synapse "
                                     "to topic %s :%s" % (new_topic.name, synapse.name))
                        new_topic.synapses = list()
                        new_topic.synapses.append(synapse)
                        # add the topic to the broker
                        broker_to_edit.topics.append(new_topic)
                    else:
                        # the topic already exist, get it from the list
                        topic_to_edit = next((topic for topic in broker_to_edit.topics
                                              if topic.name == signal.parameters["topic"]))
                        # add the synapse
                        logger.debug("[Mqtt_subscriber] Add synapse %s to existing topic %s "
                                     "in existing broker %s" % (synapse.name,
                                                                topic_to_edit.name,
                                                                broker_to_edit.broker_ip))
                        topic_to_edit.synapses.append(synapse)

        return returned_list_of_broker

    def instantiate_mqtt_client(self, list_broker_to_instantiate):
        """
        Instantiate a MqttClient thread for each broker
        :param list_broker_to_instantiate: list of broker to run
        """
        for broker in list_broker_to_instantiate:
            mqtt_client = MqttClient(broker=broker, brain=self.brain)
            mqtt_client.start()
