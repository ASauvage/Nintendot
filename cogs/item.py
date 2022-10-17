import asyncio
import re
import discord
import requests
import logging
import sqlite3
from datetime import date, datetime
from discord.ext import commands


class Item(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = sqlite3.connect("database/database.db")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cogs/item loaded")

    @commands.command()
    async def additem(self, ctx: commands.Context, link: str):
        if link.startswith("https://www.nintendo.fr/") and link.endswith(".html"):
            console, title, release_date, image_link = get_value(link)

            if console == "NINTENDO_SWITCH":
                if datetime.strptime(release_date, "%d/%m/%Y") > datetime.today():
                    cursor = self.db.cursor()
                    cursor.execute(
                        f"SELECT rowid FROM Games WHERE (server_ID = '{ctx.guild.id}') AND (name = '{title}')")
                    res = cursor.fetchone()
                    if len(res) == 0:
                        embed = discord.Embed(title=title,
                                              description=f"Release date: {release_date}",
                                              color=0xE60012)
                        embed.set_image(url=image_link)
                        embed.set_footer(text="Response with yes/no")
                        await ctx.send(embed=embed)

                        try:
                            res = await self.bot.wait_for(
                                "message",
                                check=lambda x: x.channel.id == ctx.channel.id
                                and ctx.author.id == x.author.id
                                and x.content.lower() == "yes"
                                or x.content.lower() == "no",
                                timeout=30,
                            )
                        except asyncio.TimeoutError:
                            await ctx.send(
                                f"{ctx.author.mention}, you didn't send any message that meets the check in this channel for 30 seconds")
                            await ctx.message.delete()
                            return
                        else:
                            if res.content.lower() == "yes":

                                cursor.execute(
                                    f"INSERT INTO Games VALUES ('{ctx.guild.id}', '{title}', '{release_date}', '{image_link}', '{link}')")
                                self.db.commit()

                                await ctx.send(f"{title} was added to database")
                            else:
                                # TODO change an argument
                                await ctx.send("ok i pull up")
                    else:
                        await ctx.send(f"{title} is already present in database")
                else:
                    await ctx.send(f"{title} is already available !!!")
            else:
                await ctx.send("Something wrong... Be sure to chose a Nintendo Switch game")
        else:
            await ctx.send("Wrong link, please enter a link from https://www.nintendo.fr")
        await ctx.message.delete()

    @commands.command()
    async def getitem(self, ctx: commands.Context, search_date: str):
        pass

    @commands.command()
    async def updateitem(self, ctx: commands.Context, link: str):
        pass

    @commands.command()
    async def removeitem(self, ctx: commands.Context, link: str):
        if link.startswith("https://www.nintendo.fr/") and link.endswith(".html"):
            if console == "NINTENDO_SWITCH":
                cursor = self.db.cursor()
                console, title, release_date, image_link = get_value(link)

                embed = discord.Embed(title=f"Would you like to remove {title} from database ?",
                                      description=f"Release date: {release_date}",
                                      color=0xE60012)
                embed.set_image(url=image_link)
                embed.set_footer(text="Response with yes/no")
                await ctx.send(embed=embed)

                try:
                    res = await self.bot.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                        and ctx.author.id == x.author.id
                        and x.content.lower() == "yes"
                        or x.content.lower() == "no",
                        timeout=30,
                    )
                except asyncio.TimeoutError:
                    await ctx.send(
                        f"{ctx.author.mention}, you didn't send any message that meets the check in this channel for 30 seconds")
                    await ctx.message.delete()
                    return
                else:
                    if res.content.lower() == "yes":
                        cursor.execute(
                            f"DELETE FROM Games WHERE (server_ID = '{ctx.guild.id}') AND (link = '{link}')")
                        self.db.commit()

                        await ctx.send(f"{title} was remove from database")
                    else:
                        await ctx.send(f"{title} is still in database")
            else:
                await ctx.send("Something wrong... Be sure to chose a Nintendo Switch game")
        else:
            await ctx.send("Wrong link, please enter a link from https://www.nintendo.fr")
        await ctx.message.delete()


def get_value(link: str):
    source = requests.get(link)
    console = re.search(
        "(\"offdeviceConsoleType\":.{2,})\w", source.text)[0][25:]
    title = re.search("(\"gameTitle\":.{2,})\w", source.text)[0][14:]
    release_date = re.search("(releaseDate:.{2,})\w", source.text)[0][14:]
    image_link = re.search(
        "(class=\"img-responsive\" src=\".{2,})\w", source.text)[0][28:]

    return console, title, release_date, image_link


async def setup(bot: commands.Bot):
    await bot.add_cog(Item(bot))
