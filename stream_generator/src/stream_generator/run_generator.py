import asyncio
import asyncio.selector_events
import click

from .EchoClientProtocol import EchoClientProtocol
from .generators import stream

from .config import (
    ENDPOINT_HOST,
    ENDPOINT_PORT,
    setup_logging,
)

logger = setup_logging()


async def async_main():
    loop = asyncio.get_event_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(loop),
        remote_addr=(ENDPOINT_HOST, ENDPOINT_PORT)
    )

    await stream(transport.sendto)


@click.command()
def main() -> None:
    asyncio.run(
        async_main()
    )
