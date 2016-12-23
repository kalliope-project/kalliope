import os
import unittest

from mock import mock

from kalliope import ResourcesManager
from kalliope.core.Models import Resources
from kalliope.core.Models.Dna import Dna


class TestResourcesmanager(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_settings_ok(self):
        # -----------------
        # valid resource
        # -----------------
        # valid neuron
        valid_resource = Resources()
        valid_resource.neuron_folder = "/path"
        dna = Dna()
        dna.module_type = "neuron"
        self.assertTrue(ResourcesManager.is_settings_ok(valid_resource, dna))

        # valid stt
        valid_resource = Resources()
        valid_resource.stt_folder = "/path"
        dna = Dna()
        dna.module_type = "stt"
        self.assertTrue(ResourcesManager.is_settings_ok(valid_resource, dna))

        # valid tts
        valid_resource = Resources()
        valid_resource.tts_folder = "/path"
        dna = Dna()
        dna.module_type = "tss"
        self.assertTrue(ResourcesManager.is_settings_ok(valid_resource, dna))

        # valid trigger
        valid_resource = Resources()
        valid_resource.trigger_folder = "/path"
        dna = Dna()
        dna.module_type = "trigger"
        self.assertTrue(ResourcesManager.is_settings_ok(valid_resource, dna))

        # -----------------
        # invalid resource
        # -----------------
        # valid neuron
        valid_resource = Resources()
        valid_resource.neuron_folder = None
        dna = Dna()
        dna.module_type = "neuron"
        self.assertFalse(ResourcesManager.is_settings_ok(valid_resource, dna))

        # valid stt
        valid_resource = Resources()
        valid_resource.stt_folder = None
        dna = Dna()
        dna.module_type = "stt"
        self.assertFalse(ResourcesManager.is_settings_ok(valid_resource, dna))

        # valid tts
        valid_resource = Resources()
        valid_resource.tts_folder = None
        dna = Dna()
        dna.module_type = "tts"
        self.assertFalse(ResourcesManager.is_settings_ok(valid_resource, dna))

        # valid trigger
        valid_resource = Resources()
        valid_resource.trigger_folder = None
        dna = Dna()
        dna.module_type = "trigger"
        self.assertFalse(ResourcesManager.is_settings_ok(valid_resource, dna))

    def test_is_repo_ok(self):
        # valid repo
        if "/Tests" in os.getcwd():
            dna_file_path = "modules/dna.yml"
            install_file_path = "modules/install.yml"
        else:
            dna_file_path = "Tests/modules/dna.yml"
            install_file_path = "Tests/modules/install.yml"
        self.assertTrue(ResourcesManager.is_repo_ok(dna_file_path=dna_file_path, install_file_path=install_file_path))

        # missing dna
        if "/Tests" in os.getcwd():
            dna_file_path = ""
            install_file_path = "modules/install.yml"
        else:
            dna_file_path = "T"
            install_file_path = "Tests/modules/install.yml"
        self.assertFalse(ResourcesManager.is_repo_ok(dna_file_path=dna_file_path, install_file_path=install_file_path))

        # missing install
        if "/Tests" in os.getcwd():
            dna_file_path = "modules/dna.yml"
            install_file_path = ""
        else:
            dna_file_path = "Tests/modules/dna.yml"
            install_file_path = ""
        self.assertFalse(ResourcesManager.is_repo_ok(dna_file_path=dna_file_path, install_file_path=install_file_path))

    def test_get_target_folder(self):
        # test get neuron folder
        resources = Resources()
        resources.neuron_folder = '/var/tmp/test/resources'
        self.assertEqual(ResourcesManager._get_target_folder(resources, "neuron"), "/var/tmp/test/resources")

        # test get stt folder
        resources = Resources()
        resources.stt_folder = '/var/tmp/test/resources'
        self.assertEqual(ResourcesManager._get_target_folder(resources, "stt"), "/var/tmp/test/resources")

        # test get tts folder
        resources = Resources()
        resources.tts_folder = '/var/tmp/test/resources'
        self.assertEqual(ResourcesManager._get_target_folder(resources, "tts"), "/var/tmp/test/resources")

        # test get trigger folder
        resources = Resources()
        resources.trigger_folder = '/var/tmp/test/resources'
        self.assertEqual(ResourcesManager._get_target_folder(resources, "trigger"), "/var/tmp/test/resources")

        # test get non existing resource
        resources = Resources()
        self.assertIsNone(ResourcesManager._get_target_folder(resources, "not_existing"))

    def test_check_supported_version(self):
        # version ok
        current_version = '0.4.0'
        supported_version = ['0.4.0', '0.3.0', '0.2.0']

        self.assertTrue(ResourcesManager._check_supported_version(current_version=current_version,
                                                                  supported_versions=supported_version))

        # version non ok, useer does not confir
        current_version = '0.4.0'
        supported_version = ['0.3.0', '0.2.0']

        with mock.patch('kalliope.Utils.query_yes_no', return_value=True):
            self.assertTrue(ResourcesManager._check_supported_version(current_version=current_version,
                                                                      supported_versions=supported_version))

        with mock.patch('kalliope.Utils.query_yes_no', return_value=False):
            self.assertFalse(ResourcesManager._check_supported_version(current_version=current_version,
                                                                       supported_versions=supported_version))
