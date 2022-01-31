from decimal import DivisionByZero
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
  helpEmbed.add_field(name = '!statsC4', value = 'View your win-loss and your most recent games of connect four.', inline = False)
  helpEmbed.add_field(name = '!statsTTT', value = 'View your win-loss and your most recent games of tic tac toe.', inline = False)
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
  LG = UserStats[user]['Last_games_C4']
  sp = UserStats[user]['C4_LastGame']
  statsEmbed = discord.Embed(title = f"{ctx.message.author.name}'s current stats", description = 'Current connect four win/loss:',color = 0x45B39D)
  statsEmbed.add_field(name = 'Wins: ', value = f'{W}')
  statsEmbed.add_field(name = 'Losses: ', value = f'{L}')
  LG_P = ''
  if sp == 0:
    LG_P = LG[0].split(';')
    G = LG[1].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
    G = LG[2].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
  elif sp == 1:
    LG_P = LG[1].split(';')
    G = LG[2].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
    G = LG[0].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
  else:
    LG_P = LG[2].split(';')
    G = LG[0].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
    G = LG[1].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
  x = 0
  while x in range(6):
    if LG_P[x] == 'W':
      LG_P[x] = 'Won'
    elif LG_P[x] == 'L':
      LG_P[x] = 'Loss'
    x += 1

  statsEmbed.add_field(name = 'Last Games ', value = f'{LG_P[1]} vs {LG_P[0]},{LG_P[3]} vs {LG_P[2]}, {LG_P[5]} vs {LG_P[4]}')

  await ctx.send(embed = statsEmbed)
  with open(absp, 'w') as f:
    json.dump(UserStats, f)

@bot.command()
async def statsTTT(ctx):
  absp = os.path.abspath('UserStats.json')
  with open(absp, 'r') as f:
    UserStats = json.load(f)
  user = str(ctx.message.author.id)
  await update_user_data(UserStats,user)
  W = UserStats[user]['win_TTT']
  L = UserStats[user]['Loss_TTT']
  T = UserStats[user]['Tie_TTT']
  LG = UserStats[user]['Last_games_TTT']
  sp = UserStats[user]['TTT_LastGame']
  statsEmbed = discord.Embed(title = f"{ctx.message.author.name}'s current stats", description = 'Current connect four win/loss:',color = 0x45B39D)
  statsEmbed.add_field(name = 'Wins: ', value = f'{W}')
  statsEmbed.add_field(name = 'Losses: ', value = f'{L}')
  statsEmbed.add_field(name = 'Ties: ', value = f'{T}')

  LG_P = ''
  if sp == 0:
    LG_P = LG[0].split(';')
    G = LG[1].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
    G = LG[2].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
  elif sp == 1:
    LG_P = LG[1].split(';')
    G = LG[2].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
    G = LG[0].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
  else:
    LG_P = LG[2].split(';')
    G = LG[0].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
    G = LG[1].split(';')
    LG_P.append(G[0])
    LG_P.append(G[1])
  x = 0
  while x in range(6):
    if LG_P[x] == 'W':
      LG_P[x] = 'Won'
    elif LG_P[x] == 'L':
      LG_P[x] = 'Loss'
    elif LG_P[x] == 'T':
      LG_P[x] = 'Tie'
    x += 1

  statsEmbed.add_field(name = 'Last Games ', value = f'{LG_P[1]} vs {LG_P[0]},{LG_P[3]} vs {LG_P[2]}, {LG_P[5]} vs {LG_P[4]}')

  await ctx.send(embed = statsEmbed)
  with open(absp, 'w') as f:
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

@bot.command()
async def BDhelp(ctx):
  TTTEmbed = discord.Embed(title = 'Bomb Defusal Help' , description = 'Basics of Bomb Defusal and relevant commands', color=0x77FF18)
  TTTEmbed.add_field(name = 'Goal of the game', value = 'To win, find the word by guessing letters.', inline = False)
  TTTEmbed.add_field(name = 'How to play', value = 'The player guesses a word, one letter each until the word is revealed or the player gets seven strikes, it\s hangman basically. ', inline = False)
  TTTEmbed.add_field(name = 'Commands to play', value = '!playBD to start. All directions are listed in the game. To check your statis, please use !stats_BD.', inline = False)
  await ctx.send(embed = TTTEmbed)

async def update_user_data(UserStats,user):
  user_id = str(user)
  if user_id not in UserStats:
    UserStats[user_id] = {}
    UserStats[user_id]['win_TTT'] = 0
    UserStats[user_id]['Loss_TTT'] = 0
    UserStats[user_id]['Tie_TTT'] = 0
    UserStats[user_id]['Last_games_TTT'] = ['- -','- -','- -']
    UserStats[user_id]['TTT_LastGame'] = 0
    UserStats[user_id]['win_C4'] = 0
    UserStats[user_id]['Loss_C4'] = 0
    UserStats[user_id]['Last_games_C4'] = ['- -','- -','- -']
    UserStats[user_id]['C4_LastGame'] = 0
    UserStats[user_id]['Win_DB'] = 0
    UserStats[user_id]['Loss_DB'] = 0
    UserStats[user_id]['Total_DB'] = 0

async def update_win_Loss(UserStats,user,game,WL,p2):
  if game == 'C4':
    if WL == 'W':
      UserStats[user]['win_C4'] += 1
      str = p2.name + ' W'

      UserStats[user]['Last_games_C4'][UserStats[user]['C4_LastGame']] = str
      if UserStats[user]['C4_LastGame'] == 2:
        UserStats[user]['C4_LastGame'] = 0
      else:
        UserStats[user]['C4_LastGame'] += 1

    else:
      UserStats[user]['Loss_C4'] += 1

      str = p2.name + ' L'
      UserStats[user]['Last_games_C4'][UserStats[user]['C4_LastGame']] = str
      if UserStats[user]['C4_LastGame'] == 2:
        UserStats[user]['C4_LastGame'] = 0
      else:
        UserStats[user]['C4_LastGame'] += 1

  else:
    if WL == 'W':
      UserStats[user]['win_TTT'] += 1

      str = p2.name + ' W'
      UserStats[user]['Last_games_TTT'][UserStats[user]['TTT_LastGame']] = str
      if UserStats[user]['TTT_LastGame'] == 2:
        UserStats[user]['TTT_LastGame'] = 0
      else:
        UserStats[user]['TTT_LastGame'] += 1

    elif WL == 'L':
      UserStats[user]['Loss_TTT'] += 1

      str = p2.name + ' L'
      UserStats[user]['Last_games_TTT'][UserStats[user]['TTT_LastGame']] = str
      if UserStats[user]['TTT_LastGame'] == 2:
        UserStats[user]['TTT_LastGame'] = 0
      else:
        UserStats[user]['TTT_LastGame'] += 1

    else:
      UserStats[user]['Tie_TTT'] += 1

      str = p2.name + ' T'
      UserStats[user]['Last_games_TTT'][UserStats[user]['TTT_LastGame']] = str
      if UserStats[user]['TTT_LastGame'] == 2:
        UserStats[user]['TTT_LastGame'] = 0
      else:
        UserStats[user]['TTT_LastGame'] += 1

async def update_win_Loss_DB(UserStats,user,WL):
  if WL == 'W':
    UserStats[user]['Win_DB'] += 1
    UserStats[user]['Total_DB'] += 1
  else:
    UserStats[user]['Loss_DB'] += 1
    UserStats[user]['Total_DB'] += 1

@bot.command()
async def stats_BD(ctx):
  absp = os.path.abspath('UserStats.json')
  with open(absp, 'r') as f:
    UserStats = json.load(f)
  user = str(ctx.message.author.id)
  await update_user_data(UserStats,user)
  W = UserStats[user]['Win_DB']
  L = UserStats[user]['Loss_DB']
  T = UserStats[user]['Total_DB']
  statsEmbed = discord.Embed(title = f"{ctx.message.author.name}'s current stats", description = 'Current Bomb Defusal win/loss:',color = 0x45B39D)
  statsEmbed.add_field(name = 'Wins: ', value = f'{W}')
  statsEmbed.add_field(name = 'Losses: ', value = f'{L}')
  statsEmbed.add_field(name = 'Total Games: ', value = f'{T}', inline = False)
  try:
    k = float(W/T)
  except:
    k = 0
  statsEmbed.add_field(name = 'Win percentage: ', value = f'{k}', inline = False)
  await ctx.send(embed = statsEmbed)

#plays tic tac toe
@bot.command()
async def playTTT(ctx):
  absp = os.path.abspath('UserStats.json')
  with open(absp, 'r') as f:
    UserStats = json.load(f)

  board=['-','-','-','-','-','-','-','-','-']
  p1_name = ctx.author
  p1 = str(ctx.author.id)
  
  await update_user_data(UserStats, p1)

  await ctx.send(f"Player one confirmed as {p1_name}. Player two, please type \"playTTT\".")
  def check(m):
        return m.content == "playTTT" and m.channel == ctx.channel
  def board_check(auth):
        def inner_check(msg):
            if msg.author != auth:
              return False
            try:
              if msg.content == 'abort':
                return True
              x = int(msg.content)
              if x <= 0 or x >= 10:
                return False
              return True
            except ValueError:
              return False
        return inner_check

  def abrt_check(auth):
    def inner_check(msg):
      if msg.author != auth:
        return False
      if msg.content == 'abort' or msg.content == 'cancel':
        return True
      else: 
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
    brdEmbed.add_field(name = 'How to play:', value = f'enter the number between 1-9 which correlates to its position on the board. When it\'s your turn, you can start the aborting process by typing \'abort\'.', inline = False)
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
  p2 = str(msg.author.id)
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
        if mxg.content == 'abort':
          await ctx.send(f"Abort vote detected, {p1_name} please type \"abort\" to cancel the match or \"cancel \" to continue playing.")
          mtg = await bot.wait_for('message',check = abrt_check(p1_name))
          if mtg.content == 'abort':
            k += 1
            await ctx.send("Game aborted")
            spaces = 10
          else:
            await ctx.send(embed = game_board(p2_name))
        else:
          if check_filled(int(mxg.content)-1):
            board[int(mxg.content)-1] = 'o'
            k += 1
            firs += 1

    elif firs % 2 == 1:
      k = 0
      await ctx.send(embed = game_board(p1_name))
      while k == 0:
        mxg = await bot.wait_for('message',check = board_check(p1_name))
        if mxg.content == 'abort':
          await ctx.send(f"Abort vote detected, {p2_name} please type \"abort\" to cancel the match or \"cancel \" to continue playing.")
          mtg = await bot.wait_for('message',check = abrt_check(p2_name))
          if mtg.content == 'abort':
            k += 1
            await ctx.send("Game aborted")
            spaces = 10
          else:
            await ctx.send(embed = game_board(p1_name))
        else:
          if check_filled(int(mxg.content)-1):
            board[int(mxg.content)-1] = 'x'
            k += 1
            firs += 1

    t = wincond()
    if t == 1:
      emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p1_name} for winning the game.', color=0xF5B041)
      await ctx.send(embed = emb)
      spaces = 9
      await update_win_Loss(UserStats,p1,'TTT','W',p2_name)
      await update_win_Loss(UserStats,p2,'TTT','L',p1_name)

    elif t == 2:
      emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p2_name} for winning the game.', color=0xF5B041)
      await ctx.send(embed = emb)
      spaces = 9
      await update_win_Loss(UserStats,p2,'TTT','W',p1_name)
      await update_win_Loss(UserStats,p1,'TTT','L',p2_name)

    elif spaces == 8:
       emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'It was a tie, thank you for playing.', color=0xF5B041)
       await ctx.send(embed = emb)
       await update_win_Loss(UserStats,p2,'TTT','Tie',p1_name)
       await update_win_Loss(UserStats,p1,'TTT','Tie',p2_name)
       
    spaces += 1
  with open(absp, 'w') as f:
        json.dump(UserStats, f)

@bot.command()
async def playC4(ctx):
  absp = os.path.abspath('UserStats.json')
  with open(absp, 'r') as f:
    UserStats = json.load(f)

  board=[['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-']]
  next_empty = [0,0,0,0,0,0,0]
  p1_name = ctx.author
  p1 = str(ctx.author.id)
  await ctx.send(f"Player one confirmed as {p1_name}. Player two, please type \"playC4\".")

  await update_user_data(UserStats, p1)

  def check(m):
        return m.content == "playC4" and m.channel == ctx.channel

  msg = await bot.wait_for("message", check=check)
  p2_name = msg.author
  p2 =str(msg.author.id)
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
    brdEmbed.add_field(name = 'How to play:', value = f'enter the number between 1-7 which correlates to the column on the board to drop the token, connect 4 tokens to win. When it\'s your turn, you can start the aborting process by typing \'abort\'.', inline = False)
    return brdEmbed

  def board_check(auth):
        def inner_check(msg):
            if msg.author != auth:
              return False
            try:
              if msg.content == 'abort':
                return True
              x = int(msg.content)
              if x <= 0 or x >= 8:
                return False
              return True
            except ValueError:
              return False
        return inner_check

  def abrt_check(auth):
    def inner_check(msg):
      if msg.author != auth:
        return False
      if msg.content == 'abort' or msg.content == 'cancel':
        return True
      else: 
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
        if mxg.content == 'abort':
          await ctx.send(f"Abort vote detected, {p1_name} please type \"abort\" to cancel the match or \"cancel \" to continue playing.")
          mtg = await bot.wait_for('message',check = abrt_check(p1_name))
          if mtg.content == 'abort':
            k += 1
            await ctx.send("Game aborted")
            spaces = 100
          else:
            await ctx.send(embed = game_board(p2_name))
        else:
          if check_filled(int(mxg.content)-1):
            board[int(mxg.content)-1][next_empty[int(mxg.content)-1]] = 'o'
            k += 1
            firs += 1
            next_empty[int(mxg.content)-1] += 1

            if wincond(int(mxg.content)-1, 'o'):
              emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p2_name} for winning the game.', color=0xF5B041)
              await ctx.send(embed = emb)
              spaces = 100

              await update_win_Loss(UserStats,p2,'C4','W',p1_name)
              await update_win_Loss(UserStats,p1,'C4','L',p2_name)

    elif firs % 2 == 1:
      k = 0
      await ctx.send(embed = game_board(p1_name))
      while k == 0:
        mxg = await bot.wait_for('message',check = board_check(p1_name))
        if mxg.content == 'abort':
          await ctx.send(f"Abort vote detected, {p2_name} please type \"abort\" to cancel the match or \"cancel \" to continue playing.")
          mtg = await bot.wait_for('message',check = abrt_check(p2_name))
          if mtg.content == 'abort':
            k += 1
            await ctx.send("Game aborted")
            spaces = 100
          else:
            await ctx.send(embed = game_board(p1_name))
        else:
          if check_filled(int(mxg.content)-1):
            board[int(mxg.content)-1][next_empty[int(mxg.content)-1]] = 'x'
            k += 1
            firs += 1
            next_empty[int(mxg.content)-1] += 1

            if wincond(int(mxg.content)-1, 'x'):
              emb = discord.Embed(title = f'Concluded game,{p1_name} vs {p2_name}' , description = f'Congratulations to {p1_name} for winning the game.', color=0xF5B041)
              await ctx.send(embed = emb)
              spaces = 100

              await update_win_Loss(UserStats,p1,'C4','W',p2_name)
              await update_win_Loss(UserStats,p2,'C4','L',p1_name)
       
    spaces += 1

  with open(absp, 'w') as f:
        json.dump(UserStats, f)

@bot.command()
async def word_defusal(ctx):

  absp = os.path.abspath('UserStats.json')
  with open(absp, 'r') as f:
    UserStats = json.load(f)
  p1_name = ctx.author
  p1 = str(ctx.author.id)

  await update_user_data(UserStats, p1)

  wrd_file = open('words.txt', 'r')
  wrd_dict = wrd_file.readlines()
  wv = random.randint(0,853)
  cw = wrd_dict[wv]
  print(cw)
  already_guessed = []
  current_displayline = []
  k = 0
  while k < len(cw)-1:
    current_displayline.append('_')
    k+=1
  strikes = [':white_large_square:',':white_large_square:',':white_large_square:',':white_large_square:',':white_large_square:',':white_large_square:',':white_large_square:']
  strikes_num = 0

  cw1 = []
  for x in cw:
    if len(cw1)<= len(cw)-1:
     cw1.append(x)

  def gameboard():
    x = 7 - strikes_num
    k = ""
    h = ""
    for a in strikes:
      k += a + " "
    for g in current_displayline:
      h += g
    brdembed = discord.Embed(title = f'{p1_name} is trying to defuse the bomb!' , description = 'A bomb\'s been planted and its code is not 7355608! Guerss the word to defuse it!', color=0x7718FF)
    brdembed.add_field(name = 'Timer', value = f'{k}', inline = False)
    brdembed.add_field(name = 'Word', value = f'```{h}```', inline = False)
    brdembed.add_field(name = 'Already Guessed keys:', value = f'```{already_guessed}```', inline = False)
    brdembed.add_field(name = 'Info:', value = f'You have {x} lives left until the timer runs out, so you\'d better choose your letters carefully!', inline = False)
    brdembed.add_field(name = 'How to play:', value = 'Enter a letter by itself to try it for the code. Keep at it until the code is set! You can also walk away by writing \'abort\'.', inline = False)
    return brdembed
  
  def wrdcheck(msg):
    if msg.author  == p1_name:
      x = msg.content
      if len(x) == 1 and x.isalpha():
        return True
      elif x == 'abort':
        return True
      else:
        return False
    else:
      return False

  def abrtcheck(msg):
    if msg.author  == p1_name:
      x = msg.content
      if x.lower() == 'y' or x.lower():
        return True
      else:
        return False
    else:
      return False

  def wincond():
    if strikes_num == 7:
      return 'l'
    gx = 0
    for item in cw1:
      if item == '':
        gx+=1
    if gx == len(cw)-1:
      return 'w'
    else:
      return 'x'

  G = 0
  eg = 0
  while G == 0 and strikes_num < 7 and eg == 0:
      await ctx.send(embed = gameboard())
      mxg = await bot.wait_for('message',check = wrdcheck)
      if mxg.content == 'abort':
        await ctx.send("Are you sure you want to abort this game? Y/N")
        mtg = await bot.wait_for('message',check = abrtcheck)
        if mtg.content.lower() == 'y':
          await ctx.send("Game aborted")
          G = 8
          strikes_num  == 100
        else: 
          await ctx.send("The game goes on!")
          await ctx.send(embed = gameboard)
      else:
        el = mxg.content.lower()
        if el in already_guessed:
          await ctx.send("Letter already guessed, try again!")
        else:
          if el not in cw1:
            strikes_num += 1 
            x = 7 - strikes_num
            await ctx.send(f"Uh oh! Wrong input! You only have {x} attempts left!")
            already_guessed.append(el)
            strikes[strikes_num-1] = ':red_square:'
            if wincond() == 'l':
              await update_win_Loss_DB(UserStats,p1,'L')
              emb = discord.Embed(title = 'Bomb Detonated!' , description = 'You blew up spetacularly! Don\'t worry, it was all a dream :), or was it?', color=0xF5B041)
              emb.add_field(name = 'Code Word:',value = f'The code ward was {cw}')
              await ctx.send(embed = emb)
              strikes_num = 8
          else:
            while el in cw1:
              ind = cw1.index(el)
              current_displayline[ind] = el
              cw1[ind] = ''
            await ctx.send("Good call!")
            already_guessed.append(el)
            if wincond() == 'w':
              await update_win_Loss_DB(UserStats,p1,'W')
              emb = discord.Embed(title = 'Bomb Defused!' , description = 'Congratulations, you didn\'t blow up!', color=0xF5B041)
              emb.add_field(name = 'Code Word:',value = f'The code ward was {cw}')
              await ctx.send(embed = emb)
              eg = 1
            elif wincond() == 'l':
              await update_win_Loss_DB(UserStats,p1,'L')
              emb = discord.Embed(title = 'Bomb Detonated!' , description = 'You blew up spetacularly! Don\'t worry, it was all a dream :), or was it?', color=0xF5B041)
              emb.add_field(name = 'Code Word:',value = f'The code ward was {cw}')
              await ctx.send(embed = emb)
              strikes_num = 8

  with open(absp, 'w') as f:
    json.dump(UserStats, f)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

bot.run(os.getenv('TOKEN'))