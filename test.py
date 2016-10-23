# coding: utf8
import logging

from core import OrderAnalyser
from core import Utils
from core.ConfigurationManager import SettingLoader
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.Players import Mplayer

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

# order = "quelle heure est-il"
# oa = OrderAnalyser(order=order)
# oa.start()



brain = BrainLoader.get_brain()

order = "bonjour"

oa = OrderAnalyser(order=order, brain=brain)

oa.start()


# settings = SettingLoader.get_settings()
#
# tts_name_to_use = "pico2wave"
# sentence_to_say = "bonjour monsieur, je m'appelle Kalliopé"
#
#
# def _get_tts_object_from_name(tts_name_to_use):
#     """
#     Return a Tts object from the nae of the Tss. Get parameters in settings
#     :param tts_name_to_use:
#     :return:
#     """
#     return next((x for x in settings.ttss if x.name == tts_name_to_use), None)
#
#
# # create a tts object from the tts the user want to user
# tts_object = _get_tts_object_from_name(tts_name_to_use)
#
# if tts_object is None:
#     print "TTS module name %s not found in settings" % tts_name_to_use
#
# else:
#     tts_module_instance = Utils.get_dynamic_class_instantiation("tts", tts_object.name.capitalize(), tts_object.parameters)
#     tts_module_instance.say(sentence_to_say)




