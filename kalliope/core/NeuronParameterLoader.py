from kalliope.core.Cortex import Cortex
from kalliope.core.Utils import Utils

import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NeuronParameterLoader(object):

    @classmethod
    def get_parameters(cls, synapse_order, user_order):
        """
        Class method to get all params coming from a string order. Returns a dict of key/value.
        """
        params = dict()
        if Utils.is_containing_bracket(synapse_order):
            params = cls._associate_order_params_to_values(user_order, synapse_order)
            logger.debug("[NeuronParameterLoader.get_parameters]Parameters for order: %s" % params)
            # we place the dict of parameters load from order into a cache in Cortex so the user can save it later
            Cortex.add_parameters_from_order(params)
        return params

    @classmethod
    def _associate_order_params_to_values(cls, order, order_to_check):
        """
        Associate the variables from the order to the incoming user order
        :param order_to_check: the order to check incoming from the brain
        :type order_to_check: str
        :param order: the order from user
        :type order: str
        :return: the dict corresponding to the key / value of the params
        """
        logger.debug("[NeuronParameterLoader._associate_order_params_to_values] user order: %s, "
                     "order from synapse: %s" % (order, order_to_check))

        list_word_in_order = Utils.remove_spaces_in_brackets(order_to_check).split()

        # remove sentence before order which are sentences not matching anyway
        truncate_list_word_said = order.split()

        # make dict var:value
        dict_var = dict()
        for idx, ow in enumerate(list_word_in_order):
            if not Utils.is_containing_bracket(ow):
                while truncate_list_word_said and ow.lower() != truncate_list_word_said[0].lower():
                    truncate_list_word_said = truncate_list_word_said[1:]
            else:
                # remove bracket and grab the next value / stop value
                var_name = ow.replace("{{", "").replace("}}", "")
                stop_value = Utils.get_next_value_list(list_word_in_order[idx:])
                if stop_value is None:
                    dict_var[var_name] = " ".join(truncate_list_word_said)
                    break
                for word_said in truncate_list_word_said:
                    if word_said.lower() == stop_value.lower():  # Do not consider the case
                        break
                    if var_name in dict_var:
                        dict_var[var_name] += " " + word_said
                        truncate_list_word_said = truncate_list_word_said[1:]
                    else:
                        dict_var[var_name] = word_said
            truncate_list_word_said = truncate_list_word_said[1:]

        return dict_var
