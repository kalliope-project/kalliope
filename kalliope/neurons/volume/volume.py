import logging

from kalliope.core import NeuronModule
import alsaaudio

from kalliope.core.NeuronModule import InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SoundManager(object):

    try:
        m = alsaaudio.Mixer()
    except alsaaudio.ALSAAudioError:
        # no master, we are on a Rpi
        try:
            m = alsaaudio.Mixer("PCM")
        except alsaaudio.ALSAAudioError:
            # no audio config at all
            m = None

    @classmethod
    def set_volume(cls, volume_level):
        if cls.m is not None:
            cls.m.setvolume(int(volume_level))

    @classmethod
    def get_volume(cls):
        if cls.m is not None:
            vol = cls.m.getvolume()
            return int(vol[0])
        return None


class Volume(NeuronModule):

    def __init__(self, **kwargs):
        super(Volume, self).__init__(**kwargs)

        self.level = kwargs.get('level', None)
        self.action = kwargs.get('action', "set")  # can be set, raise or lower

        # check parameters
        if self._is_parameters_ok():
            if self.action == "set":
                logger.debug("[Volume] set volume to: {}".format(self.level))
                SoundManager.set_volume(self.level)
            if self.action == "raise":
                current_level = SoundManager.get_volume()
                level_to_set = self.level + current_level
                if level_to_set > 100:
                    level_to_set = 100
                logger.debug("[Volume] set volume to: {}".format(level_to_set))
                SoundManager.set_volume(level_to_set)
            if self.action == "lower":
                current_level = SoundManager.get_volume()
                level_to_set = current_level - self.level
                if level_to_set < 0:
                    level_to_set = 0
                logger.debug("[Volume] set volume to: {}".format(level_to_set))
                SoundManager.set_volume(level_to_set)

            message = {
                "asked_level": self.level,
                "asked_action": self.action,
                "current_level": SoundManager.get_volume()
            }
            self.say(message)

    def _is_parameters_ok(self):
        if self.level is None:
            raise InvalidParameterException("[Volume] level need to be set")
        try:
            self.level = int(self.level)
        except ValueError:
            raise InvalidParameterException("[Volume] level '{}' is not a valid integer".format(self.level))
        if self.level < 0 or self.level > 100:
            raise InvalidParameterException("[Volume] level need to be placed between 0 and 100")
        if self.action not in ["set", "raise", "lower"]:
            raise InvalidParameterException("[Volume] action can be 'set', 'raise' or 'lower'")
        return True
