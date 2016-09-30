from crontab import CronTab
from crontab import CronSlices

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.Models import Event
import logging


class InvalidCrontabPeriod(Exception):
    pass

CRONTAB_COMMENT = "JARVIS"


class CrontabManager:

    def __init__(self, brain_file=None):
        self.my_user_cron = CronTab(user=True)
        self.base_command = "/path/to/jarvis/"
        self.brain = BrainLoader(filename=brain_file).get_brain()

    def load_events_in_crontab(self):
        """
        Remove all line in crontab with the CRONTAB_COMMENT
        Then add back line from event in the brain.yml
        :return:
        """
        # clean the current crontab from all jarvis event
        self._remove_all_jarvis_job()
        # load the brain file
        for synapse in self.brain.synapes:
            for signal in synapse.signals:
                # print signal
                # if the signal is an event we add it to the crontab
                if type(signal) == Event:
                    # for all synapse with an event, we add the task id to the crontab
                    self._add_event(period_string=signal.period, event_id=synapse.name)

    def _add_event(self, period_string, event_id):
        my_user_cron = CronTab(user=True)
        job = my_user_cron.new(command=self.base_command+" "+str("\""+ event_id + "\""), comment=CRONTAB_COMMENT)
        if CronSlices.is_valid(period_string):
            job.setall(period_string)
            job.enable()
        else:
            raise InvalidCrontabPeriod("The crontab period %s is not valid" % period_string)
        # write the file
        my_user_cron.write()

    def get_jobs(self):
        return self.my_user_cron.find_comment(CRONTAB_COMMENT)

    def _remove_all_jarvis_job(self):
        """
        Remove all line in crontab that are attached to JARVIS
        :return:
        """
        iter = self.my_user_cron.find_comment(CRONTAB_COMMENT)
        for job in iter:
            logging.debug("remove job %s from crontab" % job)
            self.my_user_cron.remove(job)
        # write the file
        self.my_user_cron.write()

        # this is a fix for the CronTab lib
        # see https://github.com/peak6/python-crontab/issues/1
        new_iter = self.my_user_cron.find_comment(CRONTAB_COMMENT)
        sum_job = sum(1 for _ in new_iter)
        while sum_job > 0:
            self._remove_all_jarvis_job()
