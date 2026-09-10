import discord
from discord import app_commands
from discord.ext import commands
from game.player import PlayerActionType
import time

class recipes_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="recipe_start", description="Begin an empty recipe")
    async def recipe_start(self, ctx: commands.Context) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)
        if player.assert_state(PlayerActionType.REFINING):
            await ctx.send("You begin refining")
        else:
            await ctx.send("You're already doing something else!")

    @commands.hybrid_command(name="recipe_item", description="Add an item to the cauldron")
    @app_commands.describe(id="Item to add")
    async def recipe_item(self, ctx: commands.Context, id: str) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)

        if not player.assert_state(PlayerActionType.REFINING):
            await ctx.send("You're already doing something else!")
            return
        if not self.bot.im.item_exists(id):
            await ctx.send("This item doesn't exist")
            return
        if player.get_inventory_item(id) == 0:
            await ctx.send(f"You don't have enough {self.bot.im.get_item(id).name.str(player.loc)}")
            return

        await player.change_inventory_item(id, -1)
        player.refining_data.add_item(id)
        await ctx.send(f"You add 1 {self.bot.im.get_item(id).name.str(player.loc)} and have {player.get_inventory_item(id)} left ")

    @commands.hybrid_command(name="recipe_boil", description="Start boiling")
    async def recipe_boil(self, ctx: commands.Context) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)

        if not player.assert_state(PlayerActionType.REFINING):
            await ctx.send("You're already doing something else!")
            return

        player.refining_data.boil()
        await ctx.send(f"You start boiling (<t:{int(time.time())}:R>)")

    @commands.hybrid_command(name="recipe_stir", description="Start stirring")
    async def recipe_stir(self, ctx: commands.Context) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)

        if not player.assert_state(PlayerActionType.REFINING):
            await ctx.send("You're already doing something else!")
            return

        player.refining_data.stir()
        await ctx.send(f"You start stirring (<t:{int(time.time())}:R>)")

    @commands.hybrid_command(name="recipe_stop", description="Stop the current action (boiling/stirring)")
    async def recipe_stop(self, ctx: commands.Context) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)

        if not player.assert_state(PlayerActionType.REFINING):
            await ctx.send("You're already doing something else!")
            return

        player.refining_data.stop_action()
        await ctx.send("You stop your current action")

    @commands.hybrid_command(name="recipe_finish", description="Finish the recipe")
    async def recipe_finish(self, ctx: commands.Context) -> None:
        player = await self.bot.pm.get_player(ctx.author.id)

        if not player.assert_state(PlayerActionType.REFINING):
            await ctx.send("You're already doing something else!")
            return

        rec = player.refining_data.finish()
        if rec is None:
            await ctx.send("A recipe requires some steps!")
            return

        id = self.bot.rm.try_steps(rec)
        if id is None:
            await ctx.send("The recipe failed (all items are lost)")
            return

        await player.change_inventory_item(id, 1)
        await ctx.send(f"You managed to refine {self.bot.im.get_item(id).name.str(player.loc)}!")

