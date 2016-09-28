# coding=utf-8
from core import ConfigurationManager
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.CrontabManager import CrontabManager
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

# test
# cron_manager = CrontabManager()
# cron_manager.load_events_in_crontab()

class NoEventsFound(Exception):
    pass

class NoIdInEvent(Exception):
    pass

class NoPeriodInEvent(Exception):
    pass

# events = BrainLoader(filename="test.yml").get_events()
#
# # check there is some event in the brain file
# if len(events) <= 0:
#     raise NoEventsFound("There is no events in the brain file")
#
# # we must check that each event has an id and a period
# for event in events:
#     if "id" not in event:
#         raise NoIdInEvent("No id found event must has an unique id")
#     if "period" not in event:
#         raise NoPeriodInEvent("An event must has a period")

brain = BrainLoader(filename="test.yml").get_brain()

