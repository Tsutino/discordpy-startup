from discord.ext import commands
import os
import traceback
import random
import asyncio #sleepを使うのに必要

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
slot_list = ['<:element_tsutinoko:793148122653392937>', '<:habu:829971281754718240>', '<:resplendentquetzal:803594155451482113>', '<:prairiedog:793153927595163691>', '<:ruter:835556735791661056>','<:dolca:793155035902640170>','<:aardwolf:793155951381184601>']

@bot.command()
async def slot(ctx):
  #抽選
  A = random.choice(slot_list)
  B = random.choice(slot_list)
  C = random.choice(slot_list)

  await ctx.send("%s%s%s" % (f"{A} ",f"{B} ",f"{C} "))
  #揃った場合
  if A==B==C:
    await ctx.send("スリーフレンズ！！！")

bot.run(token)
