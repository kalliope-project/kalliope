import os
import unittest

from kalliope.core.Models import Singleton

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.Models import Event
from kalliope.core.Models import Neuron
from kalliope.core.Models import Synapse
from kalliope.core.Models import Order
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.Settings import Settings


class TestBrainLoader(unittest.TestCase):

    def setUp(self):
        self.brain_to_test = os.getcwd() + os.sep + "Tests/brains/brain_test.yml"
        self.expected_result = [
            {'signals': [{'order': 'test_order'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test'},
            {'signals': [{'order': 'test_order_2'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test2'},
            {'includes': ['included_brain_test.yml']},
            {'signals': [{'order': 'test_order_3'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test3'}
        ]

    def tearDown(self):
        Singleton._instances = {}

    def test_get_yaml_config(self):
        """
        Test we can get a yaml config from the path
        """
        brain_loader = BrainLoader(file_path=self.brain_to_test)
        self.assertEqual(brain_loader.yaml_config, self.expected_result)

    def test_get_brain(self):
        """
        Test the class return a valid brain object
        """

        neuron = Neuron(name='say', parameters={'message': ['test message']})

        signal1 = Order(sentence="test_order")
        signal2 = Order(sentence="test_order_2")
        signal3 = Order(sentence="test_order_3")

        synapse1 = Synapse(name="test", neurons=[neuron], signals=[signal1])
        synapse2 = Synapse(name="test2", neurons=[neuron], signals=[signal2])
        synapse3 = Synapse(name="test3", neurons=[neuron], signals=[signal3])
        synapses = [synapse1, synapse2, synapse3]

        brain = Brain()
        brain.synapses = synapses
        brain.brain_file = self.brain_to_test
        brain.brain_yaml = self.expected_result

        brain_loader = BrainLoader(file_path=self.brain_to_test)
        self.assertEqual(brain, brain_loader.brain)

    def test_get_neurons(self):
        """
        Test to get neurons from the brainLoader
        scenarii:
            - 1/ get a simple neuron from the brainloader
            - 2/ get a neuron with global variables as parameters
        """
        # 1/ get a simple neuron from the brainloader
        st = Settings()
        neuron_list = [{'say': {'message': ['test message']}}]

        neuron = Neuron(name='say', parameters={'message': ['test message']})

        bl = BrainLoader(file_path=self.brain_to_test)
        neurons_from_brain_loader = bl._get_neurons(neuron_list,
                                                    settings=st)

        self.assertEqual([neuron], neurons_from_brain_loader)

        # 2/ get a neuron with global variables as parameters
        neuron_list = [{'say': {'message': ['bonjour {{name}}']}}]
        variables = {
            "author": "Lamonf",
            "test_number": 60,
            "name": "kalliope"
        }
        st = Settings(variables=variables)
        bl = BrainLoader(file_path=self.brain_to_test)
        neurons_from_brain_loader = bl._get_neurons(neuron_list,
                                                    settings=st)

        neuron = Neuron(name='say', parameters={'message': ['bonjour kalliope']})

        self.assertEqual([neuron], neurons_from_brain_loader)

    def test_get_signals(self):
        signals = [{'order': 'test_order'}]

        signal = Order(sentence='test_order')

        bl = BrainLoader(file_path=self.brain_to_test)
        signals_from_brain_loader = bl._get_signals(signals)

        self.assertEqual([signal], signals_from_brain_loader)

    def test_get_event_or_order_from_dict(self):

        order_object = Order(sentence="test_order")
        event_object = Event(hour="7")

        dict_order = {'order': 'test_order'}
        dict_event = {'event': {'hour': '7'}}

        bl = BrainLoader(file_path=self.brain_to_test)
        order_from_bl = bl._get_event_or_order_from_dict(dict_order)
        event_from_bl = bl._get_event_or_order_from_dict(dict_event)

        self.assertEqual(order_from_bl, order_object)
        self.assertEqual(event_from_bl, event_object)

    def test_singleton(self):
        bl1 = BrainLoader(file_path=self.brain_to_test)
        bl2 = BrainLoader(file_path=self.brain_to_test)

        self.assertTrue(bl1.brain is bl2.brain)

    def test_replace_global_variables(self):
        """
        Testing the _replace_global_variables function from the NeuronLauncher.
        Scenarii:
            - 1/ only one global variable
            - 2/ global variable with string after
            - 3/ global variable with int after
            - 4/ multiple global variables
            - 5/ parameter value is a list

        """

        # 1/ only one global variable
        parameters={
            'var1': '{{hello}}'
        }

        variables = {
            "hello": "test",
            "hello2": "test2",
        }
        st = Settings(variables=variables)

        expected_parameters={
            'var1': 'test'
        }

        self.assertEquals(BrainLoader._replace_global_variables(parameters=parameters,
                                                                settings=st),
                          expected_parameters,
                          "Fail to assign a single global variable to parameters")

        # 2/ global variable with string after
        parameters={
            'var1': '{{hello}} Sispheor'
        }
        variables = {
            "hello": "test",
            "hello2": "test2",
        }
        st = Settings(variables=variables)

        expected_parameters = {
            'var1': 'test Sispheor'
        }

        self.assertEquals(BrainLoader._replace_global_variables(parameters=parameters,
                                                                settings=st),
                          expected_parameters,
                          "Fail to assign a global variable with string after to parameters")

        # 3/ global variable with int after
        parameters={
            'var1': '{{hello}}0'
        }
        variables = {
            "hello": 60,
            "hello2": "test2",
        }
        st = Settings(variables=variables)

        expected_parameters={
            'var1': '600'
        }

        self.assertEquals(BrainLoader._replace_global_variables(parameters=parameters,
                                                                settings=st),
                          expected_parameters,
                          "Fail to assign global variable with int after to parameters")

        # 4/ multiple global variables
        parameters={
            'var1': '{{hello}} {{me}}'
        }
        variables = {
            "hello": "hello",
            "me": "LaMonf"
        }
        st = Settings(variables=variables)

        expected_parameters={
            'var1': 'hello LaMonf'
        }

        self.assertEquals(BrainLoader._replace_global_variables(parameters=parameters,
                                                                settings=st),
                          expected_parameters,
                          "Fail to assign multiple global variables to parameters")

        # 5/ parameter value is a list
        parameters={
            'var1': '[hello {{name}}, bonjour {{name}}]'
        }
        variables = {
            "name": "LaMonf",
            "hello2": "test2",
        }
        st = Settings(variables=variables)

        expected_parameters={
            'var1': '[hello LaMonf, bonjour LaMonf]'
        }

        self.assertEquals(BrainLoader._replace_global_variables(parameters=parameters,
                                                                settings=st),
                          expected_parameters,
                          "Fail to assign a single global when parameter value is a list to neuron")

    def test_get_global_variable(self):
        """
        Test the get_global_variable of the OrderAnalyser Class
        """
        sentence = "i am {{name2}}"
        variables = {
            "name": "LaMonf",
            "name2": "kalliope",
        }
        st = Settings(variables=variables)

        expected_result = "i am kalliope"

        self.assertEquals(BrainLoader._get_global_variable(sentence=sentence,
                                                           settings=st),
                          expected_result,
                          "Fail to get the global variable from the sentence")

if __name__ == '__main__':
    unittest.main()
