from discord.ext import commands
import os
import time
import traceback
import random
import asyncio #sleepを使うのに必要
import csv

#BOTの初期設定
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

f = open('NameList.csv', 'r', newline='')
r = csv.reader(f,delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
#必要な変数の定義
slot_list = ['<:element_tsutinoko:793148122653392937>', '<:habu:829971281754718240>', '<:resplendentquetzal:803594155451482113>', '<:prairiedog:793153927595163691>', '<:ruter:835556735791661056>','<:dolca:793155035902640170>','<:aardwolf:793155951381184601>']
ids_list = []
try:#csvファイルに中身があったら
    ids_list = list(next(r))
except:
    print("csvの中に何もない")
f.seek(0)#next(r)で進んでしまったイテレータを元に戻す

coin_dict = {row[0] : row[1] for row in r}#csvファイルの中身をcoin_dictの中に代入(内包表記を使用)

@bot.command()
async def slot(ctx):
    #関数内でグローバル変数に代入できるようにする
    global ids_list
    global coin_dict

    #抽選 & 結果の送信
    A = random.choice(slot_list)
    B = random.choice(slot_list)
    C = random.choice(slot_list)
    await ctx.send("%s%s%s" % (f"{A} ",f"{B} ",f"{C} "))

    #データべースを準備
    ids_list.append(ctx.author.id)#ユーザーに追加
    ids_list = list(set(ids_list))#ユーザーリストの重複を削除
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