from pkgutil import get_data
import sqlite3
import logging
from tokenize import String
import discord
from settings import *
from datetime import date


class Reminder(discord.Client):
    def __init__(self):
        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.dm_messages = True
        intents.reactions = True

        super().__init__(intents=intents)
        db = sqlite3.connect("database/database.db")
        self.allowed_mentions = discord.AllowedMentions.all

    async def send_ping(self):
        guilds_data = self.get_guilds_data()

        for guild in guilds_data:
            games_data = self.get_games_data(guild[0])
            channel = self.get_channel(guild[1])

            if len(games_data) > 0:
                await channel.send(content=f"@Test {len(games_data)} game(s) out today", allowed_mentions=self.allowed_mentions)

                for game in games_data:
                    embed = discord.Embed(title=f"{game[0]}",
                                          description=f"Release date: {game[1]}",
                                          color=0xE60012)
                    embed.set_image(url=game[2])
                    embed.set_footer(text=game[3])
                    await channel.send(embed=embed)

    def get_games_data(self, guild_id: String):
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT name, date, image_path, link FROM Games WHERE (server_ID = '{guild_id}') AND (date = '{date.today.strftime('%d/%m/%y')}')")
        res = cursor.fetchall()
        cursor.close()
        return res

    def get_guilds_data(self):
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT server_ID, channel_ID, role_ID FROM Guild_Info")
        res = cursor.fetchall()
        cursor.close()
        return res


reminder = Reminder()
reminder.run(TOKEN)
