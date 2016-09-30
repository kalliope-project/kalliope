#!/usr/bin/env python
import argparse

from core import ShellGui
from core.MainController import MainController
import signal
import sys

from core.SynapseLauncher import SynapseLauncher


def signal_handler(signal, frame):
        print "\n"
        print('Ctrl+C pressed. Killing Jarvis')
        sys.exit(0)


def main():
    """
    Entry point of jarvis program
    """
    # create arguments
    parser = argparse.ArgumentParser(description='JARVIS')
    parser.add_argument("action", help="[start|gui]")
    parser.add_argument("--run-synapse", help="SYNAPSE. Name of a synapse to load surrounded by quote")
    parser.add_argument("--brain-file", help="BRAIN_PATH_FILE")

    # parse arguments from script parameters
    args = parser.parse_args()
    print args
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit(1)

    # by default, no brain file is set. Use the default one: brain.yml in the root path
    brain_file = None

    if args.action == "start":
        # check if user set a brain.yml file
        if args.brain_file:
            print "Brain file arg: %s" % args.brain_file
            brain_file = args.brain_file

        # user set a synapse to start
        if args.run_synapse is not None:
            print "Run synapse arg: %s" % args.run_synapse
            SynapseLauncher.start_synapse(args.run_synapse, brain_file=brain_file)

        if args.run_synapse is None:
            print "Starting JARVIS. Press Ctrl+C for stopping"
            # catch signal for killing on Ctrl+C pressed
            signal.signal(signal.SIGINT, signal_handler)
            # start the main controller
            main_controller = MainController(brain_file=brain_file)
            main_controller.start()

    if args.action == "gui":
        ShellGui()

if __name__ == '__main__':
    main()
