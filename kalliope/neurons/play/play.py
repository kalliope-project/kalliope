import os
import random
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
            raise MissingParameterException("You must specify a filename")
        if isinstance(self.filename, list):
            self.filename = random.choice(self.filename)
        if os.path.isfile(self.filename) is False:
            raise InvalidParameterException("You must specify an existing filename")
        return True
