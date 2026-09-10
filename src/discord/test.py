import discord
from discord import app_commands
from discord.ext import commands

class test_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="get_test", description="test database SELECT")
    async def get_test_prefix(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.author.mention} has {await self.bot.db.get_value(ctx.author.id, "points", 0)} points")

    @commands.hybrid_command(name="set_test", description="test database INSERT")
    @app_commands.describe(amount="points to add")
    async def set_test_prefix(self, ctx: commands.Context, amount: int = 1) -> None:
        pts = await self.bot.db.get_value(ctx.author.id, "points", 0)
        pts += amount
        await self.bot.db.set_value(ctx.author.id, "points", pts)
        await ctx.send(f"{ctx.author.mention} earned {amount} points and now has {pts} points")

