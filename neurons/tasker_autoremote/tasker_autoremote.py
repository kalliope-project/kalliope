import logging

import requests

from core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Tasker_autoremote(NeuronModule):
    def __init__(self, **kwargs):
        super(Tasker_autoremote, self).__init__(**kwargs)

        # check if parameters have been provided
        self.key = kwargs.get('key', None)
        self.message = kwargs.get('message', None)

        # check parameters
        if self._is_parameters_ok():
            # create the payload
            data = {'key': self.key,
                    'message': self.message}
            url = "https://autoremotejoaomgcd.appspot.com/sendmessage"
            # post
            r = requests.post(url, data=data)
            logging.debug("Post to tasker automore response: %s" % r.status_code)

    def _is_parameters_ok(self):
        """
            Check if received parameters are ok to perform operations in the neuron
            :return: true if parameters are ok, raise an exception otherwise

            .. raises:: MissingParameterException
        """
        if self.key is None:
            raise MissingParameterException("key parameter required")
        if self.message is None:
            raise MissingParameterException("message parameter required")

        return True