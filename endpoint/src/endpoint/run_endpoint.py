import asyncio
import asyncpg

from .metrics_server_protocol import MetricsServerProtocol
from .config import (
    setup_logging,
    ENDPOINT_HOST,
    ENDPOINT_PORT,
    PG_HOST,
    PG_PORT,
    PG_USER,
    PG_PASSWORD,
)

logger = setup_logging()


async def async_main():
    logger.info("Starting UDP server")

    loop = asyncio.get_running_loop()

    conn = await asyncpg.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD
    )
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MetricsServerProtocol(conn), local_addr=(ENDPOINT_HOST, ENDPOINT_PORT)
    )

    try:
        await asyncio.sleep(60 * 60 * 10)  # Serve for 10 hour.
    finally:
        transport.close()


def main() -> None:
    asyncio.run(async_main())
