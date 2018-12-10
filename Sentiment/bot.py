import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from analysis import *


adminID = ""
Client = discord.Client()
bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_message(message):
    sentiments = getSentiment(message.content)
    print(sentiments)
    for sentiment in sentiments:
        if sentiment <= -0.2:
            await bot.send_message(message.channel, ":), be nice")
            f = open("log.txt", "a")
            f.write("%s:%s\n"%(message.author, message.content))
            f.close()
        elif sentiment >= 0.9:
            await bot.send_message(message.author, "You are a nice person!")

while True:
    bot.run('NTIxMzYxNDA4MTY4OTUxODEx.Du7Tlw.yqPBzlsrcgcjcaBP1vMsYzUqZrE')
