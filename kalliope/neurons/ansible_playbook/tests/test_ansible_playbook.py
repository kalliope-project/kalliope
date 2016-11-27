import unittest

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.ansible_playbook.ansible_playbook import Ansible_playbook


class TestAnsible_Playbook(unittest.TestCase):

    def setUp(self):
        self.task_file="task_file"
        self.random = "random"

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


if __name__ == '__main__':
    unittest.main()

