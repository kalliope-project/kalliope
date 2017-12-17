import logging

from kalliope.core.Lifo.LIFOBuffer import LIFOBuffer
from six import with_metaclass
from kalliope.core.Models import Singleton

logging.basicConfig()
logger = logging.getLogger("kalliope")


class LifoManager(with_metaclass(Singleton, object)):

    lifo_buffer = LIFOBuffer()

    @classmethod
    def get_singleton_lifo(cls):
        return cls.lifo_buffer

    @classmethod
    def get_new_lifo(cls):
        return LIFOBuffer()

    @classmethod
    def clean_saved_lifo(cls):
        cls.lifo_buffer = LIFOBuffer()

