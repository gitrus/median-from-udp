import asyncio
import logging
from asyncio import DatagramProtocol
from datetime import datetime

import msgpack
from asyncpg import Connection as APGConnection

from endpoint.config import SEQUENCE_DUMP_NUMBER
from endpoint.modules.db import insert_percentiles

from .modules.median import StreamMetrics, StreamValue

logger = logging.getLogger("info_log")


class MetricsServerProtocol(DatagramProtocol):
    """
    UDP protocol with StreamMetrics accumulator for calculate 25, 50 ,75 percentiles from stream.
    We assume that input datagram will be determined type (msgpack(float, iso_date)).
    """
    def __init__(self, connection: APGConnection) -> None:
        self.stream = StreamMetrics()
        self.pg_connection = connection

        super()

    def connection_made(self, transport) -> None:
        logger.info("Initialise connection_made")
        self.transport = transport

    def datagram_received(self, data, addr) -> None:
        message = msgpack.unpackb(data, raw=False)

        msg_int, msg_date = (
            message[0],
            datetime.strptime(message[1], "%Y%m%dT%H:%M:%S.%f"),
        )

        self.stream.append(StreamValue(msg_int, msg_date))

        if (
            self.stream.stream_sequence > SEQUENCE_DUMP_NUMBER
            and self.stream.stream_sequence % SEQUENCE_DUMP_NUMBER == 1
        ):
            asyncio.ensure_future(
                insert_percentiles(self.pg_connection, self.stream.current_metrics())
            )
