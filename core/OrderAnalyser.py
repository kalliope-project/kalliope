from Utils import *
import re


class OrderAnalyser:
    def __init__(self, main_controller, order):
        """
        Class used to load
        :param order: spelt order
        :param main_controller
        """
        self.main_controller = main_controller
        self.order = order
        self.brain = get_brain()
        print "Receiver order: %s" % self.order

    def start(self):
        print self.brain

        for el in self.brain:
            # print el
            # print el["when"]
            whens = el["when"]
            for when in whens:
                brain_order = when["order"]
                print "order to test: %s" % brain_order
                if self._spelt_order_match_brain_order(brain_order):
                    print "Order found! Run neurons: %s" % el["neurons"]
                    neurons = el["neurons"]
                    for neuron in neurons:
                        for plugin, parameter in neuron.items():
                            # capitalizes the first letter (because classes have first letter upper case)
                            plugin = plugin.capitalize()
                            print "Run plugin %s with parameter %s" % (plugin, parameter)
                            mod = __import__('neurons', fromlist=[plugin])
                            klass = getattr(mod, plugin)
                            # run the plugin
                            if not parameter:
                                klass()
                            else:
                                klass(parameter)
                            # once we ran all plugin, we can start back jarvis triger
                            self.main_controller.unpause_jarvis_trigger()

    def _spelt_order_match_brain_order(self, order_to_test):
        """
        test if the current order match the order spelt by the user
        :param order_to_test:
        :return:
        """
        my_regex = r"\b(?=\w)" + re.escape(order_to_test) + r"\b(?!\w)"

        if re.search(my_regex, self.order, re.IGNORECASE):
            return True


