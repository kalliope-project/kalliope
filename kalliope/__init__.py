#!/usr/bin/env python
# coding: utf8
import argparse
import logging

from kalliope.core import ShellGui
from kalliope.core import Utils
from kalliope.core.ConfigurationManager.BrainLoader import BrainLoader
from kalliope.core.EventManager import EventManager
from kalliope.core.MainController import MainController

from _version import version_str
import signal
import sys

from kalliope.core.ResourcesManager import ResourcesManager
from kalliope.core.SynapseLauncher import SynapseLauncher

logging.basicConfig()
logger = logging.getLogger("kalliope")


def signal_handler(signal, frame):
    """
    Used to catch a keyboard signal like Ctrl+C in order to kill the kalliope program
    :param signal: signal handler
    :param frame: execution frame
    """
    print "\n"
    Utils.print_info("Ctrl+C pressed. Killing Kalliope")
    sys.exit(0)

# actions available
ACTION_LIST = ["start", "gui", "install"]


def main():
    """
    Entry point of Kalliope program
    """
    # create arguments
    parser = argparse.ArgumentParser(description='Kalliope')
    parser.add_argument("action", help="[start|gui|install]")
    parser.add_argument("--run-synapse", help="Name of a synapse to load surrounded by quote")
    parser.add_argument("--brain-file", help="Full path of a brain file")
    parser.add_argument("--debug", action='store_true', help="Show debug output")
    parser.add_argument("--git-url", help="Git URL of the neuron to install")
    parser.add_argument('-v', '--version', action='version', version='Kalliope ' + version_str)

    # parse arguments from script parameters
    args = parser.parse_args()

    # require at least one parameter, the action
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit(1)

    # check if we want debug
    configure_logging(debug=args.debug)

    logger.debug("kalliope args: %s" % args)

    # by default, no brain file is set. Use the default one: brain.yml in the root path
    brain_file = None
    # check if user set a brain.yml file
    if args.brain_file:
        brain_file = args.brain_file
    # load the brain once
    brain_loader = BrainLoader(file_path=brain_file)
    brain = brain_loader.brain

    # check the user provide a valid action
    if args.action not in ACTION_LIST:
        Utils.print_warning("%s is not a recognised action\n" % args.action)
        parser.print_help()

    if args.action == "start":
        # user set a synapse to start
        if args.run_synapse is not None:
            SynapseLauncher.start_synapse(args.run_synapse, brain=brain)

        if args.run_synapse is None:
            # first, load events in event manager
            EventManager(brain.synapses)
            Utils.print_success("Events loaded")
            # then start kalliope
            Utils.print_success("Starting Kalliope")
            Utils.print_info("Press Ctrl+C for stopping")
            # catch signal for killing on Ctrl+C pressed
            signal.signal(signal.SIGINT, signal_handler)
            # start the main controller
            MainController(brain=brain)

    if args.action == "gui":
        ShellGui(brain=brain)

    if args.action == "install":
        if not args.git_url:
            Utils.print_danger("You must specify the git url")
        else:
            parameters = {
                "git_url": args.git_url
            }
            res_manager = ResourcesManager(**parameters)
            res_manager.install()


def configure_logging(debug=None):
    """
    Prepare log folder in current home directory
    :param debug: If true, set the lof level to debug
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
