# coding=utf-8
from core import ConfigurationManager
from core.NeuroneLauncher import NeuroneLauncher
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from neurons import Say
from neurons.ansible_tasks.ansible_tasks import Ansible_tasks
import logging

#from core import ShellGui
from jinja2 import Template
import time

hour = time.strftime("%H")
minute = time.strftime("%M")
t = Template("il est {{ hour }} heures et {{ minutes }}!")
uu= t.render(hour=hour, minutes=minute)
print uu