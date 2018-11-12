import asyncio
import click

from .generators import stream

from .config import (
    ENDPOINT_HOST,
    ENDPOINT_PORT,
    setup_logging,
)

logger = setup_logging()


async def async_main():
    await stream()

@click.command()
def main() -> None:
    asyncio.run(
        async_main()
    )
