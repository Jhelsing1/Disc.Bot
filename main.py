import os
import discord
import json
import random
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


bot = commands.Bot(command_prefix = '!')

TOKEN = os.environ.get('TOKEN')

@bot.command()
async def info(ctx):
  helpEmbed = discord.Embed(title = 'Command info' , description = 'Here are some commands avliable to you', color=0xFF5733)
  helpEmbed.add_field(name = '!playC4', value = 'Start a game of connect four. Requires two players. Work in progress', inline = False)
  helpEmbed.add_field(name = '!C4Help', value = 'View the rules and commands of Connect four.', inline = False)
  helpEmbed.add_field(name = '!playTTT', value = 'Start a game of tic tac toe. Requires two players.', inline = False)
  helpEmbed.add_field(name = '!TTTHelp', value = 'View the rules and commands of tic tac toe.', inline = False)
  helpEmbed.add_field(name = '!statsC4', value = 'View your win-loss and your most recent games of connect four. Work in progress', inline = False)
  helpEmbed.add_field(name = '!statsTTT', value = 'View your win-loss and your most recent games of tic tac toe. Work in progress', inline = False)
  await ctx.send(embed = helpEmbed)


@bot.command()
async def C4help(ctx):
  C4Embed = discord.Embed(title = 'Connect Four Help' , description = 'Basics of connect four and relevant commands', color=0x18FFEE)
  C4Embed.add_field(name = 'Goal of the game', value = 'To win, get four of your tokens to be in line with teachother, whether that\'d be diagonal, horizontal or vertically.', inline = False)
  C4Embed.add_field(name = 'How to play', value = 'Each player takes a turn dropping a token into a column, the token will drop to the bottom of the column. First to \" connect four\" wins. ', inline = False)
  C4Embed.add_field(name = 'Commands to play', value = '!drop (column number) to drop the token at the specified column, !forefit to forefit. To check your statis, please use !statsC4.', inline = False)
  await ctx.send(embed = C4Embed)

@bot.command()
async def TTThelp(ctx):
  TTTEmbed = discord.Embed(title = 'Tic Tac Toe Help' , description = 'Basics of Tic Tac Toe and relevant commands', color=0x77FF18)
  TTTEmbed.add_field(name = 'Goal of the game', value = 'To win, get three of your symbols in line, whether that\'d be diagonally, horizontally or vertically.', inline = False)
  TTTEmbed.add_field(name = 'How to play', value = 'Each player take turns marking a 3x3 square with ther symbol, First to mark 3 symbols together wins. ', inline = False)
  TTTEmbed.add_field(name = 'Commands to play', value = '!playTTT to start. All directions are listed in the game. To check your statis, please use !statsTTT.', inline = False)
  await ctx.send(embed = TTTEmbed)

#plays tic tac toe
@bot.command()
async def playTTT(ctx):
  board=['-','-','-','-','-','-','-','-','-']
  p1 = ctx.author.id
  p1_name = ctx.author
  await ctx.send(f"Player one confirmed as {p1_name}. Player two, please type \"playTTT\".")
  def check(m):
        return m.content == "playTTT" and m.channel == ctx.channel
  def board_check(auth):
        def inner_check(msg):
            if msg.author != auth:
              return False
            try:
              x = int(msg.content)
              if x <= 0 or x >= 10:
                return False
              return True
            except ValueError:
              return False
        return inner_check

  def check_filled(num):
    if board[num] == '-':
      return True
    return False
  def game_board(cp):
    gb = board[0]+'|'+board[1]+'|'+board[2]+'\n'+board[3]+'|'+board[4]+'|'+board[5]+'\n'+board[6]+'|'+board[7]+'|'+board[8]
    test_board = '1|2|3\n4|5|6\n7|8|9'
    brdEmbed = discord.Embed(title = f'Ongoing game,{p1_name} vs {p2_name}' , description = f'{cp}\'s turn, please enter a number between 1-9 ', color=0x7718FF)
    brdEmbed.add_field(name = 'Game Board', value = f'```{gb}```', inline = False)
    brdEmbed.add_field(name = 'Example board with correlating input values:', value = f'```{test_board}```', inline = False)
    brdEmbed.add_field(name = 'How to play:', value = f'enter the number between 1-9 which correlates to its position on the board. ', inline = False)
    return brdEmbed
  def wincond():
    if board[0] == board[1] and board[0] == board[2]:
      if board[0] == 'x': 
          return 1
      elif board[0] == 'o':
          return 2
    elif board[0] == board[3] and board[0] == board[6]:
      if board[0] == 'x': 
          return 1
      elif board[0] == 'o':
          return 2
    elif board[0] == board[4] and board[0] == board[8]:
      if board[0] == 'x': 
          return 1
      elif board[0] == 'o':
          return 2
    elif board[1] == board[4] and board[1] == board[7]:
        if board[1] == 'x': 
          return 1
        elif board[1] == 'o':
          return 2
    elif board[2] == board[5] and board[2] == board[8]:
        if board[2] == 'x': 
          return 1
        elif board[2] == 'o':
          return 2
    elif board[2] == board[4] and board[2] == board[6]:
        if board[2] == 'x': 
          return 1
        elif board[2] == 'o':
          return 2
    elif board[3] == board[4] and board[3] == board[5]:
        if board[3] == 'x': 
          return 1
        elif board[3] == 'o':
          return 2
    elif board[6] == board[7] and board[6] == board[8]:
        if board[6] == 'x': 
          return 1
        elif board[6] == 'o':
          return 2
    else:
      return 0

  msg = await bot.wait_for("message", check=check)
  p2 = msg.author.id
  p2_name = msg.author
  firs = random.randint(1,2)
  spaces = 0
  if firs == 1:
    await ctx.send(f"Randomizing go order, {p1_name} will go first.")
  elif firs == 2:
    await ctx.send(f"Randomizing go order, {p2_name} will go first.")


  while spaces in range(9): 
    if firs % 2 == 0:
      await ctx.send(embed = game_board(p2_name))
      k = 0
      while k == 0:
        mxg = await bot.wait_for('message',check = board_check(p2_name))
        if check_filled(int(mxg.content)-1):
          board[int(mxg.content)-1] = 'o'
          k += 1
          firs += 1

    elif firs % 2 == 1:
      k = 0
      await ctx.send(embed = game_board(p1_name))
      while k == 0:
        mxg = await bot.wait_for('message',check = board_check(p1_name))
        if check_filled(int(mxg.content)-1):
          board[int(mxg.content)-1] = 'x'
          k += 1
          firs += 1

    t = wincond()
    if t == 1:
      emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p1_name} for winning the game.', color=0xF5B041)
      await ctx.send(embed = emb)
      spaces = 9
    elif t == 2:
      emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p2_name} for winning the game.', color=0xF5B041)
      await ctx.send(embed = emb)
      spaces = 9
    elif spaces == 8:
       emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'It was a tie, thank you for playing.', color=0xF5B041)
       await ctx.send(embed = emb)
       
    spaces += 1

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

#178384103605927937


bot.run(os.getenv('TOKEN'))
