import asyncio
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

import aiosqlite

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "database.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS user_data (
    user_id INTEGER PRIMARY KEY,
    data    TEXT NOT NULL DEFAULT '{}'
);
"""


class Database:
    def __init__(self, path: Path = DB_PATH) -> None:
        self.path = path
        self.connection: aiosqlite.Connection | None = None
        self.locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def connect(self) -> None:
        self.connection = await aiosqlite.connect(self.path)
        await self.connection.execute("PRAGMA journal_mode=WAL;")
        await self.connection.execute("PRAGMA synchronous=FULL;")
        await self.connection.execute(_SCHEMA)
        await self.connection.commit()
        logger.info("Database connected at %s", self.path)

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()
            self.connection = None
            logger.info("Database connection closed")

    async def get_user_data(self, user_id: int) -> dict[str, Any]:
        assert self.connection is not None, "call connect() first"
        async with self.connection.execute(
            "SELECT data FROM user_data WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
        return json.loads(row[0]) if row else {}

    async def set_user_data(self, user_id: int, data: dict[str, Any]) -> None:
        assert self.connection is not None, "call connect() first"
        await self.connection.execute(
            """
            INSERT INTO user_data (user_id, data) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET data = excluded.data
            """,
            (user_id, json.dumps(data)),
        )
        await self.connection.commit()

    async def get_value(self, user_id: int, key: str, default: Any = None) -> Any:
        data = await self.get_user_data(user_id)
        return data.get(key, default)

    async def set_value(self, user_id: int, key: str, value: Any) -> None:
        async with self.locks[user_id]:
            data = await self.get_user_data(user_id)
            data[key] = value
            await self.set_user_data(user_id, data)

