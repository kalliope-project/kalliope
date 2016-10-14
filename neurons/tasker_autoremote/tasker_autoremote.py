import logging

import requests

from core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Tasker_autoremote(NeuronModule):
    def __init__(self, **kwargs):
        super(Tasker_autoremote, self).__init__(**kwargs)

        # check if parameters have been provided
        key = kwargs.get('key', None)
        message = kwargs.get('message', None)

        if key is None:
            raise MissingParameterException("key parameter required")

        if message is None:
            raise MissingParameterException("message parameter required")

        # create the payload
        data = {'key': key,
                'message': message}
        url = "https://autoremotejoaomgcd.appspot.com/sendmessage"
        # post
        r = requests.post(url, data=data)
        logging.debug("Post to tasker automore response: %s" % r.status_code)


