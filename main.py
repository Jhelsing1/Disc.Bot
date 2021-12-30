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
  helpEmbed.add_field(name = '!playC4', value = 'Start a game of connect four. Requires two players.', inline = False)
  helpEmbed.add_field(name = '!C4Help', value = 'View the rules and commands of Connect four.', inline = False)
  helpEmbed.add_field(name = '!playTTT', value = 'Start a game of tic tac toe. Requires two players.', inline = False)
  helpEmbed.add_field(name = '!TTTHelp', value = 'View the rules and commands of tic tac toe.', inline = False)
  helpEmbed.add_field(name = '!statsC4', value = 'View your win-loss and your most recent games of connect four. Work in progress', inline = False)
  helpEmbed.add_field(name = '!statsTTT', value = 'View your win-loss and your most recent games of tic tac toe. Work in progress', inline = False)
  await ctx.send(embed = helpEmbed)

@bot.command()
async def statsC4(ctx):
  absp = os.path.abspath('UserStats.json')
  with open(absp, 'r') as f:
    UserStats = json.load(f)
  user = str(ctx.message.author.id)
  await update_user_data(UserStats,user)
  W = UserStats[user]['win_C4']
  L = UserStats[user]['Loss_C4']
  statsEmbed = discord.Embed(title = f"{ctx.message.author.name}'s current stats", description = 'Current connect four win/loss:')
  statsEmbed.add_field(name = 'Wins: ', value = f'${W}')
  statsEmbed.add_field(name = 'Losses: ', value = f'${L}')
  await ctx.send(embed = statsEmbed)
  with open(absp, 'w') as f:
    json.dump(UserStats, f)

@bot.command()
async def statsTTT(ctx):

  with open('UserStats.json', 'r') as f:
    UserStats = json.load(f)
  user = str(ctx.message.author.id)
  await update_user_data(UserStats,user)
  W = UserStats[user]['win_TTT']
  L = UserStats[user]['Loss_TTT']
  T = UserStats[user]['Tie_TTT']
  statsEmbed = discord.Embed(title = f"{ctx.message.author.name}'s current stats", description = 'Current connect four win/loss:')
  statsEmbed.add_field(name = 'Wins: ', value = f'${W}')
  statsEmbed.add_field(name = 'Losses: ', value = f'${L}')
  statsEmbed.add_field(name = 'Ties: ', value = f'${T}')
  await ctx.send(embed = statsEmbed)
  with open('UserStats.json', 'w') as f:
    json.dump(UserStats, f)

@bot.command()
async def C4help(ctx):
  C4Embed = discord.Embed(title = 'Connect Four Help' , description = 'Basics of connect four and relevant commands', color=0x18FFEE)
  C4Embed.add_field(name = 'Goal of the game', value = 'To win, get four of your tokens to be in line with teachother, whether that\'d be diagonal, horizontal or vertically.', inline = False)
  C4Embed.add_field(name = 'How to play', value = 'Each player takes a turn dropping a token into a column, the token will drop to the bottom of the column. First to \" connect four\" wins. ', inline = False)
  C4Embed.add_field(name = 'Commands to play', value = '!playC4 to start. All directions are listed in the game. To check your statis, please use !statsC4.', inline = False)
  await ctx.send(embed = C4Embed)

@bot.command()
async def TTThelp(ctx):
  TTTEmbed = discord.Embed(title = 'Tic Tac Toe Help' , description = 'Basics of Tic Tac Toe and relevant commands', color=0x77FF18)
  TTTEmbed.add_field(name = 'Goal of the game', value = 'To win, get three of your symbols in line, whether that\'d be diagonally, horizontally or vertically.', inline = False)
  TTTEmbed.add_field(name = 'How to play', value = 'Each player take turns marking a 3x3 square with ther symbol, First to mark 3 symbols together wins. ', inline = False)
  TTTEmbed.add_field(name = 'Commands to play', value = '!playTTT to start. All directions are listed in the game. To check your statis, please use !statsTTT.', inline = False)
  await ctx.send(embed = TTTEmbed)

async def update_user_data(UserStats,user):
  user_id = str(user)
  if user_id not in UserStats:
    UserStats[user_id] = {}
    UserStats[user_id]['win_TTT'] = 0
    UserStats[user_id]['Loss_TTT'] = 0
    UserStats[user_id]['Tie_TTT'] = 0
    UserStats[user_id]['win_C4'] = 0
    UserStats[user_id]['Loss_C4'] = 0

async def update_win_Loss(UserStats,user,game,WL):
  if game == 'C4':
    if WL == 'W':
      UserStats[user]['win_C4'] += 1
    else:
      UserStats[user]['Loss_C4'] += 1
  else:
    if WL == 'W':
      UserStats[user]['win_TTT'] += 1
    elif WL == 'L':
      UserStats[user]['Loss_TTT'] += 1
    else:
      UserStats[user]['Tie_TTT'] += 1

#plays tic tac toe
@bot.command()
async def playTTT(ctx):

  with open('UserStats.json', 'r') as f:
    UserStats = json.load(f)

  board=['-','-','-','-','-','-','-','-','-']
  p1_name = ctx.author
  p1 = ctx.author.id
  
  await update_user_data(UserStats, p1)

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
  p2_name = msg.author
  p2 = msg.author.id
  await update_user_data(UserStats, p2)
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
      await update_win_Loss(UserStats,p1,'TTT','W')
      await update_win_Loss(UserStats,p2,'TTT','L')

      await ctx.send(embed = emb)
      spaces = 9
    elif t == 2:
      emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p2_name} for winning the game.', color=0xF5B041)
      await update_win_Loss(UserStats,p2,'TTT','W')
      await update_win_Loss(UserStats,p1,'TTT','L')

      await ctx.send(embed = emb)
      spaces = 9
    elif spaces == 8:
       emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'It was a tie, thank you for playing.', color=0xF5B041)
       await update_win_Loss(UserStats,p2,'TTT','Tie')
       await update_win_Loss(UserStats,p1,'TTT','Tie')

       await ctx.send(embed = emb)
       
    spaces += 1
  with open('UserStats.json', 'w') as f:
        json.dump(UserStats, f)

@bot.command()
async def playC4(ctx):

  with open('UserStats.json', 'r') as f:
    UserStats = json.load(f)

  board=[['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-']]
  next_empty = [0,0,0,0,0,0,0]
  p1_name = ctx.author
  p1 = ctx.author.id
  await ctx.send(f"Player one confirmed as {p1_name}. Player two, please type \"playC4\".")

  await update_user_data(UserStats, p1)

  def check(m):
        return m.content == "playC4" and m.channel == ctx.channel

  msg = await bot.wait_for("message", check=check)
  p2_name = msg.author
  p2 = msg.author.id
  await update_user_data(UserStats, p2)
  firs = random.randint(1,2)
  if firs == 1:
    await ctx.send(f"Randomizing go order, {p1_name} will go first.")
  elif firs == 2:
    await ctx.send(f"Randomizing go order, {p2_name} will go first.")
  
  
  def game_board(cp):
    gb = board[0][5] + '|'+ board[1][5] + '|'+board[2][5] + '|'+board[3][5] + '|'+board[4][5] + '|'+board[5][5] + '|'+board[6][5] + '\n'
    gb += board[0][4] + '|'+ board[1][4] + '|'+board[2][4] + '|'+board[3][4] + '|'+board[4][4] + '|'+board[5][4] + '|'+board[6][4] + '\n'
    gb += board[0][3] + '|'+ board[1][3] + '|'+board[2][3] + '|'+board[3][3] + '|'+board[4][3] + '|'+board[5][3] + '|'+board[6][3] + '\n'
    gb += board[0][2] + '|'+ board[1][2] + '|'+board[2][2] + '|'+board[3][2] + '|'+board[4][2] + '|'+board[5][2] + '|'+board[6][2] + '\n'
    gb += board[0][1] + '|'+ board[1][1] + '|'+board[2][1] + '|'+board[3][1] + '|'+board[4][1] + '|'+board[5][1] + '|'+board[6][1] + '\n'
    gb += board[0][0] + '|'+ board[1][0] + '|'+board[2][0] + '|'+board[3][0] + '|'+board[4][0] + '|'+board[5][0] + '|'+board[6][0] 
    brdEmbed = discord.Embed(title = f'Ongoing game,{p1_name} vs {p2_name}' , description = f'{cp}\'s turn, please enter a number between 1-7 ', color=0x7718FF)
    brdEmbed.add_field(name = 'Game Board', value = f'```{gb}```', inline = False)
    brdEmbed.add_field(name = 'Enter the column number to drop token in that column', value = '```1 | 2 | 3 | 4 | 5 | 6 | 7```', inline = False)
    brdEmbed.add_field(name = 'How to play:', value = f'enter the number between 1-7 which correlates to the column on the board to drop the token, connect 4 tokens to win. ', inline = False)
    return brdEmbed

  def board_check(auth):
        def inner_check(msg):
            if msg.author != auth:
              return False
            try:
              x = int(msg.content)
              if x <= 0 or x >= 8:
                return False
              return True
            except ValueError:
              return False
        return inner_check

  def check_filled(num):
    if next_empty[num] == 6:
      return False
    if board[num][next_empty[num]] == '-':
      return True
    return False

  def wicd(dir,token, num, row, col):
    try:
      if board[col][row] != token:
        return False
    except IndexError:
      return False
    if dir == 'D':
      try:
        x = num
        if board[col][row-1] == token and x == 3:
          return True
        elif board[col][row-1] == token and x < 3:
          return wicd(dir,token, x + 1, row-1, col)
        elif x >= 4:
          return False
      except IndexError:
        return False
    
    elif dir == 'L':
      try:
        x = num
        if board[col-1][row] == token and x == 3:
          return True
        elif board[col-1][row] == token and x < 3:
          return wicd(dir,token, x + 1, row, col-1)
        elif x >= 4:
          return False
      except IndexError:
        return False

    elif dir == 'R':
      try:
        x = num
        if board[col+1][row] == token and x == 3:
          return True
        elif board[col+1][row] == token and x < 3:
          return wicd(dir,token, x + 1, row+1, col)
        elif x >= 4:
          return False
      except IndexError:
        return False
    
    elif dir == 'TL':
      try:
        x = num
        if board[col-1][row+1] == token and x == 3:
          return True
        elif board[col-1][row+1] == token and x < 3:
          return wicd(dir,token, x + 1, row+1, col-1)
        elif x >= 4:
          return False
      except IndexError:
        return False

    elif dir == 'TR':
      try:
        x = num
        if board[col+1][row+1] == token and x == 3:
          return True
        elif board[col+1][row+1] == token and x < 3:
          return wicd(dir,token, x + 1, row+1, col+1)
        elif x >= 4:
          return False
      except IndexError:
        return False
    
    elif dir == 'BL':
      try:
        x = num
        if board[col-1][row-1] == token and x == 3:
          return True
        elif board[col-1][row-1] == token and x < 3:
          return wicd(dir,token, x + 1, row-1, col-1)
        elif x >= 4:
          return False
      except IndexError:
        return False

    elif dir == 'BR':
      try:
        x = num
        if board[col+1][row-1] == token and x == 3:
          return True
        elif board[col+1][row-1] == token and x < 3:
          return wicd(dir,token, x + 1, row-1, col+1)
        elif x >= 4:
          return False
      except IndexError:
        return False

  def wincond(ldc, token):
        if wicd('D',token,1,next_empty[ldc]-1,ldc):
          return True
        elif wicd('L',token,1,next_empty[ldc]-1,ldc):
          return True
        elif wicd('R',token,1,next_empty[ldc]-1,ldc):
          return True
        elif wicd('TL',token,1,next_empty[ldc]-1,ldc):
          return True
        elif wicd('TR',token,1,next_empty[ldc]-1,ldc):
          return True
        elif wicd('BL',token,1,next_empty[ldc]-1,ldc):
          return True
        elif wicd('BR',token,1,next_empty[ldc]-1,ldc):
          return True
        
        elif wicd('L',token,1,next_empty[ldc]-1,ldc+1):
          return True
        elif wicd('BL',token,1,next_empty[ldc],ldc+1):
          return True
        elif wicd('TL',token,1,next_empty[ldc]-2,ldc+1):
          return True
        elif wicd('R',token,1,next_empty[ldc]-1,ldc-1):
          return True
        elif wicd('BR',token,1,next_empty[ldc],ldc-1):
          return True
        elif wicd('TR',token,1,next_empty[ldc]-2,ldc-1):
          return True
        else:
          return False

  spaces = 0
  while spaces in range(42): 

    if firs % 2 == 0:
      await ctx.send(embed = game_board(p2_name))
      k = 0
      while k == 0:
        mxg = await bot.wait_for('message',check = board_check(p2_name))
        if check_filled(int(mxg.content)-1):
          board[int(mxg.content)-1][next_empty[int(mxg.content)-1]] = 'o'
          k += 1
          firs += 1
          next_empty[int(mxg.content)-1] += 1

          if wincond(int(mxg.content)-1, 'o'):
            emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p2_name} for winning the game.', color=0xF5B041)
            await ctx.send(embed = emb)
            spaces = 100

            await update_win_Loss(UserStats,p2,'C4','W')
            await update_win_Loss(UserStats,p1,'C4','L')

    elif firs % 2 == 1:
      k = 0
      await ctx.send(embed = game_board(p1_name))
      while k == 0:
        mxg = await bot.wait_for('message',check = board_check(p1_name))
        if check_filled(int(mxg.content)-1):
          board[int(mxg.content)-1][next_empty[int(mxg.content)-1]] = 'x'
          k += 1
          firs += 1
          next_empty[int(mxg.content)-1] += 1

          if wincond(int(mxg.content)-1, 'x'):
            emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p1_name} for winning the game.', color=0xF5B041)
            await ctx.send(embed = emb)
            spaces = 100

            await update_win_Loss(UserStats,p1,'C4','W')
            await update_win_Loss(UserStats,p2,'C4','L')
       
    spaces += 1

  with open('UserStats.json', 'w') as f:
        json.dump(UserStats, f)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

bot.run(os.getenv('TOKEN'))