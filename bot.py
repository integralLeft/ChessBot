import discord
import asyncio
import logging
from discord.ext import commands
from discord.ext.commands import Bot
import traceback
import sys
import yaml

import numpy as np
import ast

from io import StringIO
import contextlib

import subprocess

import os
import discord
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#bot = commands.Bot(command_prefix='m!')

# below: manual input of token/guild vals
#TOKEN = input('Please enter the token: ')
#GUILD = input('Please enter the guild: ')

# client = discord.Client()

#stream = open('config.yaml')
#data = yaml.load(stream)

description = """beep boop I'm a bot that lets you play chess"""

extensions = ['cogs.game']
#discord_logger = logging.getLogger('discord')
#discord_logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.WARNING)
#handler = logging.FileHandler(filename='tz.log', encoding='utf-8', mode='w')
#log.addHandler(handler)
help_attrs = dict(hidden=True)


bot = commands.Bot(command_prefix='>', description=description, pm_help=None, help_attrs=help_attrs)


@bot.event
async def on_ready():
    print('logged in as: ')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    game = discord.Game("chess")
    await bot.change_presence(activity=game)



@bot.event
async def on_message(message):
    print('on_message')
    if message.author.bot and message.author.id != 334051580791750667: # allow corona bot to use chessbot
        return
    await bot.process_commands(message)





if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded {extension}.")
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__,e))
    bot.run(TOKEN, bot=True, reconnect=True)

    #handlers = log.handlers[:]
    #for hdlr in handlers:
        #hdlr.close()
        #log.removeHandler(hdlr)


servers = {
    "scftf" : {"general": 542493636248469531,
               "burner_channel" : 727054721789198357
    },
    "ME" : {"general" : 302953345105002496,
            "specific" : 688805196612239429,
            "serious" : 377935738316128256,
            "software" : 289085592653004801,
            "meta" : 316211369559195648,
            "gaming" : 255071268338925568,
            "bots" : 232245773448773633,
            "media" : 320180014207336459,
            "wholesome" : 484095865183797260,
            "homework" : 606652330276028436,
            "minecraft" : 535379067210563584,
            "memes_disc" : 383163730453856256,
            "pol_memes" : 686266664169373793,
            "weeb" : 498346809295634462,
            "meme_pit" : 263300751986655232,
            "shitposting" : 300377971234177024,
            "history" : 257296403435487242,
            "events" : 303891514361118720,
            "police" : 267150859605901314,
            "voice" : 474798151371587610
    }
}

@bot.command(name='send')
async def send(ctx, guild, channel, message):
    if ctx.guild != bot.get_guild(542493635757867037):
        return
    channel = bot.get_channel(servers[guild][channel])
    await channel.send(message)

@bot.command(name='hi')
async def hello(ctx):
    response = 'Hi, <@' + str(ctx.author.id) + '>!'
    await ctx.send(response, delete_after=5)

@bot.command(name='eval')
async def evaluate(ctx, message):
    await ctx.send(ast.literal_eval(message))

# exec rarted output shit
from io import StringIO
import contextlib
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
@bot.command(name='exec')
async def execute(ctx, message):
    with stdoutIO() as s:
        exec(message)
    await ctx.send(s.getvalue())
'''





#################################
########## CURSED AREA ##########
#################################

inline_bot = discord.Client()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# cursed inline bot messaging lol
@inline_bot.event
async def on_message(message):
    content = message.content
    if content.find('evaluate(') != -1:
        print('inline message received!')
        start_expr_index = content.index('evaluate(') + len('evaluate(')
        end_expr_index = content.rfind(')', start_expr_index)
        expression = content[start_expr_index:end_expr_index]
        result = eval(expression)
        await message.channel.send(result)
    # exec rarted output shit
    elif content.find('exec(') != -1:
        print('inline message received!')
        start_expr_index = content.index('exec(') + len('exec(')
        end_expr_index = content.rfind(')', start_expr_index)
        if end_expr_index == -1:
            await message.channel.send("You fucked up and forgot your closing parenthesis.")
        else:
            expression = content[start_expr_index:end_expr_index]
            with stdoutIO() as s:
                exec('print(' + expression + ')')
            await message.channel.send(s.getvalue())



inline_bot.run(TOKEN)
'''
