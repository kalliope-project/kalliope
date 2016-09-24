# coding=utf-8
from core import ConfigurationManager
from core.NeuroneLauncher import NeuroneLauncher
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from neurons import Say
from neurons.ansible_tasks.ansible_tasks import Ansible_tasks
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# run command
# order = "playbook"
# order_analyser = OrderAnalyser(order)
# order_analyser.start()

# test ansible
# tasks_file = "tasks.yml"
# ansible_tasks = Ansible_tasks(tasks_file)


# def test_multi_args(*args , **kwargs):
#     if kwargs is not None:
#         for key, value in kwargs.iteritems():
#             print "%s == %s" % (key, value)
#
#
# conf = ConfigurationManager(brain_file_name="test.yml")
#
# brain = conf.brainLoader.get_config()
# print brain
#
#
# for el in brain:
#     print el["neurons"]
#
#     neurons = el["neurons"]
#     for neuron in neurons:
#         NeuroneLauncher().start_neurone(neuron)
#
#
#     # test_multi_args(**el["neurons"][0]["say"])

# test unique message
# Say(message="A vôtre écoute")

# test multiple message
messages = list()
messages.append("Je vous écoute")
messages.append("Oui monsieur?")
messages.append("Que puis-je faire pour vous?")
messages.append("Monsieur?")
messages.append("A vôtre écoute")
messages.append("J'écoute")

Say(message=messages)


