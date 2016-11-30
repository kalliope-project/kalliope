import logging
import re

from core.NeuronModule import NeuronModule, MissingParameterException
from core.Models import Order

class List_available_orders(NeuronModule):
    def __init__(self, **kwargs):
        super(List_available_orders, self).__init__(**kwargs)

        ignore_machine_name = kwargs.get('ignore_machine_name', None)
        query_replace_text = kwargs.get("query_replace_text", None)

        self.values = dict()
        self.values['orders'] = []
        self.values['nb_orders'] = 0

        # check if parameters have been provided
        if self._is_parameters_ok():
            for synapse in self.brain.synapses:
                for signal in synapse.signals:
                    if isinstance(signal, Order):
                        if self._is_valid_order(signal.sentence, ignore_machine_name):
                            self.values['orders'].append(
                                self._get_final_sentence(signal.sentence, query_replace_text))

            self.values['nb_orders'] = len(self.values['orders'])

            self.say(self.values)


    def _is_valid_order(self, sentence, ignore_machine_name):
        """
        Check if the order should be added to the list of available orders.

        :return: true if the order is valid, false otherwise
        :rtype: Boolean
        """

        if ignore_machine_name == 1 and re.compile("\w+(-\w)+").match(sentence) is not None:
            return False

        return True

    def _get_final_sentence(self, sentence, query_replace_text):
        """
        Return the final sentence with the changed text if applicable

        :return: the final sentence
        :rtype: String
        """

        s = sentence
        pattern = re.compile("\{\{ \w+ \}\}")

        if pattern.search(sentence) is not None and query_replace_text is not None:
            s = re.sub(pattern, query_replace_text, sentence)

        return s

