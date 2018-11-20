import asyncio

from .MetricsServerProtocol import MetricsServerProtocol
from .config import ENDPOINT_HOST, ENDPOINT_PORT, setup_logging

logger = setup_logging()


async def async_main():
    logger.info("Starting UDP server")

    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MetricsServerProtocol(),
        local_addr=(ENDPOINT_HOST, ENDPOINT_PORT)
    )

    try:
        await asyncio.sleep(60 * 60 * 10)  # Serve for 10 hour.
    finally:
        transport.close()


def main() -> None:
    asyncio.run(
        async_main()
    )
