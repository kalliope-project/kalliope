import unittest

from kalliope.neurons.systemdate import Systemdate


class TestSystemdate(unittest.TestCase):

    def setUp(self):
        pass

    def test_date_is_returned(self):
        """
        Check that the neuron return consistent values
        :return:
        """
        systemdate = Systemdate()
        # check returned value
        self.assertTrue(0 <= int(systemdate.message["hours"]) <= 24)
        self.assertTrue(0 <= int(systemdate.message["minutes"]) <= 60)
        self.assertTrue(0 <= int(systemdate.message["weekday"]) <= 6)
        self.assertTrue(1 <= int(systemdate.message["day_month"]) <= 31)
        self.assertTrue(1 <= int(systemdate.message["month"]) <= 12)
        self.assertTrue(2016 <= int(systemdate.message["year"]) <= 3000)


if __name__ == '__main__':
    unittest.main()
