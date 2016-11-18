import time

from kalliope.core.NeuronModule import NeuronModule,  MissingParameterException


class Sleep(NeuronModule):
    def __init__(self, **kwargs):
        super(Sleep, self).__init__(**kwargs)
        self.seconds = kwargs.get('seconds', None)

        # check parameters
        if self._is_parameters_ok():
            time.sleep(self.seconds)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.seconds is None:
            raise MissingParameterException("You must set a number of seconds as parameter")
