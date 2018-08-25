import os
import unittest
from collections import namedtuple

import mock

from kalliope.neurons.ansible_playbook import Ansible_playbook
from kalliope.core.NeuronModule import MissingParameterException


class TestAnsible_Playbook(unittest.TestCase):

    def setUp(self):
        self.task_file = "task_file"
        self.random = "random"
        self.test_file = "/tmp/kalliope_text_ansible_playbook.txt"
        if "/tests" in os.getcwd():
            self.test_tasks_file = os.getcwd() + os.sep + "test_ansible_playbook_neuron.yml"
        else:
            self.test_tasks_file = os.getcwd() + \
                                   os.sep + "kalliope/neurons/ansible_playbook/tests/test_ansible_playbook_neuron.yml"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Ansible_playbook(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing task_file
        parameters = {
            "random": self.random
        }
        run_test(parameters)

        # missing sudo user
        parameters = {
            "sudo": True,
            "random": self.random
        }
        run_test(parameters)

        # missing sudo password
        parameters = {
            "sudo": True,
            "sudo_user": "user"
        }
        run_test(parameters)

        # parameters ok
        parameters = {
            "task_file": self.test_tasks_file,
            "sudo": True,
            "sudo_user": "user",
            "sudo_password": "password"
        }

        with mock.patch("ansible.executor.task_queue_manager.TaskQueueManager.run"):
            instantiated_neuron = Ansible_playbook(**parameters)
            self.assertTrue(instantiated_neuron._is_parameters_ok)

    def test_create_file_via_ansible_playbook(self):
        """
        This test will use an ansible playbook the create a file. We check that the file has been created
        """
        # without sudo
        param = {
            "task_file": self.test_tasks_file
        }

        Ansible_playbook(**param)

        self.assertTrue(os.path.isfile(self.test_file))

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        # with sudo
        param = {
            "task_file": self.test_tasks_file,
            "sudo": True,
            "sudo_user": "user",
            "sudo_password": "password"
        }

        Options = namedtuple('Options',
                             ['connection', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts',
                              'listtasks', 'listtags', 'syntax', 'module_path', 'diff'])

        expected_option = Options(connection='local', forks=100, become=True, become_method="sudo",
                                  become_user="user", check=False, listhosts=False, listtasks=False, listtags=False,
                                  syntax=False, module_path="", diff=False)

        with mock.patch("ansible.executor.task_queue_manager.TaskQueueManager.run") as playbookExecutor:
            instance_neuron = Ansible_playbook(**param)
            playbookExecutor.assert_called_once()

            self.assertEqual(instance_neuron._get_options(), expected_option)


if __name__ == '__main__':
    unittest.main()
