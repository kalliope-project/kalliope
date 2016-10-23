# coding: utf8
import logging

from core.Players import Mplayer

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

# order = "quelle heure est-il"
# oa = OrderAnalyser(order=order)
# oa.start()

# SettingLoader.get_settings()
#
# brain = BrainLoader.get_brain()
#
# order = "bonjour2"
#
# oa = OrderAnalyser(order=order, brain=brain)
#
# oa.start()


file_path = "/tmp/kalliope/tts/Acapela/sonid15/Manon.378f97b9ae266e30898396f4c4f7e159.tts"


player = Mplayer()
player.play(file_path)








