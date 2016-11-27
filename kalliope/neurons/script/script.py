import subprocess
import os
import threading

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException


class AsyncShell(threading.Thread):
    """
    Class used to run an asynchronous Shell command

    .. notes:: Impossible to get the success code of the command
    """
    def __init__(self, path):
        self.stdout = None
        self.stderr = None
        self.path = path
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen(self.path,
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()


class Script(NeuronModule):
    def __init__(self, **kwargs):
        super(Script, self).__init__(**kwargs)
        self.path = kwargs.get("path", None)
        # get if the user select a blocking command or not
        self.async = kwargs.get('async', False)

        # check parameters
        if self._is_parameters_ok():
            # run the command
            if not self.async:
                p = subprocess.Popen(self.path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                (output, err) = p.communicate()
                self.output = output
                self.returncode = p.returncode
                message = {
                    "output": self.output,
                    "returncode": self.returncode
                }
                self.say(message)

            else:
                async_shell = AsyncShell(path=self.path)
                async_shell.start()

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException, InvalidParameterException
        """
        if self.path is None:
            raise MissingParameterException("You must provide a script path.")
        if not os.path.isfile(self.path):
            raise InvalidParameterException("Script not found or is not a file.")
        if not os.access(self.path, os.X_OK):
            raise InvalidParameterException("Script not Executable.")

        return True
