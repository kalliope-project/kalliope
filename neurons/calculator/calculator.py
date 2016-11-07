# encoding=utf8  
import math

from core.NeuronModule import NeuronModule, InvalidParameterException
from core import Utils


class Calculator(NeuronModule):
    def __init__(self, **kwargs):

        super(Calculator, self).__init__(**kwargs)

        """
        Ideally, a parser, lexer, tokenizer would be the best option for a
        calculator app. But this works ok for simple operations...
        """

        # get operation from brain
        self.operation  = kwargs.get('operation', None)

        # 3 following lines force STT to math operators
        self.operation  = self.operation.replace('divisé par', '/')
        self.operation  = self.operation.replace('% de', '%')
        self.operation  = self.operation.replace('pourcent de', '%')

        # get arguments and operator
        self.arguments  = self.operation.split(" ")
        self.first_arg  = Utils.string_to_num(self.arguments[0])
        self.operand    = Utils.string_to_ope(self.arguments[1])
        self.second_arg = Utils.string_to_num(self.arguments[2])

        # perform operation
        if self.operand == '-':
            self.result = self.first_arg - self.second_arg
        elif self.operand == '+':
            self.result = self.first_arg + self.second_arg
        elif self.operand == 'x':
            self.result = self.first_arg * self.second_arg
        elif self.operand == '/' and self.second_arg != 0:
            self.result = float(self.first_arg) / self.second_arg
        elif self.operand == 'puissance':
            self.result = math.pow(self.first_arg, self.second_arg)
        elif self.operand == '%':
            self.result = float(self.first_arg) * self.second_arg / 100
        else:
            raise InvalidParameterException("Input Error!")

        # convert result back to french (e.g: "point" to become "virgule")
        self.result = Utils.num_to_string(self.result)

        message = {
            "first_arg":    Utils.num_to_string(self.first_arg),
            "operand":      Utils.ope_to_string(self.operand),
            "second_arg":   Utils.num_to_string(self.second_arg),
            "result":       self.result
        }

        if self._is_parameters_ok():
            self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """
        if self.operation is None:
            raise InvalidParameterException("Need an operation")
        if self.first_arg is None:
            raise InvalidParameterException("Need a first argument")
        if self.operand is None:
            raise InvalidParameterException("Need an operand")
        if self.second_arg is None:
            raise InvalidParameterException("Need a second argument")

        return True




