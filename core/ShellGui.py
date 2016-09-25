from dialog import Dialog
import locale

from core import ConfigurationManager
from neurons import Say


class ShellGui:
    def __init__(self):
        # get settings
        self.conf = ConfigurationManager().get_settings()
        locale.setlocale(locale.LC_ALL, '')

        self.d = Dialog(dialog="dialog")

        self.d.set_background_title("Jarvis shell UI")

        self.show_main_menu()

    def show_main_menu(self):
        """
        Main menu of the shell UI.
        Provide a list of action the user can select to test his settings
        :return:
        """

        code, tag = self.d.menu("Test your JARVIS settings from this menu",
                                choices=[("TTS", "Text to Speech"),
                                         ("STT", "Speech to text")])

        if code == self.d.OK:
            if tag == "STT":
                self.show_stt_test_menu()
            if tag == "TTS":
                self.show_tts_test_menu()

    def show_stt_test_menu(self):
        pass

    def show_tts_test_menu(self, sentence_to_test=None):
        """
         A menu for testing text to speech
        :return:
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
            tts_list = ConfigurationManager.get_tts_list()

            # create a list of tuple that can be used by the dialog menu
            choices = list()
            for tts in tts_list:
                for name, settings in tts.iteritems():
                    print name
                    print settings
                    tup = (str(name), str(settings))
                    choices.append(tup)

            code, tag = self.d.menu("Sentence to test: %s" % sentence_to_test,
                                    choices=choices)

            if code == self.d.CANCEL:
                self.show_tts_test_menu()
            if code == self.d.OK:
                self._run_tts_test(tag, sentence_to_test)
                # then go back to this menu with the same sentence
                self.show_tts_test_menu(sentence_to_test=sentence_to_test)

    def _run_tts_test(self, tag, sentence_to_test):
        """
        Call the TTS
        :param tag:
        :param sentence_to_test:
        :return:
        """
        Say(message=sentence_to_test, tts=tag)

