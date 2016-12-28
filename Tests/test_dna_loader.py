import os
import unittest

from kalliope.core.ConfigurationManager.DnaLoader import DnaLoader
from kalliope.core.Models.Dna import Dna


class TestDnaLoader(unittest.TestCase):

    def setUp(self):
        if "/Tests" in os.getcwd():
            self.dna_test_file = "modules/test_valid_dna.yml"
        else:
            self.dna_test_file = "Tests/modules/test_valid_dna.yml"

    def tearDown(self):
        pass

    def test_get_yaml_config(self):

        expected_result = {'kalliope_supported_version': ['0.4.0'],
                           'author': 'Kalliope project team',
                           'type': 'neuron',
                           'name': 'neuron_test',
                           'tags': ['test']}

        dna_file_content = DnaLoader(self.dna_test_file).get_yaml_config()

        self.assertEqual(dna_file_content, expected_result)

    def test_get_dna(self):

        expected_result = Dna()
        expected_result.name = "neuron_test"
        expected_result.module_type = "neuron"
        expected_result.tags = ['test']
        expected_result.author = 'Kalliope project team'
        expected_result.kalliope_supported_version = ['0.4.0']

        dna_to_test = DnaLoader(self.dna_test_file).get_dna()

        self.assertTrue(dna_to_test.__eq__(expected_result))

    def test_load_dna(self):
        # test with a valid DNA file
        dna_to_test = DnaLoader(self.dna_test_file)._load_dna()

        self.assertTrue(isinstance(dna_to_test, Dna))

        # test with a non valid DNA file
        if "/Tests" in os.getcwd():
            dna_invalid_test_file = "modules/test_invalid_dna.yml"
        else:
            dna_invalid_test_file = "Tests/modules/test_invalid_dna.yml"

        self.assertIsNone(DnaLoader(dna_invalid_test_file)._load_dna())

    def test_check_dna(self):
        # check with valid DNA file
        test_dna = {'kalliope_supported_version': ['0.4.0'],
                    'author': 'Kalliope project team',
                    'type': 'neuron',
                    'name': 'neuron_test',
                    'tags': ['test']}

        self.assertTrue(DnaLoader(file_path=self.dna_test_file)._check_dna_file(test_dna))

        # invalid DNA file, no name
        test_dna = {'kalliope_supported_version': ['0.4.0'],
                    'author': 'Kalliope project team',
                    'type': 'neuron',
                    'tags': ['test']}

        self.assertFalse(DnaLoader(file_path=self.dna_test_file)._check_dna_file(test_dna))

        # invalid DNA file, no type
        test_dna = {'kalliope_supported_version': ['0.4.0'],
                    'author': 'Kalliope project team',
                    'name': 'neuron_test',
                    'tags': ['test']}

        self.assertFalse(DnaLoader(file_path=self.dna_test_file)._check_dna_file(test_dna))

        # invalid DNA, wrong type
        test_dna = {'kalliope_supported_version': ['0.4.0'],
                    'author': 'Kalliope project team',
                    'type': 'doesnotexist',
                    'name': 'neuron_test',
                    'tags': ['test']}

        self.assertFalse(DnaLoader(file_path=self.dna_test_file)._check_dna_file(test_dna))

        # invalid DNA, no kalliope_supported_version
        test_dna = {'author': 'Kalliope project team',
                    'type': 'neuron',
                    'name': 'neuron_test',
                    'tags': ['test']}
        self.assertFalse(DnaLoader(file_path=self.dna_test_file)._check_dna_file(test_dna))

        # invalid DNA, kalliope_supported_version empty
        test_dna = {'kalliope_supported_version': [],
                    'author': 'Kalliope project team',
                    'type': 'neuron',
                    'name': 'neuron_test',
                    'tags': ['test']}

        self.assertFalse(DnaLoader(file_path=self.dna_test_file)._check_dna_file(test_dna))
