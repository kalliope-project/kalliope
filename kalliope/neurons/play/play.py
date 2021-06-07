import os
import random
import sndhdr

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from kalliope.core.PlayerLauncher import PlayerLauncher


class Play(NeuronModule):
    def __init__(self, **kwargs):
        super(Play, self).__init__(**kwargs)
        self.filename = kwargs.get('filename', None)
        self.player = PlayerLauncher.get_player(settings=self.settings)

        # check if parameters have been provided
        if self._is_parameters_ok():
            self.player.play(self.filename)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.filename is None:
            raise MissingParameterException("You must specify (at least one) filename")
        if not isinstance(self.filename, list):
            self.filename = [self.filename]
        self.filename[:] = [x for x in self.filename if os.path.isfile(x)]
        self.filename[:] = [x for x in self.filename if sndhdr.whathdr(x) is not None]
        self.filename[:] = [x for x in self.filename if sndhdr.whathdr(x).filetype == 'wav']
        if len(self.filename) == 0:
            raise InvalidParameterException("You must specify at least one valid wav file (none remained after validation)")
        self.filename = random.choice(self.filename)
        return True
