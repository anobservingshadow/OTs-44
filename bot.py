# bot.py
import os
import random
import discord
from dotenv import load_dotenv

# 1
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

async def text_format(text,format):
    if format == 'italic':
        return "*" + text + "*"
    elif format == 'bold':
        return "**" + text + "**"
    elif format == 'both':
        return "***" + text + "***"
    else:
        return text

async def random_caps(text):
    newtext = ''.join(random.choice((str.upper, str.lower))(x) for x in text)
    return newtext

async def notice_me_text(text,format):
    if format == 'bold':
        newtext = await text_format(text,'bold')
        return newtext
    elif format == 'italic':
        newtext = await text_format(text,'italic')
        return newtext
    elif format == 'both':
        newtext = await text_format(text,'both')
        return newtext
    elif format == 'cbold':
        captext = await random_caps(text)
        newtext = await text_format(captext,'bold')
        return newtext
    elif format == 'citalic':
        captext = await random_caps(text)
        newtext = await text_format(captext,'italic')
        return newtext
    elif format == 'cboth':
        captext = await random_caps(text)
        newtext = await text_format(captext,'both')
        return newtext
    else:
        return text

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    channel = bot.get_channel(617279982674116620)
    if message.channel.type == discord.ChannelType.private and message.author != bot.user:
        await channel.send(message.author)
        await channel.send(message.content)
    await bot.process_commands(message)

@bot.command(name='testing')
async def notice_me(ctx, targetid:int, repeat:int, format, message):

#    quotes = [
#        'Hey, hey~! Pay more attention to me, will you?',
#        "Who's that other girl you're talking to?", 
#        "**You didn't think you could just ignore me like that, did you?**"
#    ]
    target = bot.get_user(targetid)
    if target is not None:
        if target.dm_channel is None:
            await target.create_dm()
        for i in range(repeat):
            notice = await notice_me_text(message,format)
            await target.dm_channel.send(notice)

bot.run(token)