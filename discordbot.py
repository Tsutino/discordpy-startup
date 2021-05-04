from discord.ext import commands
from discord.ext import tasks
import discord
import os
import traceback
import random
import asyncio #sleepを使うのに必要
import psycopg2
import psycopg2.extras
import time
from datetime import datetime
import schedule

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = 721885806125645844

url = os.environ['DATABASE_URL']
conn = psycopg2.connect(url)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("""select * from discordbot_table;""")
r = cur.fetchall()
dict_result={dict(row)["ids"] : dict(row)["coins"] for row in r}
cur.close()
conn.close()

def setTable(userID, coinNumber):
  conn = psycopg2.connect(url)
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("INSERT INTO discordbot_table (ids, coins) VALUES (%s, %s);", (userID, coinNumber))
  cur.execute("SELECT * FROM discordbot_table;")
  cur.fetchone()
  conn.commit()
  cur.close()
  conn.close()

def updateTable(userID, coinNumber):
  conn = psycopg2.connect(url)
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("UPDATE discordbot_table SET coins = '%s' WHERE ids='%s';", (coinNumber , userID))
  cur.execute("SELECT * FROM discordbot_table;")
  cur.fetchone()
  conn.commit()
  cur.close()
  conn.close()

channel_sent = None
slot_list = ['<:element_tsutinoko:793148122653392937>', '<:habu:829971281754718240>', '<:resplendentquetzal:803594155451482113>', '<:prairiedog:793153927595163691>', '<:ruter:835556735791661056>','<:dolca:793155035902640170>','<:aardwolf:793155951381184601>']

@bot.command()
async def slot(ctx):
  global dict_result
  userID = str(ctx.author.id)
  #抽選
  A = random.choice(slot_list)
  B = random.choice(slot_list)
  C = random.choice(slot_list)
  await ctx.send(f"{A} {B} {C}")
  if userID not in dict_result:
    setTable(userID,0)
  #揃った場合
  if A==B==C:
    await ctx.send("スリーフレンズ！！！")
    await ctx.send(f"{ctx.author}さんに+100コイン！")
    dict_result[userID] = int(dict_result[userID]) + 100
    updateTable((int(userID)),dict_result[userID])

@bot.command()
async def coin(ctx):
  global dict_result
  userID = str(ctx.author.id)
  await ctx.send(f"{ctx.author}さんのコイン枚数は{dict_result[userID]}枚です")

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    dt = datetime.now().weekday()
    if now == '20:45' and dt == 1:
      　channel = bot.get_channel(CHANNEL_ID)
        await channel.send('今日は道場越し！')  

#ループ処理実行
loop.start()

bot.run(token)
