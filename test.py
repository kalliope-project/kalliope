# coding=utf-8
from core.OrderAnalyser import OrderAnalyser

oa = OrderAnalyser("sens de la vie", brain_file="brain_examples/fr/say_examples.yml")

oa.start()
