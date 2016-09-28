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
from crontab import CronSlices, CronTab

oa = OrderAnalyser("sens de la vie", brain_file="brain_examples/fr/say_examples.yml")

oa.start()

#
# cron_manager = CrontabManager(brain_file="test.yml")
# cron_manager.load_events_in_crontab()

# command = "/path/to/my/command"
# comment = "JARVIS"
# period_string = "* * 5 5 *"
#
# my_user_cron = CronTab(user=True)
#
# for x in range(0, 5, 1):
#     job = my_user_cron.new(command=command, comment=comment)
#     if CronSlices.is_valid(period_string):
#         job.setall(period_string)
#         job.enable()
#     my_user_cron.write()

# # here we have:
# # * * 5 5 * /path/to/my/command # SAMECOMMENT
# # * * 5 5 * /path/to/my/command # SAMECOMMENT
# # * * 5 5 * /path/to/my/command # SAMECOMMENT
#
# iter = my_user_cron.find_comment(comment)
# for job in iter:
#     print "remove job %s" % job
#     my_user_cron.remove(job)
# my_user_cron.write()
#
# # now we check the content
# new_iter = my_user_cron.find_comment(comment)
# # for job in iter:
# #     print "Still a job: %s" % job
# vsum_job = sum(1 for _ in new_iter)
# print vsum_job
#
# # output
# # remove job * * 5 5 * /path/to/my/command # SAMECOMMENT
# # remove job * * 5 5 * /path/to/my/command # SAMECOMMENT
# # Still a job: * * 5 5 * /path/to/my/command # SAMECOMMENT