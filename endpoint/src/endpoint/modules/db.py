from typing import Dict, Union

import asyncpg
from asyncpg import Connection as APGConnection


async def insert_percentiles(
    pg_conn: APGConnection, percentiles: Dict[int, Union[int, float]]
):
    await pg_conn.execute(
        "INSERT INTO percentiles (percentile_25, percentile_50, percentile_75) VALUES ($1,$2,$3)",
        percentiles[25],
        percentiles[50],
        percentiles[75],
    )
