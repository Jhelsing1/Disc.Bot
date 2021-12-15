import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '!')
TOKEN = os.environ.get("DISCORD_TOKEN")

@bot.command()
async def hello(ctx):
  await ctx.reply('Hello!')



bot.run(os.getenv('TOKEN'))