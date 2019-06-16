import logging

from kalliope.core.Lifo.LIFOBuffer import LIFOBuffer
from six import with_metaclass
from kalliope.core.Models import Singleton

logging.basicConfig()
logger = logging.getLogger("kalliope")


class LifoManager(with_metaclass(Singleton, object)):

    lifo_buffer = None

    @classmethod
    def get_singleton_lifo(cls):
        if cls.lifo_buffer is None:
            cls._new_lifo_buffer()
        return cls.lifo_buffer

    @classmethod
    def get_new_lifo(cls):
        """
        This class is used to manage hooks "on_start_speaking" and "on_stop_speaking".
        :return:
        """
        return LIFOBuffer()

    @classmethod
    def clean_saved_lifo(cls):
        cls.lifo_buffer = LIFOBuffer()

    @classmethod
    def _new_lifo_buffer(cls):
        cls.lifo_buffer = LIFOBuffer()
