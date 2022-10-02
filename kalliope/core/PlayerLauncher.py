import logging

from kalliope.core import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class PlayerLauncher(object):
    def __init__(self):
        pass

    @staticmethod
    def get_player(settings):
        """
        Instantiate a Player
        :param settings: setting object
        :type settings: Settings
        :return: the Player instance
        :rtype: Player
        """

        player_folder = None
        if settings.resources:
            player_folder = settings.resources.player_folder

        player_instance = None
        for player in settings.players:
            if player.name == settings.default_player_name:
                logger.debug("PlayerLauncher: Start player %s with parameters: %s" % (player.name, player.parameters))
                player_instance = Utils.get_dynamic_class_instantiation(package_name="players",
                                                                        module_name=player.name,
                                                                        parameters=player.parameters,
                                                                        resources_dir=player_folder)
                break
        return player_instance
