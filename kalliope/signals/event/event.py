from threading import Thread

from kalliope.core import SignalModule, MissingParameter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core import Utils


class Event(SignalModule, Thread):
    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)
        Thread.__init__(self, name=Event)
        Utils.print_info('[Event] Starting manager')
        self.scheduler = BackgroundScheduler()
        self.list_synapses_with_event = list(super(Event, self).get_list_synapse())
        self.load_events()

    def run(self):
        self.scheduler.start()

    def load_events(self):
        """
        For each received synapse that have an event as signal, we add a new job scheduled
        to launch the synapse
        """
        for synapse in self.list_synapses_with_event:
            for signal in synapse.signals:
                # We need to loop here again if the synapse has multiple event signals.
                # if the signal is an event we add it to the task list.
                if signal.name == "event":
                    my_cron = CronTrigger(year=self.get_parameter_from_dict("year", signal.parameters),
                                          month=self.get_parameter_from_dict("month", signal.parameters),
                                          day=self.get_parameter_from_dict("day", signal.parameters),
                                          week=self.get_parameter_from_dict("week", signal.parameters),
                                          day_of_week=self.get_parameter_from_dict("day_of_week",
                                                                                   signal.parameters),
                                          hour=self.get_parameter_from_dict("hour", signal.parameters),
                                          minute=self.get_parameter_from_dict("minute", signal.parameters),
                                          second=self.get_parameter_from_dict("second", signal.parameters), )
                    Utils.print_info("Add synapse name \"%s\" to the scheduler: %s" % (synapse.name, my_cron))
                    self.scheduler.add_job(self.run_synapse_by_name, my_cron, args=[synapse.name])

    @staticmethod
    def run_synapse_by_name(synapse_name):
        """
        This method will run the synapse
        """
        Utils.print_info("[Event] triggered, running synapse: %s" % synapse_name)
        # get a brain
        brain_loader = BrainLoader()
        brain = brain_loader.brain
        SynapseLauncher.start_synapse_by_list_name([synapse_name], brain=brain)

    @staticmethod
    def get_parameter_from_dict(parameter_name, parameters_dict):
        """
        return the value in the dict parameters_dict frm the key parameter_name
        return None if the key does not exist
        :param parameter_name: name of the key
        :param parameters_dict: dict
        :return: string
        """
        try:
            return parameters_dict[parameter_name]
        except KeyError:
            return None

    @staticmethod
    def check_parameters(parameters):
        """
        Check received event dictionary of parameter is valid:

        :param event_dict: The event Dictionary
        :type event_dict: Dict
        :return: True if event are ok
        :rtype: Boolean
        """

        def get_key(key_name):
            try:
                return parameters[key_name]
            except KeyError:
                return None

        if parameters is None or parameters == "":
            raise MissingParameter("Event must contain at least one of those elements: "
                                "year, month, day, week, day_of_week, hour, minute, second")

        # check content as at least on key
        year = get_key("year")
        month = get_key("month")
        day = get_key("day")
        week = get_key("week")
        day_of_week = get_key("day_of_week")
        hour = get_key("hour")
        minute = get_key("minute")
        second = get_key("second")

        list_to_check = [year, month, day, week, day_of_week, hour, minute, second]
        number_of_none_object = list_to_check.count(None)
        list_size = len(list_to_check)
        if number_of_none_object >= list_size:
            raise MissingParameter("Event must contain at least one of those elements: "
                                "year, month, day, week, day_of_week, hour, minute, second")

        return True
