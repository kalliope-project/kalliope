from crontab import CronTab
from crontab import CronSlices


class InvalidCrontabPeriod(Exception):
    pass

CRONTAB_COMMENT = "JARVIS"


class CrontabManager:

    def __init__(self, brain_file=None):
        self.my_user_cron = CronTab(user=True)
        self.base_command = "/usr/bin/echo"

    def load_events_in_crontab(self):
        # clean the current crontab from all jarvis event
        self._remove_all_jarvis_job()
        # # load the brain file
        period_string = "* * 5 5 *"
        event_id = 1
        # for all tasks with an event, we add the task id to the crontab
        self._add_event(period_string=period_string, event_id=event_id)

    def _add_event(self, period_string, event_id):
        my_user_cron = CronTab(user=True)
        job = my_user_cron.new(command=self.base_command, comment=CRONTAB_COMMENT)
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
            self.my_user_cron.remove(job)
        # write the file
        self.my_user_cron.write()