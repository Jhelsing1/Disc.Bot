import os
import discord
from discord.ext import commands


if not os.environ.get("TOKEN"):
    from dotenv import load_dotenv
    load_dotenv()
bot = commands.Bot(command_prefix = '!')

TOKEN = os.environ.get("TOKEN")

@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)

@bot.command()
async def CMD(ctx):
  helpEmbed = discord.Embed(title = "Command Menu" , description = "Here are all avliable commands. Note that to call a command, you must attach a '!' in front.", color = discord.Color.dark_gold)
  helpEmbed.add_field(name = "!playC4", value = "Start a game of connect four. Requires two players.", inline = False)
  helpEmbed.add_field(name = "!C4Help", value = "View the rules and commands of Connect four.", inline = False)
  helpEmbed.add_field(name = "!playTTT", value = "Start a game of tic tac toe. Requires two players.", inline = False)
  helpEmbed.add_field(name = "!TTTHelp", value = "View the rules and commands of tic tac toe.", inline = False)
  helpEmbed.add_field(name = "!statsC4", value = "View your win-loss and your most recent games of connect four.", inline = False)
  helpEmbed.add_field(name = "!statsTTT", value = "View your win-loss and your most recent games of tic tac toe.", inline = False)
  await ctx.send(embed = helpEmbed)























bot.run(os.getenv('TOKEN'))