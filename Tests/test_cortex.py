import unittest

from kalliope.core.Cortex import Cortex


class TestCortex(unittest.TestCase):

    def setUp(self):
        # cleanup the cortex memory
        Cortex.memory = dict()
        Cortex.temp = dict()

    def test_get_memory(self):
        test_memory = {
            "key1": "value1",
            "key2": "value2"
        }

        Cortex.memory = test_memory
        self.assertDictEqual(test_memory, Cortex.get_memory())

    def test_save(self):
        key_to_save = "key1"
        value_to_save = "value1"

        expected_memory = {
            "key1": "value1"
        }

        Cortex.save(key=key_to_save, value=value_to_save)
        self.assertDictEqual(expected_memory, Cortex.memory)

    def test_get_from_key(self):
        test_memory = {
            "key1": "value1",
            "key2": "value2"
        }

        Cortex.memory = test_memory
        expected_value = "value2"
        self.assertEqual(expected_value, Cortex.get_from_key("key2"))

    def test_add_parameters_from_order(self):

        order_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        expected_temp_dict = {
            "key1": "value1",
            "key2": "value2"
        }

        Cortex.add_parameters_from_order(order_parameters)
        self.assertDictEqual(Cortex.temp, expected_temp_dict)

    def test_clean_parameter_from_order(self):
        Cortex.temp = {
            "key1": "value1",
            "key2": "value2"
        }

        Cortex.clean_parameter_from_order()
        expected_temp_dict = dict()
        self.assertDictEqual(expected_temp_dict, Cortex.memory)

    def test_save_neuron_parameter_in_memory(self):

        # test with a list of parameter with bracket

        neuron1_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        dict_val_to_save = {"my_key_in_memory": "{{key1}}"}

        expected_dict = {"my_key_in_memory": "value1"}

        Cortex.save_neuron_parameter_in_memory(kalliope_memory_dict=dict_val_to_save,
                                               neuron_parameters=neuron1_parameters)

        self.assertDictEqual(expected_dict, Cortex.memory)

        # test with a list of parameter with brackets and string
        self.setUp()  # clean
        neuron1_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        dict_val_to_save = {"my_key_in_memory": "string {{key1}}"}

        expected_dict = {"my_key_in_memory": "string value1"}

        Cortex.save_neuron_parameter_in_memory(kalliope_memory_dict=dict_val_to_save,
                                               neuron_parameters=neuron1_parameters)

        self.assertDictEqual(expected_dict, Cortex.memory)

        # test with a list of parameter with only a string. Neuron parameters are not used
        self.setUp()  # clean
        neuron1_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        dict_val_to_save = {"my_key_in_memory": "string"}

        expected_dict = {"my_key_in_memory": "string"}

        Cortex.save_neuron_parameter_in_memory(kalliope_memory_dict=dict_val_to_save,
                                               neuron_parameters=neuron1_parameters)

        self.assertDictEqual(expected_dict, Cortex.memory)

        # test with an empty list of parameter to save (no kalliope_memory set)
        self.setUp()  # clean

        neuron1_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        dict_val_to_save = None

        Cortex.save_neuron_parameter_in_memory(kalliope_memory_dict=dict_val_to_save,
                                               neuron_parameters=neuron1_parameters)

        self.assertDictEqual(dict(), Cortex.memory)

    def test_save_parameter_from_order_in_memory(self):
        # Test with a value that exist in the temp memory
        order_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        Cortex.temp = order_parameters

        dict_val_to_save = {"my_key_in_memory": "{{key1}}"}

        expected_dict = {"my_key_in_memory": "value1"}

        Cortex.save_parameter_from_order_in_memory(dict_val_to_save)

        self.assertDictEqual(expected_dict, Cortex.memory)

        # test with a value that does not exist
        order_parameters = {
            "key1": "value1",
            "key2": "value2"
        }

        Cortex.temp = order_parameters
        dict_val_to_save = {"my_key_in_memory": "{{key3}}"}

        self.assertFalse(Cortex.save_parameter_from_order_in_memory(dict_val_to_save))

        # save a value with no brackets
        dict_val_to_save = {"my_key_in_memory": "my value"}
        expected_dict = {"my_key_in_memory": "my value"}

        self.assertTrue(Cortex.save_parameter_from_order_in_memory(dict_val_to_save))
        self.assertDictEqual(expected_dict, Cortex.memory)


if __name__ == '__main__':
    unittest.main()
