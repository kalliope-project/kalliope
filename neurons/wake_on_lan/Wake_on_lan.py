import ipaddress
import logging

from core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from wakeonlan import wol

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Wake_on_lan(NeuronModule):
    def __init__(self, **kwargs):
        super(Wake_on_lan, self).__init__(**kwargs)

        mac_address = kwargs.get('mac_address', None)
        broadcast_address = kwargs.get('broadcast_address', '255.255.255.255')
        port = kwargs.get('port', 9)

        # check we provide a mac address
        if mac_address is None:
            raise MissingParameterException("mac_address parameter required")

        # convert to unicode for testing
        broadcast_address_unicode = broadcast_address.decode('utf-8')
        # check the ip address is a valid one
        ipaddress.ip_address(broadcast_address_unicode)

        # check the port
        if type(port) is not int:
            raise InvalidParameterException("port argument must be an integer. Remove quotes in your configuration.")

        logger.debug("Call Wake_on_lan_neuron with parameters: mac_address: %s, broadcast_address: %s, port: %s"
                     % (mac_address, broadcast_address, port))

        # send the magic packet, the mac address format will be check by the lib
        # wol.send_magic_packet(mac_address, ip_address=broadcast_address, port=port)
