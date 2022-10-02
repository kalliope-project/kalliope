import unittest
import mock

from kalliope.core.Models.settings.Player import Player
from kalliope.core.Models.settings.Settings import Settings
from kalliope.core.PlayerLauncher import PlayerLauncher


class TestPlayerLauncher(unittest.TestCase):
    """
    Class to test Launchers Classes (PlayerLauncher) and methods
    """

    def setUp(self):
        pass

    ####
    # Player Launcher
    def test_get_player(self):
        """
        Test the PlayerLauncher trying to run the Player
        """
        player1 = Player("Player", {})
        player2 = Player("Player2", {'test': "hitheparamtest"})
        settings = Settings()
        settings.players = [player1, player2]
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            # Get the player1
            settings.default_player_name = "Player"
            PlayerLauncher.get_player(settings=settings)

            mock_get_class_instantiation.assert_called_once_with(package_name="players",
                                                                 module_name=player1.name,
                                                                 parameters=player1.parameters,
                                                                 resources_dir=None)
            mock_get_class_instantiation.reset_mock()

            # Get the player 2
            settings.default_player_name = "Player2"
            PlayerLauncher.get_player(settings=settings)

            mock_get_class_instantiation.assert_called_once_with(package_name="players",
                                                                 module_name=player2.name,
                                                                 parameters=player2.parameters,
                                                                 resources_dir=None)
            mock_get_class_instantiation.reset_mock()
