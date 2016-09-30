#!/usr/bin/env python
import argparse

from core import ShellGui
from core.MainController import MainController
import signal
import sys


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
    parser.add_argument("--synapse", help="SYNAPSE. Name of a synapse to load in quote")
    parser.add_argument("--brain-file", help="BRAIN_PATH_FILE")

    # parse arguments from script parameters
    args = parser.parse_args()
    print args
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit(1)

    if args.action == "start":
        # user set a synapse to start
        if args.synapse is not None:
            print "Playing synapse: %s" % args.synapse

        if args.synapse is None:
            print "Starting JARVIS. Press Ctrl+C for stopping"
            # catch signal for killing on Ctrl+C pressed
            signal.signal(signal.SIGINT, signal_handler)
            # start the main controller
            main_controller = MainController()
            main_controller.start()

    if args.action == "gui":
        ShellGui()

if __name__ == '__main__':
    main()
