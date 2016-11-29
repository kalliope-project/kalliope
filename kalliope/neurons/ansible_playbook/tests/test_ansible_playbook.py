import os
import unittest
from kalliope.neurons.ansible_playbook import Ansible_playbook
from kalliope.core.NeuronModule import MissingParameterException


class TestAnsible_Playbook(unittest.TestCase):

    def setUp(self):
        self.task_file = "task_file"
        self.random = "random"
        self.test_file = "/tmp/kalliope_text_ansible_playbook.txt"

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

    def test_create_file_via_ansible_playbook(self):
        """
        This test will use an ansible playbook the create a file. We check that the file has been created
        """
        param = {
            "task_file": "kalliope/neurons/ansible_playbook/tests/test_ansible_playbook_neuron.yml"
        }

        Ansible_playbook(**param)

        self.assertTrue(os.path.isfile(self.test_file))

        if os.path.exists(self.test_file):
            os.remove(self.test_file)


if __name__ == '__main__':
    unittest.main()
