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

inline_bot = discord.Client()

@bot.event
async def on_ready():
    print('logged in as: ')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    game = discord.Game("chess")
    await bot.change_presence(activity=game)

"""
@bot.event
async def on_message(message):
    game = bot.get_cog('Game')
    if message == game.draw_message:
        print("the message is game.draw_message!")
        reactionlist = ['✅', '❌']
        def check(reaction, user):
            print('checking for reaction validity...')
            return user == bot.get_user(game.opposingPlayer.id) and str(reaction) in reactionlist
        try:
            print('trying to wait for reaction...')
            reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            print('draw offer timed out...')
            await game.draw_message.channel.send('Draw offer timed out.', delete_after=5)
        else:
            print('made it to the else block...')
            if str(reaction) == reactionlist[0]:
                await game.draw_message.delete()
                embed_title = 'Game over. ' + str(game.player.username) + ' and ' + str(game.opposingPlayer.username) + ' have agreed to a draw.'
                await game.Update_Message(ctx, embed_title=embed_title, edit=True)
                self.Reset()
            elif str(reaction) == reactionlist[1]:
                await game.draw_message.delete()
                await game.draw_message.channel.send('Draw offer declined.', delete_after=5)
"""

@bot.event
async def on_message(message):
    print('on_message')
    if message.author.bot and message.author.id != 334051580791750667: # allow corona bot to use chessbot
        return
    await bot.process_commands(message)

# cursed inline bot messaging lol
@inline_bot.event
async def on_message(message):
    if 'evaluate(' in message:
        print('inline message received!')
        start_expr_index = message.index('evaluate(') + len('evaluate(')
        end_expr_index = message.find(')', start_expr_index)
        expression = message[start_expr_index:end_expr_index]
        await ctx.send(ast.literal_eval(expression))

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

"""
@commands.command()
async def load(extension_name : str, ctx):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("'''py\n{}; {}\n'''".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))
"""

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

"""
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
)
"""


"""

def eval(s,op):
    lst = []
    for i in s:
        if i.isnumeric():
            lst.append(int(i))
    if op == 'add':
        return sum(lst)
    elif op == 'mult':
        result = 1
        for i in lst:
            result *= i
        return result

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    cmddict = {'greet':'Hi, ' + message.author.name + '!',
               'gay':'no u',
               'm!':'haha yes very funny',
               'fuck':'wow haha i am dying of laughter',
               'daily':'wrong prefix idiot. not tatsumaki smdh',
               '':"that's not a command dumbass, that's the absence of a command. smdh",
               'help':'Commands:\n\t1. greet (prints a greeting)\n\t2. gay (no u)\n\t3. add (adds ints in input)\n\t4. mult (multiplies ints in input)'}
    prefix = 'm!'
    if message.content[:len(prefix)] == prefix:
        body = message.content[len(prefix):]
        if body[:3] == 'add':
            response = eval(message.content, 'add')
        elif body[:4] == 'mult':
            response = eval(message.content, 'mult')
        elif body not in cmddict:
            response = 'enter a valid command dumbass'
        else:
            response = cmddict[body]
        await message.channel.send(response)

client.run(TOKEN)
#bot.run(TOKEN)
"""
