import logging
import subprocess
import threading
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class AsyncShell(threading.Thread):
    """
    Class used to run an asynchrone Shell command

    .. notes:: Impossible to get the success code of the command
    """
    def __init__(self, cmd):
        self.stdout = None
        self.stderr = None
        self.cmd = cmd
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen(self.cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()


class Shell(NeuronModule):
    """
    Run a shell command in a synchron mode
    """
    def __init__(self, **kwargs):
        super(Shell, self).__init__(**kwargs)

        # get the command
        self.cmd = kwargs.get('cmd', None)
        # get if the user select a blocking command or not
        self.async = kwargs.get('async', False)
        self.query = kwargs.get('query', None)

        if self.query is not None:
            self.cmd = self.cmd + "\"" + self.query +"\""

        # check parameters
        if self._is_parameters_ok():
            # run the command
            if not self.async:
                p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
                self.output = output
                self.returncode = p.returncode
                message = {
                    "output": self.output,
                    "returncode": self.returncode
                }
                self.say(message)

            else:
                async_shell = AsyncShell(cmd=self.cmd)
                async_shell.start()

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.cmd is None:
            raise MissingParameterException("cmd parameter required")

        return True
