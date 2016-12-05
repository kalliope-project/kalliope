from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core import Utils
from kalliope.core.Models import Event


class EventManager(object):

    def __init__(self, synapses):
        Utils.print_info('Starting event manager')
        self.scheduler = BackgroundScheduler()
        self.synapses = synapses
        self.load_events()
        self.scheduler.start()

    def load_events(self):
        """
        For each received synapse that have an event as signal, we add a new job scheduled
        to launch the synapse
        :return:
        """
        for synapse in self.synapses:
            for signal in synapse.signals:
                # if the signal is an event we add it to the task list
                if type(signal) == Event:
                    my_cron = CronTrigger(year=signal.year,
                                          month=signal.month,
                                          day=signal.day,
                                          week=signal.week,
                                          day_of_week=signal.day_of_week,
                                          hour=signal.hour,
                                          minute=signal.minute,
                                          second=signal.second)
                    Utils.print_info("Add synapse name \"%s\" to the scheduler: %s" % (synapse.name, my_cron))
                    self.scheduler.add_job(self.run_synapse_by_name, my_cron, args=[synapse.name])

    @staticmethod
    def run_synapse_by_name(synapse_name):
        """
        This method will run the synapse
        """
        Utils.print_info("Event triggered, running synapse: %s" % synapse_name)
        # get a brain
        brain_loader = BrainLoader()
        brain = brain_loader.brain
        SynapseLauncher.start_synapse(synapse_name, brain=brain)
