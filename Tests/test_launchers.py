import unittest
import mock

from kalliope.core.Models.Resources import Resources
from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.SynapseLauncher import SynapseLauncher, SynapseNameNotFound
from kalliope.core.TriggerLauncher import TriggerLauncher
from kalliope.core.ConfigurationManager import SettingLoader

from kalliope.core.Models.Trigger import Trigger
from kalliope.core.Models.Neuron import Neuron
from kalliope.core.Models.Order import Order
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.Synapse import Synapse


class TestLaunchers(unittest.TestCase):
    """
    Class to test Launchers Classes (TriggerLauncher, SynapseLauncher, NeuronLauncher) and methods
    """

    def setUp(self):
        pass

    ####
    # Trigger Launcher
    def test_get_trigger(self):
        """
        Test the Trigger Launcher trying to run the trigger
        """
        trigger = Trigger("Trigger", {})
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            TriggerLauncher.get_trigger(trigger=trigger,
                                        callback=None)

            mock_get_class_instantiation.assert_called_once_with(package_name="trigger",
                                                                 module_name=trigger.name,
                                                                 parameters=trigger.parameters)
            mock_get_class_instantiation.reset_mock()

    ####
    # Synapse Launcher
    def test_start_synapse(self):
        """
        Test the Synapse launcher trying to start synapse
        """
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Order(sentence="this is the sentence")
        signal2 = Order(sentence="this is the second sentence")
        signal3 = Order(sentence="that is part of the third sentence")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        synapse3 = Synapse(name="Synapse3", neurons=[neuron2, neuron4], signals=[signal3])

        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        br = Brain(synapses=all_synapse_list)

        sl = SettingLoader()
        r = Resources(neuron_folder="/var/tmp/test/resources")
        sl.settings.resources = r
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            # Success
            SynapseLauncher.start_synapse("Synapse1", brain=br)

            calls = [mock.call(package_name="neurons",
                               module_name=neuron1.name,
                               parameters=neuron1.parameters,
                               resources_dir='/var/tmp/test/resources'),
                     mock.call(package_name="neurons",
                               module_name=neuron2.name,
                               parameters=neuron2.parameters,
                               resources_dir='/var/tmp/test/resources')]
            mock_get_class_instantiation.assert_has_calls(calls=calls)
            mock_get_class_instantiation.reset_mock()

            # Fail
            with self.assertRaises(SynapseNameNotFound):
                SynapseLauncher.start_synapse("Synapse4", brain=br)

    def test_run_synapse(self):
        """
        Test to run a Synapse
        """
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        signal1 = Order(sentence="this is the sentence")
        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse_empty = Synapse(name="Synapse_empty", neurons=[], signals=[signal1])
        sl = SettingLoader()
        resources = Resources(neuron_folder='/var/tmp/test/resources')
        sl.settings.resources = resources
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            SynapseLauncher._run_synapse(synapse=synapse1)

            calls = [mock.call(package_name="neurons",
                               module_name=neuron1.name,
                               parameters=neuron1.parameters,
                               resources_dir="/var/tmp/test/resources"),
                     mock.call(package_name="neurons",
                               module_name=neuron2.name,
                               parameters=neuron2.parameters,
                               resources_dir="/var/tmp/test/resources")]
            mock_get_class_instantiation.assert_has_calls(calls=calls)
            mock_get_class_instantiation.reset_mock()

            # Do not any Neurons
            SynapseLauncher._run_synapse(synapse=synapse_empty)
            mock_get_class_instantiation.assert_not_called()
            mock_get_class_instantiation.reset_mock()

    ####
    # Neurons Launcher
    def test_start_neuron(self):
        """
        Test the Neuron Launcher trying to start a Neuron
        """
        neuron = Neuron(name='neurone1', parameters={'var1': 'val1'})
        sl = SettingLoader()
        resources = Resources(neuron_folder='/var/tmp/test/resources')
        sl.settings.resources = resources
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            NeuronLauncher.start_neuron(neuron=neuron)

            mock_get_class_instantiation.assert_called_once_with(package_name="neurons",
                                                                 module_name=neuron.name,
                                                                 parameters=neuron.parameters,
                                                                 resources_dir=sl.settings.resources.neuron_folder)
            mock_get_class_instantiation.reset_mock()

