from discord.ext import commands
import os
import traceback
import random
import asyncio #sleepを使うのに必要
import psycopg2
import psycopg2.extras

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
url = os.environ['DATABASE_URL']

def setDictionary():
  conn = psycopg2.connect(url)
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("""select * from discordbot_table;""")
  r = cur.fetchall()
  dict_result={dict(row)["ids"] : dict(row)["coins"] for row in r}
  return dict_result

def updateTable(userID, coinNumber):
  cur.execute("UPDATE discordbot_table SET coins = '%s' WHERE ids='%s';", (coinNumber , userID))
  cur.execute("SELECT * FROM discordbot_table;")
  cur.fetchone()
  conn.commit()

slot_list = ['<:element_tsutinoko:793148122653392937>', '<:habu:829971281754718240>', '<:resplendentquetzal:803594155451482113>', '<:prairiedog:793153927595163691>', '<:ruter:835556735791661056>','<:dolca:793155035902640170>','<:aardwolf:793155951381184601>']
dict_result = setDictionary()
@bot.command()
async def slot(ctx):
  global dict_result
  userID = str(ctx.author.id)
  #抽選
  A = random.choice(slot_list)
  B = random.choice(slot_list)
  C = random.choice(slot_list)
  await ctx.send(f"{A} {B} {C}")
  #揃った場合
  if A==B==C:
    await ctx.send("スリーフレンズ！！！")
    dict_result[userID] = int(dict_result[userID]) + 100
    dict_result = setDictionary()
    updateTable((int(userID)),dict_result[userID])
bot.run(token)
