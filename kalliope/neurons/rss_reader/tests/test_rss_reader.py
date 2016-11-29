import unittest

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.rss_reader.rss_reader import Rss_reader


class TestRss_Reader(unittest.TestCase):

    def setUp(self):
        self.feedUrl="http://www.lemonde.fr/rss/une.xml"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Rss_reader(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

if __name__ == '__main__':
    unittest.main()

