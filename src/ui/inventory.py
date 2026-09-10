import discord
from discord import app_commands
from discord.ext import commands

class inventory_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="inventory", description="Look through inventory")
    async def inventory(self, ctx: commands.Context) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)
        response: str = f"# {ctx.author.mention}'s Inventory:\n"
        for item,qty in player.inventory.items():
            response += f" - {qty} x {self.bot.im.get_item(item).name.str(player.loc)}\n"
        if len(player.inventory) == 0:
            response += "(empty)"
        await ctx.send(response)

    @commands.hybrid_command(name="add_item", description="add item to inventory (dev)")
    @app_commands.describe(id="item to add")
    @app_commands.describe(amount="amount of that item to add")
    async def set_test_prefix(self, ctx: commands.Context, id: str, amount: int = 1) -> None:
        if(self.bot.im.item_exists(id)):
            player = await self.bot.pm.get_player(ctx.author.id)
            await player.change_inventory_item(id, amount)
            await ctx.send(f"now {ctx.author.mention} has {player.get_inventory_item(id)} {self.bot.im.get_item(id).name.str(player.loc)}")
        else:
            await ctx.send(f"no such item: {id}")

