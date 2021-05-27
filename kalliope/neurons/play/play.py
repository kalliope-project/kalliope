import os
import random
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from kalliope.core.PlayerLauncher import PlayerLauncher


class Play(NeuronModule):
    def __init__(self, **kwargs):
        super(Play, self).__init__(**kwargs)
        self.file = kwargs.get('file', None)
        self.player = PlayerLauncher.get_player(settings=self.settings)

        # check if parameters have been provided
        if self._is_parameters_ok():
            self.player.play(self.file)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.file is None:
            raise MissingParameterException("You must specify a file")
        if isinstance(self.file, list):
            self.file = random.choice(self.file)
        if os.path.isfile(self.file) is False:
            raise InvalidParameterException("You must specify an existing file")
        return True
