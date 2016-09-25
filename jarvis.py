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
    parser.add_argument("--start", action='store_true', help="Start Jarvis in the current shell")
    parser.add_argument("--gui", action='store_true', help="Run Jarvis with shell GUI to test components")

    # parse arguments from script parameters
    args = parser.parse_args()
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit(1)

    if args.start:
        print "Starting JARVIS. Press Ctrl+C for stopping"
        # catch signal for killing on Ctrl+C pressed
        signal.signal(signal.SIGINT, signal_handler)
        # start the main controller
        main_controller = MainController()
        main_controller.start()

    if args.gui:
        ShellGui()

if __name__ == '__main__':
    main()
