import ipaddress
import logging

from core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from wakeonlan import wol

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Wake_on_lan(NeuronModule):
    def __init__(self, **kwargs):
        super(Wake_on_lan, self).__init__(**kwargs)

        self.mac_address = kwargs.get('mac_address', None)
        self.broadcast_address = kwargs.get('broadcast_address', '255.255.255.255')
        self.port = kwargs.get('port', 9)

        # check parameters
        if self._is_parameters_ok():
            # convert to unicode for testing
            broadcast_address_unicode = self.broadcast_address.decode('utf-8')
            # check the ip address is a valid one
            ipaddress.ip_address(broadcast_address_unicode)

            logger.debug("Call Wake_on_lan_neuron with parameters: mac_address: %s, broadcast_address: %s, port: %s"
                         % (self.mac_address, self.broadcast_address, self.port))

            # send the magic packet, the mac address format will be check by the lib
            wol.send_magic_packet(self.mac_address, ip_address=self.broadcast_address, port=self.port)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        """
        # check we provide a mac address
        if self.mac_address is None:
            raise MissingParameterException("mac_address parameter required")
            # check the port
        if type(self.port) is not int:
            raise InvalidParameterException(
                "port argument must be an integer. Remove quotes in your configuration.")

        return True
