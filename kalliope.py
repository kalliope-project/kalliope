#!/usr/bin/env python
# coding: utf8
import argparse
import logging

from core import ShellGui
from core import Utils
from core.CrontabManager import CrontabManager
from core.MainController import MainController
import signal
import sys

from core.SynapseLauncher import SynapseLauncher

logging.basicConfig()
logger = logging.getLogger("kalliope")


def signal_handler(signal, frame):
    print "\n"
    Utils.print_info("Ctrl+C pressed. Killing Kalliope")
    sys.exit(0)

ACTION_LIST = ["start", "gui", "load-events"]


def main():
    """
    Entry point of Kalliope program
    """
    # create arguments
    parser = argparse.ArgumentParser(description='Kalliope')
    parser.add_argument("action", help="[start|gui]")
    parser.add_argument("--run-synapse", help="Name of a synapse to load surrounded by quote")
    parser.add_argument("--brain-file", help="Full path of a brain file")
    parser.add_argument("--debug", action='store_true', help="Show debug output")

    # parse arguments from script parameters
    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit(1)

    # check if we want debug
    configure_logging(debug=args.debug)

    logger.debug("jarvis args: %s" % args)

    # by default, no brain file is set. Use the default one: brain.yml in the root path
    brain_file = None

    # check the user provide a valid action
    if args.action not in ACTION_LIST:
        Utils.print_warning("%s is not a recognised action\n" % args.action)
        parser.print_help()

    if args.action == "start":
        # check if user set a brain.yml file
        if args.brain_file:
            brain_file = args.brain_file

        # user set a synapse to start
        if args.run_synapse is not None:
            SynapseLauncher.start_synapse(args.run_synapse, brain_file=brain_file)

        if args.run_synapse is None:
            # first, load events in crontab
            crontab_manager = CrontabManager(brain_file=brain_file)
            crontab_manager.load_events_in_crontab()
            Utils.print_success("Events loaded in crontab")
            # then stat jarvis
            Utils.print_success("Starting JARVIS")
            Utils.print_info("Press Ctrl+C for stopping")
            # catch signal for killing on Ctrl+C pressed
            signal.signal(signal.SIGINT, signal_handler)
            # start the main controller
            MainController(brain_file=brain_file)

    if args.action == "gui":
        ShellGui()


def configure_logging(debug=None):
    """
    Prepare log folder in current home directory
    :param debug: If true, set the lof level to debug
    :return:
    """
    logger = logging.getLogger("kalliope")
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    ch.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.debug("Logger ready")

if __name__ == '__main__':
    main()
