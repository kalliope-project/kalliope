# coding: utf8
import logging

from core.ConfigurationManager.BrainLoader import BrainLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


brain = BrainLoader.get_brain()

brain2 = BrainLoader.get_brain()
brain3 = BrainLoader.get_brain()
brain4 = BrainLoader.get_brain()


print brain is brain2
print brain is brain3
print brain is brain4
print brain4 is brain2


