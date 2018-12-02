from kalliope.core.NeuronModule import NeuronModule, MissingParameterException


class Say(NeuronModule):
    def __init__(self, **kwargs):
        super(Say, self).__init__(**kwargs)
        self.message = kwargs.get('message', None)
        self.file_template = kwargs.get('file_template', None)
        self.parameters = kwargs.get('parameters', None)

        if self.file_template is not None:
            self.message = self.parameters

        # check if parameters have been provided
        if self._is_parameters_ok():
            self.say(self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.message is None and self.file_template is None:
            raise MissingParameterException("You must specify a message string, a list of messages or a file template"
                                            " as parameter")
        return True
