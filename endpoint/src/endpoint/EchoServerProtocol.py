import random
import logging

logger = logging.getLogger('info_log')


class EchoServerProtocol:
    def connection_made(self, transport):
        logger.info("connection_made")
        self.transport = transport
        self.random = random.random()

    def datagram_received(self, data, addr):
        message = data.decode()
        logger.info('Received %r from %s' % (message, addr))
        logger.info('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)
