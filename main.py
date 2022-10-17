import os
import discord
import asyncio
import logging
from settings import *
from discord.ext import commands
from datetime import date


class DiscordBot(commands.Bot):
    def __init__(self):
        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.dm_messages = True
        intents.reactions = True

        super().__init__(command_prefix=PREFIX, help_command=None, intents=intents)

    async def on_ready(self):
        logging.basicConfig(filename=f"./Logs/{date.today()}.log",
                            level=logging.INFO,
                            format="%(asctime)s %(message)s")
        logging.info("Logged in as {0.user}".format(self))
        print("Logged in as {0.user}".format(self))
        await self.change_presence(status=discord.Status.online)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f"Error: Missing Required Argument // {error}")
            await ctx.message.delete()
            logging.info(f"Error: MissingRequiredArgument // {error}")
        elif isinstance(error, commands.BadArgument):
            await ctx.channel.send(f"Error: Bad Argument // {error}")
            await ctx.message.delete()
            logging.info(f"Error: Bad Argument // {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(f"Error: Missing Permissions // {error}")
            await ctx.message.delete()
            logging.info(f"Error: Missing Permissions // {error}")
        elif isinstance(error, commands.ChannelNotReadable):
            await ctx.channel.send(f"Error: Channel Not Readable // {error}")
            await ctx.message.delete()
            logging.info(f"Error: Channel Not Readable // {error}")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.channel.send(
                f"Sorry {ctx.author.mention}, but your not allowed to use this command in private message")
            logging.info(f"Error : No Private Message // {error}")
        else:
            logging.info(f"Error: Unknown // {error}")


async def load_extensions(bot: commands.Bot):
    """load all Cogs inside "Cogs" folder"""

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main(bot: commands.Bot, token):
    async with bot:
        await load_extensions(bot)
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main(DiscordBot(), TOKEN))
