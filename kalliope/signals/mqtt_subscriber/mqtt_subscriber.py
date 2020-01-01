import logging
from threading import Thread

from kalliope.core import SignalModule
from kalliope.core import Utils
from kalliope.signals.mqtt_subscriber.MqttClient import MqttClient
from kalliope.signals.mqtt_subscriber.models import Broker, Topic

CLIENT_ID = "kalliope"

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Mqtt_subscriber(SignalModule, Thread):

    def __init__(self, **kwargs):
        super(Mqtt_subscriber, self).__init__(**kwargs)
        Thread.__init__(self, name=Mqtt_subscriber)
        Utils.print_info('[Mqtt_subscriber] Starting manager')  # variables
        self.list_synapses_with_mqtt = list(super(Mqtt_subscriber, self).get_list_synapse())
        self.broker_ip = None
        self.topic = None
        self.json_message = False

    def run(self):
        logger.debug("[Mqtt_subscriber] Starting Mqtt_subscriber")

        # we need to sort broker URL by ip, then for each broker, we sort by topic and attach synapses name to run to it
        list_broker_to_instantiate = self.get_list_broker_to_instantiate(self.list_synapses_with_mqtt)

        # now instantiate a MQTT client for each broker object
        self.instantiate_mqtt_client(list_broker_to_instantiate)

    @staticmethod
    def check_parameters(parameters):
        """
        overwrite method
        receive a dict of parameter from a mqtt_subscriber signal
        :param parameters: dict of mqtt_signal_parameters
        :return: True if parameters are valid
        """
        # check mandatory parameters
        mandatory_parameters = ["broker_ip", "topic"]
        if not all(key in parameters for key in mandatory_parameters):
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
                    if "is_json" in signal.parameters:
                        logger.debug("[Mqtt_subscriber] Message for the topic %s will be json converted"
                                     % new_topic.name)
                        new_topic.is_json = bool(signal.parameters["is_json"])
                    else:
                        new_topic.is_json = False
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
                        if "is_json" in signal.parameters:
                            logger.debug("[Mqtt_subscriber] Message for the topic %s will be json converted"
                                         % new_topic.name)
                            new_topic.is_json = bool(signal.parameters["is_json"])
                        else:
                            new_topic.is_json = False
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
