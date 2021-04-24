from discord.ext import commands

import os

import traceback

import random

import asyncio #sleepを使うのに必要

bot = commands.Bot(command_prefix='/')

token = os.environ['DISCORD_BOT_TOKEN']

@bot.command()

async def slot(ctx):

  kakuritu = random.randint(1, 319)

  slot_list = ['<:element_tsutinoko:793148122653392937>', ':augreen:', ':aublue:', ':auyellow:', ':aublack:']

  A = random.choice(slot_list)

  B = random.choice(slot_list)

  C = random.choice(slot_list)

  if int(kakuritu) == int(1): #確率は1 /399

    await ctx.send("ボーナス確定！！！")

    await asyncio.sleep(3) #3秒間待ってやる

    i=0

    while i < random.randint(1, 5):

      await ctx.send("%s%s%s" % ("<:auyellow:824832834005893120>", "<:auyellow:824832834005893120>", "<:auyellow:824832834005893120>")) #7だけ出るように指定

      await asyncio.sleep(1)

      i += 1

  else:

    await ctx.send("%s%s%s" % (A, B, C))

bot.run(token)
