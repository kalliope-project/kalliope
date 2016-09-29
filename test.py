# coding=utf-8
from core.OrderAnalyser import OrderAnalyser

oa = OrderAnalyser("test 2", brain_file="brain_examples/fr/fr_systemdate.yml")

oa.start()
