import unittest
from ..OrderAnalyser import *


class OrderAnalyserTest(unittest.TestCase):

    """Test case for the OrderAnalyser Class"""

    def setUp(self):
        pass

    def test__is_containing_bracket(self):
        self.assertTrue(OrderAnalyser._is_containing_bracket("This test contains {{ bracket }}"))