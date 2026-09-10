import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from game.db import Database
from ui.test import test_cog

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("bot")

load_dotenv()
TOKEN = os.environ.get("DC_TOKEN")
DEV_GUILD = os.environ.get("DEV_GUILD")
if not TOKEN:
    raise SystemExit("you big dummy, set DC_TOKEN")

class TestBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="~", intents=intents)
        self.db = Database()

    async def setup_hook(self) -> None:
        await self.db.connect()
        await self.add_cog(test_cog(self))
        if DEV_GUILD is not None:
            logger.info(f"Syncing to {DEV_GUILD}")
            await self.tree.sync(guild=discord.Object(id=DEV_GUILD))
        await self.tree.sync()

    async def close(self) -> None:
        logger.info("Shutting down...")
        await self.db.close()
        await super().close()

bot = TestBot()

async def main() -> None:
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Signal raised")

