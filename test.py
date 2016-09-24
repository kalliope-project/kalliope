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


order = OrderAnalyser("dis bonjour")

order.start()



