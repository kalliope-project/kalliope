import json
import logging
import os

import requests

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Uri(NeuronModule):

    def __init__(self, **kwargs):
        super(Uri, self).__init__(**kwargs)

        # input variables
        self.url = kwargs.get('url', None)
        self.headers = kwargs.get('headers', None)
        self.data = kwargs.get('data', None)
        self.data_from_file = kwargs.get('data_from_file', None)
        self.method = kwargs.get('method', "GET")
        self.user = kwargs.get('user', None)
        self.password = kwargs.get('password', None)
        self.timeout = kwargs.get('timeout', None)

        # processing parameters
        self.parameters = None

        # output variable
        self.status_code = None
        self.content = None
        self.text = None
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
        logger.debug(self.neuron_name + " do_get method called")
        r = requests.get(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_post(self):
        logger.debug(self.neuron_name + " do_post method called")
        r = requests.post(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_delete(self):
        logger.debug(self.neuron_name + " do_delete method called")
        r = requests.delete(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_put(self):
        logger.debug(self.neuron_name + " do_put method called")
        r = requests.put(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_head(self):
        logger.debug(self.neuron_name + " do_head method called")
        r = requests.head(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_patch(self):
        logger.debug(self.neuron_name + " do_patch method called")
        r = requests.patch(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def do_options(self):
        logger.debug(self.neuron_name + " do_options method called")
        r = requests.options(url=self.url, **self.parameters)
        self.post_processing_request(r)

    def get_parameters(self):
        """

        :return: Dict of parameters usable by the "requests" lib
        """
        returned_parameters = dict()

        if self.headers is not None:
            returned_parameters["headers"] = self.headers

        if self.timeout is not None:
            returned_parameters["timeout"] = self.timeout

        if self.data is not None:
            returned_parameters["data"] = self.data

        if self.data_from_file is not None:
            returned_parameters["data"] = self.data_from_file

        if self.user is not None:
            # this implicitly means that the password is set too, the check has been done in _is_parameters_ok
            returned_parameters["auth"] = self.user, self.password

        logger.debug(self.neuron_name + " parameters: %s" % returned_parameters)

        return returned_parameters

    def post_processing_request(self, r):
        self.status_code = r.status_code
        self.content = r.content
        # we try to load into a json object the content. So Kalliope can use it to talk
        try:
            self.content = json.loads(self.content)
        except ValueError:
            logger.debug(self.neuron_name + "cannot get a valid json from returned content")
            pass
        self.text = r.text
        self.response_header = r.headers

        logger.debug(self.neuron_name + " status_code: %s" % self.status_code)
        logger.debug(self.neuron_name + " content: %s" % self.content)
        logger.debug(self.neuron_name + " response_header: %s" % self.response_header)

    def _is_parameters_ok(self):
        """
        Check that all provided parameters in the neurons are valid
        :return: True if all check passed
        """
        # URL is mandatory
        if self.url is None:
            raise InvalidParameterException("Uri needs an url")

        # headers can be null, but if provided it must be a list
        if self.headers is not None:
            if not isinstance(self.headers, dict):
                raise InvalidParameterException("headers must be a list of key: value")

        # timeout in second must be an integer
        if self.timeout is not None:
            if not isinstance(self.timeout, int):
                raise InvalidParameterException("timeout must be an integer")

        # data must be loadable with json
        if self.data is not None:
            try:
                json.loads(self.data)
            except ValueError, e:
                raise InvalidParameterException("error in \"data\" parameter: %s" % e)

        # data_from_file path must exist and data inside must be loadable by json
        if self.data_from_file is not None:
            # check that the file exist
            if not os.path.exists(self.data_from_file):
                raise InvalidParameterException("error in \"data_file\". File does not exist: %s" % self.data_from_file)
            # then try to load the json from the file
            try:
                self.data_from_file = self.readfile(self.data_from_file)
            except ValueError, e:
                raise InvalidParameterException("error in \"data\" parameter: %s" % e)

        # we cannot provide both data and data from file
        if self.data is not None and self.data_from_file is not None:
            raise InvalidParameterException("URI can be used with data or data_from_file, not both in same time")

        # the provided method must exist
        allowed_method = ["GET", "POST", "DELETE", "PUT", "HEAD", "PATCH", "OPTIONS"]
        if self.method not in allowed_method:
            raise InvalidParameterException("method %s not in: %s" % (self.method, allowed_method))

        return True

    @staticmethod
    def readfile(file_path):
        """
        return the content of the file <file_path>
        :param file_path: File path to read
        :return: Str content of the file
        """
        file_to_read = open(file_path, 'r')
        return file_to_read.read()
