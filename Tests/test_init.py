import unittest

import logging

import sys

import mock

from kalliope import parse_args, configure_logging, main


class TestInit(unittest.TestCase):

    def test_parse_args(self):
        # start option
        parser = parse_args(['value'])
        self.assertEqual(parser.action, "value")

        # no option
        with self.assertRaises(SystemExit):
            parse_args([])

        parser = parse_args(['start', '--run-synapse', 'run_synapse'])
        self.assertEqual(parser.run_synapse, 'run_synapse')

        parser = parse_args(['start', '--run-order', 'my order'])
        self.assertEqual(parser.run_order, 'my order')

    def test_configure_logging(self):
        logger = logging.getLogger("kalliope")
        # Level 10 = DEBUG
        configure_logging(debug=True)
        self.assertEqual(logger.getEffectiveLevel(), 10)
        logger.propagate = False

        # Level 20 = INFO
        configure_logging(debug=False)
        self.assertEqual(logger.getEffectiveLevel(), 20)

        # disable after testing
        logger.disabled = True

    def test_main(self):
        # test start kalliope
        sys.argv = ['kalliope.py', 'start']
        with mock.patch('kalliope.core.SignalLauncher.SignalLauncher.launch_signal_class_by_name') \
                as mock_signal_launcher:
            mock_signal_launcher.return_value = None
            main()
            mock_signal_launcher.assert_called()

        # test start gui
        sys.argv = ['kalliope.py', 'gui']
        with mock.patch('kalliope.core.ShellGui.__init__') as mock_shell_gui:
            mock_shell_gui.return_value = None
            main()
            mock_shell_gui.assert_called()

        # test run_synapse
        sys.argv = ['kalliope.py', 'start', '--run-synapse', 'synapse_name']
        with mock.patch('kalliope.core.SynapseLauncher.start_synapse_by_name') as mock_synapse_launcher:
            mock_synapse_launcher.return_value = None
            main()
            mock_synapse_launcher.assert_called()

        # test run order
        sys.argv = ['kalliope.py', 'start', '--run-order', 'my order']
        with mock.patch('kalliope.core.SynapseLauncher.run_matching_synapse_from_order') as mock_synapse_launcher:
            mock_synapse_launcher.return_value = None
            main()
            mock_synapse_launcher.assert_called()

        # action doesn't exist
        sys.argv = ['kalliope.py', 'non_existing_action']
        with self.assertRaises(SystemExit):
            main()

        # install
        sys.argv = ['kalliope.py', 'install', '--git-url', 'https://my_url']
        with mock.patch('kalliope.core.ResourcesManager.install') as mock_resource_manager:
            mock_resource_manager.return_value = None
            main()
            mock_resource_manager.assert_called()

        # install, no URL
        sys.argv = ['kalliope.py', 'install']
        with self.assertRaises(SystemExit):
            main()

        sys.argv = ['kalliope.py', 'install', '--git-url']
        with self.assertRaises(SystemExit):
            main()

        # uninstall
        sys.argv = ['kalliope.py', 'uninstall', '--neuron-name', 'neuron_name']
        with mock.patch('kalliope.core.ResourcesManager.uninstall') as mock_resource_manager:
            mock_resource_manager.return_value = None
            main()
            mock_resource_manager.assert_called()

        sys.argv = ['kalliope.py', 'uninstall']
        with self.assertRaises(SystemExit):
            main()


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestInit("test_main"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
