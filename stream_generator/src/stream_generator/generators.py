import asyncio
import logging
from datetime import datetime
from typing import Collection, Callable, Generator, Union, NewType, Awaitable
from functools import partial

import numpy as np
import msgpack

from .utils.codec import encode_msg
from .distributions import get_sample_gen_by_name

GenValueType = NewType('GenValueType', Union[float, np.float])

logger = logging.getLogger('info_log')

SAMPLE_MIN_SIZE = 20


async def delayed_gen(
    sample_fabric: Callable[[int], Collection[GenValueType]],
    delay: float
) -> Generator[GenValueType, None, None]:
    """Yield numbers from 0 to `to` every `delay` seconds."""
    while True:
        for v in sample_fabric(SAMPLE_MIN_SIZE):
            yield v
            await asyncio.sleep(delay)


async def stream(send: Awaitable):
    gen = delayed_gen(
        partial(
            get_sample_gen_by_name('normal'),
            1,
            3
        ),
        0.01
    )

    async for v in gen:
        send(
            msgpack.packb((v, datetime.now()), default=encode_msg, use_bin_type=True)
        )
