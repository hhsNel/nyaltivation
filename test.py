from discord.ext import commands

class test_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def get_test(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.author.mention} has {await self.bot.db.get_value(ctx.author_id, "points", 0)} points")

    @commands.command()
    async def set_test(self, ctx: commands.Context, amount: int = 1) -> None:
        pts = await self.bot.db.get_value(ctx.author_id, "points", 0)
        pts += amount
        await self.bot.db.set_value(ctx.author_id, "points", pts)
        await ctx.send(f"{ctx.author.mention} earned {amount} points and now has {pts} points")

