import logging
import threading

import time

from kalliope.core.NeuronModule import MissingParameterException, InvalidParameterException

from kalliope.core import NeuronModule

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TimerThread(threading.Thread):
    def __init__(self, time_to_wait_seconds, callback):
        """
        A Thread that will call the given callback method after waiting time_to_wait_seconds
        :param time_to_wait_seconds: number of second to wait before call the callback method
        :param callback: callback method
        """
        threading.Thread.__init__(self)
        self.time_to_wait_seconds = time_to_wait_seconds
        self.callback = callback

    def run(self):
        # wait the amount of seconds
        logger.debug("[Neuroretarder] wait %s seconds" % self.time_to_wait_seconds)
        time.sleep(self.time_to_wait_seconds)
        # then run the callback method
        self.callback()


class Neurotimer(NeuronModule):
    def __init__(self, **kwargs):
        super(Neurotimer, self).__init__(**kwargs)

        # get parameters
        self.seconds = kwargs.get('seconds', None)
        self.minutes = kwargs.get('minutes', None)
        self.hours = kwargs.get('hours', None)
        self.synapse = kwargs.get('synapse', None)
        self.forwarded_parameter = kwargs.get('forwarded_parameters', None)

        # do some check
        if self._is_parameters_ok():
            # make the sum of all time parameter in seconds
            retarding_time_seconds = self._get_retarding_time_seconds()

            # now wait before running the target synapse
            ds = TimerThread(time_to_wait_seconds=retarding_time_seconds, callback=self.callback_run_synapse)
            # ds.daemon = True
            ds.start()

    def _is_parameters_ok(self):
        """
        Check given neuron parameters are valid
        :return: True if the neuron has been well configured
        """

        # at least one time parameter must be set
        if self.seconds is None and self.minutes is None and self.hours is None:
            raise MissingParameterException("Neuroretarder must have at least one time "
                                            "parameter: seconds, minutes, hours")

        self.seconds = self.get_integer_time_parameter(self.seconds)
        self.minutes = self.get_integer_time_parameter(self.minutes)
        self.hours = self.get_integer_time_parameter(self.hours)
        if self.synapse is None:
            raise MissingParameterException("Neuroretarder must have a synapse name parameter")

        return True

    @staticmethod
    def get_integer_time_parameter(time_parameter):
        """
        Check if a given time parameter is a valid integer:
        - must be > 0
        - if type no an integer, must be convertible to integer

        :param time_parameter: string or integer
        :return: integer
        """
        if time_parameter is not None:
            if not isinstance(time_parameter, int):
                # try to convert into integer
                try:
                    time_parameter = int(time_parameter)
                except ValueError:
                    raise InvalidParameterException("[Neuroretarder] %s is not a valid integer" % time_parameter)
            # check if positive
            if time_parameter < 0:
                raise InvalidParameterException("[Neuroretarder] %s must be > 0" % time_parameter)

        return time_parameter

    def _get_retarding_time_seconds(self):
        """
        Return the sum of given time parameters
        seconds + minutes + hours
        :return: integer, number of total seconds
        """
        returned_time = 0

        if self.seconds is not None:
            returned_time += self.seconds
        if self.minutes is not None:
            returned_time += self.minutes
        if self.hours is not None:
            returned_time += self.hours

        logger.debug("[Neuroretarder] get_retarding_time_seconds: %s" % returned_time)
        return returned_time

    def callback_run_synapse(self):
        """
        Callback method which will be started by the timer thread once the time is over
        :return:
        """
        logger.debug("[Neuroretarder] waiting time is over, start the synapse %s" % self.synapse)

        self.start_synapse_by_name(synapse_name=self.synapse, overriding_parameter_dict=self.forwarded_parameter)
