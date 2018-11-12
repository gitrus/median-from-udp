import random
import logging
import struct

logger = logging.getLogger('info_log')


class EchoServerProtocol:
    def connection_made(self, transport):
        logger.info("connection_made")
        self.transport = transport
        self.random = random.random()

    def datagram_received(self, data, addr):
        message = struct.unpack('<f', data)
        logger.info('Received %r from %s' % (message, addr))
