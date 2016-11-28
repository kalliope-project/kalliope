# coding: utf8

import locale
import logging
import signal
import sys

from dialog import Dialog

from kalliope.core import OrderListener
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core.Utils.Utils import Utils
from kalliope.neurons.say.say import Say

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

signal.signal(signal.SIGINT, signal_handler)


class ShellGui:
    def __init__(self, brain=None):
        """
        Load a GUI in a shell console for testing TTS, STT and brain configuration
        :param brain: The Brain object provided by the brain.yml
        :type brain: Brain

        .. seealso:: Brain
        """
        # override brain
        self.brain = brain

        # get settings
        sl = SettingLoader()
        self.settings = sl.settings
        locale.setlocale(locale.LC_ALL, '')

        self.d = Dialog(dialog="dialog")

        self.d.set_background_title("Kalliope shell UI")

        self.show_main_menu()

    def show_main_menu(self):
        """
        Main menu of the shell UI.
        Provide a list of action the user can select to test his settings
        """

        code, tag = self.d.menu("Test your Kalliope settings from this menu",
                                choices=[("TTS", "Text to Speech"),
                                         ("STT", "Speech to text"),
                                         ("Synapses", "Run a synapse")])

        if code == self.d.OK:
            if tag == "STT":
                self.show_stt_test_menu()
            if tag == "TTS":
                self.show_tts_test_menu()
            if tag == "Synapses":
                self.show_synapses_test_menu()

    def show_stt_test_menu(self):
        """
        Show the list of available STT.
        Clicking on a STT will load the engine to catch the user audio and return a text
        """
        # we get STT from settings
        stt_list = self.settings.stts
        logger.debug("Loaded stt list: %s" % str(stt_list))
        choices = self._get_choices_tuple_from_list(stt_list)

        code, tag = self.d.menu("Select the STT to test:",
                                choices=choices)

        # go back to the main menu if we choose "cancel"
        if code == self.d.CANCEL:
            self.show_main_menu()

        # if ok, call the target TTS engine and catch audio
        if code == self.d.OK:
            self.d.infobox("Please talk now")
            # the callback funtion will print the translated audio into text on the screen
            order_listener = OrderListener(callback=self.callback_stt, stt=str(tag))
            order_listener.load_stt_plugin()

    def show_tts_test_menu(self, sentence_to_test=None):
        """
        A menu for testing text to speech
        - select a TTS engine to test
        - type a sentence
        - press ok and listen the generated audio from the typed text
        :param sentence_to_test: the screen written sentence to test
        """
        continue_bool = True
        # if we don't have yet a sentence to test, we ask the user to type one
        if sentence_to_test is None:
            # First, we ask the user to type a sentence that will be passed in the TTS
            code, sentence_to_test = self.d.inputbox("Please type the sentence you want to test", height=20, width=50)

            if code == self.d.CANCEL:
                self.show_main_menu()
                continue_bool = False
            if code == self.d.OK:
                continue_bool = True

        if continue_bool:
            # we get TTS from settings
            tts_list = self.settings.ttss

            # create a list of tuple that can be used by the dialog menu
            choices = self._get_choices_tuple_from_list(tts_list)

            code, tag = self.d.menu("Sentence to test: %s" % sentence_to_test,
                                    choices=choices)

            if code == self.d.CANCEL:
                self.show_tts_test_menu()
            if code == self.d.OK:
                self._run_tts_test(tag, sentence_to_test)
                # then go back to this menu with the same sentence
                # if the user want to test the same text with another TTS
                self.show_tts_test_menu(sentence_to_test=sentence_to_test)

    @staticmethod
    def _run_tts_test(tts_name, sentence_to_test):
        """
        Call the TTS
        :param tts_name: Name of the TTS module to launch
        :param sentence_to_test: String text to send to the TTS engine
        """
        sentence_to_test = sentence_to_test.encode('utf-8')
        tts_name = tts_name.encode('utf-8')

        Say(message=sentence_to_test, tts=tts_name)

    @staticmethod
    def _get_choices_tuple_from_list(list_to_convert):
        """
            Return a list of tup that can be used in Dialog menu
            :param list_to_convert: List of object to convert into tuple
            :return: List of choices
            :rtype: List
        """
        # create a list of tuple that can be used by the dialog menu
        choices = list()
        for el in list_to_convert:
            tup = (str(el.name), str(el.parameters))
            choices.append(tup)
            logger.debug("Add el to the list: %s with parameters: %s" % (str(el.name), str(el.parameters)))
        return choices

    def callback_stt(self, audio):
        """
        Callback function called after the STT has finish his job
        Print the text of what the STT engine think we said on the screen
        :param audio: Text from the translated audio
        """
        code = self.d.msgbox("The STT engine think you said:\n %s" % audio, width=50)

        if code == self.d.OK:
            self.show_stt_test_menu()

    def show_synapses_test_menu(self):
        """
        Show a list of available synapse in the brain to run it directly
        """

        # create a tuple for the list menu
        choices = list()
        x = 0
        for el in self.brain.synapses:
            tup = (str(el.name), str(x))
            choices.append(tup)
            x += 1

        code, tag = self.d.menu("Select a synapse to run",
                                choices=choices)

        if code == self.d.CANCEL:
            self.show_main_menu()
        if code == self.d.OK:
            logger.debug("Run synapse from GUI: %s" % tag)
            SynapseLauncher.start_synapse(tag, brain=self.brain)
            self.show_synapses_test_menu()
