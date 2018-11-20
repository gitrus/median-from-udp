from typing import Dict, Union

import asyncpg
from asyncpg import Connection as APGConnection


async def insert_percentiles(pg_conn: APGConnection, percentiles: Dict[int, Union[int, float]]):
    await pg_conn.execute(
        "INSERT INTO percentiles (percentile_25, percentile_50, percentile_75) VALUE ($1,$2,$3)",
        [percentiles[key] for key in (25, 50, 75)]
    )
