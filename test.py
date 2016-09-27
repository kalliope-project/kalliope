# coding=utf-8
from crontab import CronTab

from core import ConfigurationManager
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
from crontab import CronSlices

class CronManager:

    def __init__(self):
        """
        Manager the crontab to add JAVIS event
        """
        self.my_user_cron = CronTab(user=True)
        # my_user_cron.remove_all()
        self.command = "cat test > /home/nico/Desktop/test.txt"

    def add_event(self, period_string, event_id):

        job = self.my_user_cron.new(command='self.command', comment='JARVIS')
        if CronSlices.is_valid(period_string):
            job.setall(period_string)
            job.enable()
            self.my_user_cron.write()

    def get_jobs(self):
        for job in self.my_user_cron:
                print job

    def _remove_all_jarvis_job(self):
        pass


# test
cron_manager = CronManager()
period_string = "* * 5 5 *"
event_id = 1
cron_manager.add_event(period_string=period_string, event_id=event_id)
