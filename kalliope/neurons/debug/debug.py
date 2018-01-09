import datetime

from kalliope import Utils
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException


class Debug(NeuronModule):
    def __init__(self, **kwargs):
        super(Debug, self).__init__(**kwargs)
        self.message = kwargs.get('message', None)

        # check if parameters have been provided
        if self._is_parameters_ok():
            Utils.print_warning("[Debug neuron, %s] %s\n" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                             self.message))

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.message is None:
            raise MissingParameterException("You must specify a message string or a list of messages as parameter")
        return True
