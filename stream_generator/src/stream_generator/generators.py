import asyncio
from typing import Collection, Callable, Generator, Union, NewType
from functools import partial

import numpy as np
import logging

from .distributions import get_sample_gen_by_name

GenValueType = NewType('GenValueType', Union[float, np.float])

logger = logging.getLogger('info_log')


async def delayed_gen(
    sample_fabric: Callable[[int], Collection[GenValueType]],
    delay: float
) -> Generator[GenValueType, None, None]:
    """Yield numbers from 0 to `to` every `delay` seconds."""
    while True:
        for v in sample_fabric(20):
            yield v
            await asyncio.sleep(delay)


async def stream():
    gen = delayed_gen(
        partial(
            get_sample_gen_by_name('normal'),
            0.1,
            0.01
        ),
        0.2
    )
    for i in range(1000):
        logger.info(
            await gen.__anext__()
        )
