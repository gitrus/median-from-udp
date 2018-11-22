import logging
from asyncio import DatagramProtocol

logger = logging.getLogger('inf_log')


class StreamProtocol(DatagramProtocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.on_con_lost = loop.create_future()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        logger.info(f"Received: {data.decode()}")

    def error_received(self, exc):
        logger.error('Error received:', exc)

    def connection_lost(self, exc):
        logger.warning("Connection closed")
        self.on_con_lost.set_result(True)
