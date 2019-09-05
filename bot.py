# bot.py
import os
import random
import discord
from botdb import *
from dotenv import load_dotenv

# 1
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
usercheck = os.getenv('USER_DICT')
userdict={
    453053325105954816 : 617709678163525633, #Shadow
    193521437397614592 : 617709599658737707, #Bastet
    244509682712969217 : 617709511238483989, #Rapid
    284453956673994752 : 617709531421605927, #Merc
    96488405591953408 : 617709570831286303, #Hatsu
    249631916368723978 : 617709658278461442, #Dragon
    146832411798274049 : 617714450740281374, #Panda
    141441725871685632 : 617906178810183710 #Heart
    }


# 2
bot = commands.Bot(command_prefix='!')
database = None

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
    database = await open_pool("sqlite:///affection_module.db")
    await affection_check(database)
    await close_pool(database)

@bot.event
async def on_message(message):
    database = await open_pool("sqlite:///affection_module.db")
    if message.channel.type == discord.ChannelType.private and message.author != bot.user:
        aff_table = await affection_inc(database,message.author.id,message.author)
        print(aff_table)
        if message.author.id in userdict:
            channel = bot.get_channel(userdict[message.author.id])
        else:
            channel = bot.get_channel(617279982674116620)
        await channel.send(message.author)
        await channel.send(message.content)
    elif message.channel.type == discord.ChannelType.private and message.author == bot.user:
        aff_level = await check_aff_level(database, str(message.author.id))
        if int(aff_level[0][2]) >= 100:
            affection_state = await state_change(database, int(aff_level[0][2])+1)
            sql = """UPDATE affection SET affection_level = :level, username = :uname, state = :a_state WHERE userid = :id"""
            await database.execute(query=sql, values={"level":int(aff_level[0][2])+1,"uname":message.author,"a_state":affection_state,"id":message.author.id})
    await close_pool(database)
    await bot.process_commands(message)

@bot.command(name='lookatme')
async def look_at_me(ctx, targetid:int, repeat:int, format, message):
    target = bot.get_user(targetid)
    if target is not None:
        if target.dm_channel is None:
            await target.create_dm()
        for i in range(repeat):
            notice = await notice_me_text(message,format)
            await target.dm_channel.send(notice)

@bot.command(name="hellothere")
async def hello_there(ctx, channelid:int, repeat:int, format, message):
    channel = bot.get_channel(channelid)
    if channel is not None:
        for i in range(repeat):
            hello = await notice_me_text(message,format)
            await channel.send(hello)

@bot.command(name='thoseilove')
async def affection_table(ctx):
    database = await open_pool("sqlite:///affection_module.db")
    channel = bot.get_channel(618449496497455105)
    aff_return = await select_from(database, "affection")
    aff_list = []
    emp_str = ""
    trip_quote = '```'
    head_1 = 'UserID'
    head_2 = 'Love Muffin'
    head_3 = 'Affection Lvl'
    head_4 = 'Affection State'
    rowcount = 0
    aff_list.append(trip_quote)
    aff_list.append(f'    | {head_1:<20}| {head_2:<30}| {head_3:<15}| {head_4:<20}')
    aff_list.append(f'{emp_str:-<100}')
    for row in aff_return:
        aff_list.append(f'{rowcount+1:<4}| {row[0]:<20}| {row[1]:<30}| {row[2]:<15}| {row[3]:<20}')
        rowcount += 1
    aff_list.append(trip_quote)
    aff_table = "\n".join(aff_list)
    await channel.send(aff_table)
    await close_pool(database)

@bot.command(name="goodnight")
@commands.is_owner()
async def shutdown(ctx):
    await bot.logout()

bot.run(token)