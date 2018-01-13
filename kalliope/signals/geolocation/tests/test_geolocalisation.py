import unittest

from kalliope.core.SignalModule import MissingParameter

from kalliope.core.Models import Brain
from kalliope.core.Models import Neuron
from kalliope.core.Models import Synapse
from kalliope.core.Models.Signal import Signal

from kalliope.signals.geolocation.geolocation import Geolocation


class Test_Geolocation(unittest.TestCase):
    def test_check_geolocation_valid(self):
        expected_parameters = ["latitude", "longitude", "radius"]
        self.assertTrue(Geolocation.check_parameters(expected_parameters))

    def test_check_geolocation_valid_with_other(self):
        expected_parameters = ["latitude", "longitude", "radius", "kalliope", "random"]
        self.assertTrue(Geolocation.check_parameters(expected_parameters))

    def test_check_geolocation_no_radius(self):
        expected_parameters = ["latitude", "longitude", "kalliope", "random"]
        self.assertFalse(Geolocation.check_parameters(expected_parameters))

    def test_check_geolocation_no_latitude(self):
        expected_parameters = ["longitude", "radius", "kalliope", "random"]
        self.assertFalse(Geolocation.check_parameters(expected_parameters))

    def test_check_geolocation_no_longitude(self):
        expected_parameters = ["latitude", "radius", "kalliope", "random"]
        self.assertFalse(Geolocation.check_parameters(expected_parameters))

    def test_get_list_synapse_with_geolocation(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        fake_geolocation_parameters = {
            "latitude": 66,
            "longitude": 66,
            "radius": 66,
        }
        signal1 = Signal(name="geolocation", parameters=fake_geolocation_parameters)
        signal2 = Signal(name="order", parameters="this is the second sentence")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])

        synapses_list = [synapse1, synapse2]
        br = Brain(synapses=synapses_list)

        expected_list = [synapse1]

        # Stubbing the Geolocation Signal with the brain
        geo = Geolocation()
        geo.brain = br
        geo.run()

        self.assertEqual(expected_list, geo.list_synapses_with_geolocalion)

    def test_get_list_synapse_with_raise_missing_parameters(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        fake_geolocation_parameters = {
            "longitude": 66,
            "radius": 66,
        }
        signal1 = Signal(name="geolocation", parameters=fake_geolocation_parameters)
        signal2 = Signal(name="order", parameters="this is the second sentence")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])

        synapses_list = [synapse1, synapse2]
        br = Brain(synapses=synapses_list)

        # Stubbing the Geolocation Signal with the brain
        geo = Geolocation()
        geo.brain = br

        with self.assertRaises(MissingParameter):
            geo.run()


if __name__ == '__main__':
    unittest.main()
