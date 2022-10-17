import discord
import logging
from settings import *
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cogs/old loaded")

    @commands.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title=self.bot.user,
                              description="\n\n", color=0xE60012)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        for command in HELP:
            embed.add_field(
                name=PREFIX + command['title'], value=command["description"], inline=False)

        embed.add_field(name=f"{PREFIX}help",
                        value=f"Show this help menu\n",
                        inline=False)
        embed.add_field(name=f"{PREFIX}help command",
                        value="Show help details for the ",
                        inline=False)
        embed.add_field(name=f"{PREFIX}additem link",
                        value="Add new game to database\n",
                        inline=False)
        embed.add_field(name=f"{PREFIX}updateitem link",
                        value="Update item from database\n",
                        inline=False)
        embed.add_field(name=f"{PREFIX}getitem date",
                        value="Get item by month or year\n",
                        inline=False)
        embed.add_field(name=f"{PREFIX}removeitem name/link",
                        value="Remove item from database\n",
                        inline=False)

        embed.set_footer(text="By DilanDuck#4014")
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def help(self, ctx: commands.Context, command: str):
        embed = discord.Embed(
            title=HELP[command], description="\n\n", color=0xE60012)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.set_footer(text="By DilanDuck#4014")
        await ctx.send(embed=embed)
        await ctx.message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
