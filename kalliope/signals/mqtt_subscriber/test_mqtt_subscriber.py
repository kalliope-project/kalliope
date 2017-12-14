import unittest

from kalliope.core.Models import Neuron, Signal, Synapse, Brain
from kalliope.signals.mqtt_subscriber import Mqtt_subscriber
from kalliope.signals.mqtt_subscriber.models import Broker, Topic


class TestMqtt_subscriber(unittest.TestCase):

    def test_check_mqtt_dict(self):

        valid_dict_of_parameters = {
            "topic": "my_topic",
            "broker_ip": "192.168.0.1"
        }

        invalid_dict_of_parameters = {
            "topic": "my_topic"
        }

        self.assertTrue(Mqtt_subscriber.check_parameters(valid_dict_of_parameters))
        self.assertFalse(Mqtt_subscriber.check_parameters(invalid_dict_of_parameters))

    def test_get_list_synapse_with_mqtt_subscriber(self):

        # test with one signal mqtt
        neuron = Neuron(name='say', parameters={'message': ['test message']})
        signal1 = Signal(name="mqtt_subscriber", parameters={"topic": "test", "broker_ip": "192.168.0.1"})
        synapse1 = Synapse(name="synapse1", neurons=[neuron], signals=[signal1])
        synapses = [synapse1]
        brain = Brain()
        brain.synapses = synapses

        expected_result = synapses

        mq = Mqtt_subscriber()
        mq.brain = brain

        generator = mq.get_list_synapse()

        self.assertEqual(expected_result, list(generator))

        # test with two synapse
        neuron = Neuron(name='say', parameters={'message': ['test message']})
        signal1 = Signal(name="order", parameters="test_order")
        signal2 = Signal(name="mqtt_subscriber", parameters={"topic": "test", "broker_ip": "192.168.0.1"})
        synapse1 = Synapse(name="synapse1", neurons=[neuron], signals=[signal1])
        synapse2 = Synapse(name="synapse2", neurons=[neuron], signals=[signal1, signal2])

        synapses = [synapse1, synapse2]
        brain = Brain()
        brain.synapses = synapses

        expected_result = [synapse2]

        mq = Mqtt_subscriber()
        mq.brain = brain
        generator = mq.get_list_synapse()

        self.assertEqual(expected_result, list(generator))

    def test_get_list_broker_to_instantiate(self):
        # ----------------
        # only one synapse
        # ----------------
        neuron = Neuron(name='say', parameters={'message': ['test message']})
        signal1 = Signal(name="mqtt_subscriber", parameters={"topic": "topic1", "broker_ip": "192.168.0.1"})
        synapse1 = Synapse(name="synapse1", neurons=[neuron], signals=[signal1])
        brain = Brain()
        brain.synapses = [synapse1]

        list_synapse_with_mqtt_subscriber = [synapse1]

        expected_broker = Broker()
        expected_broker.broker_ip = "192.168.0.1"
        expected_broker.topics = list()
        expected_topic = Topic()
        expected_topic.name = "topic1"
        # add the current synapse to the topic
        expected_topic.synapses = list()
        expected_topic.synapses.append(synapse1)
        expected_broker.topics.append(expected_topic)

        expected_retuned_list = [expected_broker]

        mq = Mqtt_subscriber()
        mq.brain = brain

        self.assertListEqual(expected_retuned_list,
                             mq.get_list_broker_to_instantiate(list_synapse_with_mqtt_subscriber))

        # ----------------
        #  one synapse, two different broker
        # ----------------
        neuron = Neuron(name='say', parameters={'message': ['test message']})
        signal1 = Signal(name="mqtt_subscriber", parameters={"topic": "topic1",
                                                             "broker_ip": "192.168.0.1",
                                                             "is_json": False})
        signal2 = Signal(name="mqtt_subscriber", parameters={"topic": "topic2",
                                                             "broker_ip": "172.16.0.1",
                                                             "is_json": False})
        synapse1 = Synapse(name="synapse1", neurons=[neuron], signals=[signal1, signal2])
        brain = Brain()
        brain.synapses = [synapse1]

        list_synapse_with_mqtt_subscriber = [synapse1]

        expected_broker1 = Broker()
        expected_broker1.broker_ip = "192.168.0.1"
        expected_broker1.topics = list()
        expected_topic = Topic()
        expected_topic.name = "topic1"
        # add the current synapse to the topic
        expected_topic.synapses = list()
        expected_topic.synapses.append(synapse1)
        expected_broker1.topics.append(expected_topic)

        expected_broker2 = Broker()
        expected_broker2.broker_ip = "172.16.0.1"
        expected_broker2.topics = list()
        expected_topic = Topic()
        expected_topic.name = "topic2"
        # add the current synapse to the topic
        expected_topic.synapses = list()
        expected_topic.synapses.append(synapse1)
        expected_broker2.topics.append(expected_topic)

        expected_retuned_list = [expected_broker1, expected_broker2]

        mq = Mqtt_subscriber()
        mq.brain = brain

        self.assertEqual(expected_retuned_list, mq.get_list_broker_to_instantiate(list_synapse_with_mqtt_subscriber))

        # ----------------
        #  two synapse, same broker, different topics
        # ----------------
        # synapse 1
        neuron1 = Neuron(name='say', parameters={'message': ['test message']})
        signal1 = Signal(name="mqtt_subscriber", parameters={"topic": "topic1", "broker_ip": "192.168.0.1"})
        synapse1 = Synapse(name="synapse1", neurons=[neuron1], signals=[signal1])

        # synapse 2
        neuron2 = Neuron(name='say', parameters={'message': ['test message']})
        signal2 = Signal(name="mqtt_subscriber", parameters={"topic": "topic2", "broker_ip": "192.168.0.1"})
        synapse2 = Synapse(name="synapse2", neurons=[neuron2], signals=[signal2])

        brain = Brain()
        brain.synapses = [synapse1, synapse2]

        list_synapse_with_mqtt_subscriber = [synapse1, synapse2]

        expected_broker1 = Broker()
        expected_broker1.broker_ip = "192.168.0.1"
        expected_broker1.topics = list()
        expected_topic1 = Topic()
        expected_topic1.name = "topic1"
        expected_topic2 = Topic()
        expected_topic2.name = "topic2"
        # add the current synapse to the topic
        expected_topic1.synapses = [synapse1]
        expected_topic2.synapses = [synapse2]
        # add both topic to the broker
        expected_broker1.topics.append(expected_topic1)
        expected_broker1.topics.append(expected_topic2)

        expected_retuned_list = [expected_broker1]

        mq = Mqtt_subscriber()
        mq.brain = brain

        self.assertEqual(expected_retuned_list, mq.get_list_broker_to_instantiate(list_synapse_with_mqtt_subscriber))

        # ----------------
        #  two synapse, same broker, same topic
        # ----------------
        # synapse 1
        neuron1 = Neuron(name='say', parameters={'message': ['test message']})
        signal1 = Signal(name="mqtt_subscriber", parameters={"topic": "topic1", "broker_ip": "192.168.0.1"})
        synapse1 = Synapse(name="synapse1", neurons=[neuron1], signals=[signal1])

        # synapse 2
        neuron2 = Neuron(name='say', parameters={'message': ['test message']})
        signal2 = Signal(name="mqtt_subscriber", parameters={"topic": "topic1", "broker_ip": "192.168.0.1"})
        synapse2 = Synapse(name="synapse2", neurons=[neuron2], signals=[signal2])

        brain = Brain()
        brain.synapses = [synapse1, synapse2]

        list_synapse_with_mqtt_subscriber = [synapse1, synapse2]

        expected_broker1 = Broker()
        expected_broker1.broker_ip = "192.168.0.1"
        expected_broker1.topics = list()
        expected_topic1 = Topic()
        expected_topic1.name = "topic1"
        # add both synapses to the topic
        expected_topic1.synapses = [synapse1, synapse2]
        # add the topic to the broker
        expected_broker1.topics.append(expected_topic1)

        expected_retuned_list = [expected_broker1]

        mq = Mqtt_subscriber()
        mq.brain = brain

        self.assertEqual(expected_retuned_list, mq.get_list_broker_to_instantiate(list_synapse_with_mqtt_subscriber))


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestMqtt_subscriber("test_get_list_broker_to_instantiate"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
