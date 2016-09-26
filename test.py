# coding=utf-8
from core import ConfigurationManager
from core.NeuroneLauncher import NeuroneLauncher
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from neurons import Say
from neurons.ansible_tasks.ansible_tasks import Ansible_tasks
import logging

from core import ShellGui

Say(message="bonjour", tts="pico2wave")
