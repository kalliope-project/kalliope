import json
import logging

import requests

from core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Uri(NeuronModule):

    def __init__(self, **kwargs):
        super(Uri, self).__init__(**kwargs)

        # input variables
        self.url = kwargs.get('url', None)
        self.headers = kwargs.get('headers', None)
        self.data = kwargs.get('data', None)
        self.method = kwargs.get('method', "GET")
        self.user = kwargs.get('user', None)
        self.password = kwargs.get('password', None)
        self.timeout = kwargs.get('timeout', None)

        # processing parameters
        self.parameters = None

        # output variable
        self.status_code = None
        self.content = None
        self.response_header = None

        # this is a switch case option
        switch_case = {
            "GET": self.do_get,
            "POST": self.do_post,
            "DELETE": self.do_delete,
            "PUT": self.do_put,
            "HEAD": self.do_head,
            "PATCH": self.do_patch,
            "OPTIONS": self.do_options
        }

        # check parameters
        if self._is_parameters_ok():
            # we get parameters that will be passed to the requests lib
            self.parameters = self.get_parameters()
            # we call the right method depending of the method selected
            switch_case[self.method]()

            message = {
                "status_code": self.status_code,
                "content": self.content,
                "response_header": self.response_header
            }

            self.say(message)



    def do_get(self):
        logger.debug("do_get method called")
        r = requests.get(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_post(self):
        logger.debug("do_post method called")
        r = requests.post(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_delete(self):
        logger.debug("do_delete method called")
        r = requests.delete(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_put(self):
        logger.debug("do_put method called")
        r = requests.put(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_head(self):
        logger.debug("do_head method called")
        r = requests.head(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_patch(self):
        logger.debug("do_patch method called")
        r = requests.patch(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_options(self):
        logger.debug("do_options method called")
        r = requests.options(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def get_parameters(self):
        """

        :return: Dict of parameters usable by the "requests" lib
        """
        logger.debug("get_parameters method called")
        returned_parameters = dict()

        if self.headers is not None:
            returned_parameters["headers"] = self.headers

        if self.timeout is not None:
            returned_parameters["timeout"] = self.timeout

        if self.data is not None:
            returned_parameters["data"] = self.data

        print returned_parameters

        return returned_parameters

    def post_processing_request(self, r):
        self.status_code = r.status_code
        self.content = r.content
        self.response_header = r.headers

        logger.debug("status_code: %s" % self.status_code)
        logger.debug("content: %s" % self.content)
        logger.debug("response_header: %s" % self.response_header)

        return

    def _is_parameters_ok(self):
        if self.url is None:
            raise InvalidParameterException("Uri needs an url")

        if self.headers is not None:
            if not isinstance(self.headers, dict):
                raise InvalidParameterException("headers must be a list of string")

        if self.timeout is not None:
            if not isinstance(self.timeout, int):
                raise InvalidParameterException("timeout must be an integer")

        if self.data is not None:
            try:
                self.data = json.loads(self.data)
            except ValueError, e:
                raise InvalidParameterException("error in \"data\" parameter: %s" % e)

        allowed_method = ["GET", "POST", "DELETE", "PUT", "HEAD", "PATCH", "OPTIONS"]
        if self.method not in allowed_method:
            raise InvalidParameterException("method %s not in: %s" % (self.method, allowed_method))

        return True
