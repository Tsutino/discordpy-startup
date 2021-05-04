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

slot_list = ['<:element_tsutinoko:793148122653392937>', '<:habu:829971281754718240>', '<:resplendentquetzal:803594155451482113>', '<:prairiedog:793153927595163691>', '<:ruter:835556735791661056>','<:dolca:793155035902640170>','<:aardwolf:793155951381184601>']

coin_dict = {row[0] : row[1] for row in r}#csvファイルの中身をcoin_dictの中に代入(内包表記を使用)

@bot.command()
async def slot(ctx):
    #関数内でグローバル変数に代入できるようにする
    global coin_dict

    #抽選 & 結果の送信
    A = random.choice(slot_list)
    B = random.choice(slot_list)
    C = random.choice(slot_list)
    await ctx.send(f"{A} {B} {C}")

    #データべースを準備
    coin_dict.setdefault(str(ctx.author.id), 0)#ユーザーの財布を作成

    if A==B==C:#揃った場合
        await ctx.send("スリーフレンズ！！！")#揃った旨を通知
        coin_dict[str(ctx.author.id)] = int(coin_dict[str(ctx.author.id)]) + 100#コインを追加

    #csvに書き込み
    g = open('NameList.csv', 'w', newline='')
    wg = csv.writer(g)
    for s in coin_dict:
        wg.writerow([s , coin_dict[s]])

bot.run(token)


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
    
bot.run(token)
