import os
import unittest

from kalliope.core.ConfigurationManager.YAMLLoader import YAMLFileNotFound, YAMLLoader


class TestYAMLLoader(unittest.TestCase):
    """
    Class to test YAMLLoader
    """

    def setUp(self):
        pass

    def test_get_config(self):

        valid_file_path_to_test = os.getcwd() + os.sep + "Tests/brains/brain_test.yml"
        invalid_file_path = "brains/non_existing_brain.yml"
        expected_result = [
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

        with self.assertRaises(YAMLFileNotFound):
            YAMLLoader.get_config(invalid_file_path)

        self.assertEqual(YAMLLoader.get_config(valid_file_path_to_test), expected_result)


if __name__ == '__main__':
    unittest.main()
