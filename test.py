# coding=utf-8
from core.OrderAnalyser import OrderAnalyser

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# oa = OrderAnalyser("test", brain_file="brain_examples/fr/say_examples.yml")

oa = OrderAnalyser("test", brain_file="brain_examples/fr/fr_systemdate.yml")

oa.start()
