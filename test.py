# coding=utf-8
from core import ConfigurationManager
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.CrontabManager import CrontabManager
from core.Models import Event
from core.NeuroneLauncher import NeuroneLauncher
from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener
from neurons import Say
from neurons.ansible_tasks.ansible_tasks import Ansible_tasks
import logging

from core import ShellGui
from crontab import CronSlices

# oa = OrderAnalyser("dis bonjour", brain_file="test.yml")
#
# oa.start()


cron_manager = CrontabManager(brain_file="test.yml")
cron_manager.load_events_in_crontab()


