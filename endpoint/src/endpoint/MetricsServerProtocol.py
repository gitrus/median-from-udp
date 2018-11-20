from datetime import datetime
import logging

import msgpack
from .modules.median import StreamMetrics, StreamValue

logger = logging.getLogger("info_log")


class MetricsServerProtocol:
    def __init__(self) -> None:
        self.stream = StreamMetrics()

        super()

    def connection_made(self, transport) -> None:
        logger.info("Initialise connection_made")
        self.transport = transport

    def datagram_received(self, data, addr) -> None:
        message = msgpack.unpackb(data, raw=False)

        msg_int, msg_date = message[0], datetime.strptime(message[1], "%Y%m%dT%H:%M:%S.%f")
        logger.info(f"Received {msg_int}, {msg_date} from {addr}")

        self.stream.append(StreamValue(msg_int, msg_date))



