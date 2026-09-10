import discord
from discord import app_commands
from discord.ext import commands
from game.loc import Language

class player_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="lang", description="Change your language")
    @app_commands.describe(lang="what language you want")
    @app_commands.choices(lang=[
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="Catpersonian", value="nya"),
    ])
    async def lang(self, ctx: commands.Context, lang: str) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)
        if lang == "en":
            await player.set_language(Language.EN)
            await ctx.send("Your language is now English")
        elif lang == "nya":
            await player.set_language(Language.NYA)
            await ctx.send("Your language is now Catpersonian")

