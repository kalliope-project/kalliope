import subprocess
import os

from core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException


class Script(NeuronModule):
    def __init__(self, **kwargs):
        super(Script, self).__init__(**kwargs)
        self.path = kwargs.get("path", None)

        # check parameters
        if self._is_parameters_ok():
            p = subprocess.Popen(self.path, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        """
        if self.path is None:
            raise MissingParameterException("You must provide a script path.")
        if not os.path.isfile(self.path):
            raise InvalidParameterException("Script not found or is not a file.")
        if not os.access(self.path, os.X_OK):
            raise InvalidParameterException("Script not Executable.")

        return True
