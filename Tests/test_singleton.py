import unittest
import sys
from six import with_metaclass

from kalliope.core.Models import Singleton


class MyClass(with_metaclass(Singleton, object)):

    def __init__(self):
        self.value = "test"

class TestSingleton(unittest.TestCase):

    def setUp(self):
        pass

    def test_singleton(self):

        obj1 = MyClass()
        obj2 = MyClass()

        self.assertEqual(id(obj1), id(obj2))

    def test_drop_singleton(self):

        obj1 = MyClass()
        obj2 = MyClass()
        # drop the singleton instance
        Singleton._instances = {}
        obj3 = MyClass()

        self.assertEqual(id(obj1), id(obj2))
        self.assertNotEqual(id(obj1), id(obj3))
