import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from game.db import Database
from game.player import PlayerManager
from game.items import ItemManager
from game.item_table import setup_item_table
from game.recipes import RecipeManager
from game.recipe_table import setup_recipe_table
from ui.inventory import inventory_cog
from ui.player import player_cog
from ui.recipes import recipes_cog

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("bot")

load_dotenv()
TOKEN = os.environ.get("DC_TOKEN")
DEV_GUILD = os.environ.get("DEV_GUILD")
if not TOKEN:
    raise SystemExit("you big dummy, set DC_TOKEN")

class NyaltivationBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="~", intents=intents)
        self.db = Database()
        self.pm = PlayerManager(self.db)
        self.im = ItemManager()
        setup_item_table(self.im)
        self.rm = RecipeManager()
        setup_recipe_table(self.rm)

    async def setup_hook(self) -> None:
        await self.db.connect()
        await self.add_cog(inventory_cog(self))
        await self.add_cog(player_cog(self))
        await self.add_cog(recipes_cog(self))
        if DEV_GUILD is not None:
            logger.info(f"Syncing to {DEV_GUILD}")
            guild = discord.Object(id=DEV_GUILD)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def close(self) -> None:
        logger.info("Shutting down...")
        await self.db.close()
        await super().close()

bot = NyaltivationBot()

async def main() -> None:
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Signal raised")

