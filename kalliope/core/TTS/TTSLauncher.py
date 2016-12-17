import logging

from kalliope.core import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TTSLauncher(object):
    def __init__(self):
        pass

    @classmethod
    def get_tts(cls, tts):
        """
        Return an instance of a TTS module from the name of this module
        :param tts: TTS model
        :type tts: Tts
        :return: TTS module instance

        .. seealso::  TTS
        .. warnings:: Class Method and Public
        """
        logger.debug("get TTS module \"%s\" with parameters %s" % (tts.name, tts.parameters))
        return Utils.get_dynamic_class_instantiation(package_name="tts",
                                                     module_name=tts.name,
                                                     parameters=tts.parameters)
