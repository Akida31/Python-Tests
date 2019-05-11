import asyncio
import discord
import youtube_dl
from discord.ext import commands
from itertools import cycle
import json
import os

TOKEN = '' # <- PUT HERE YOUR TOKEN
client = commands.Bot(command_prefix = '?')
status=['nicht, sondern hilft!', '?help','Viel Erfolg!']
client.remove_command('help')

extensions = ['fun']
players = {}
queues = {}

@client.event
@asyncio.coroutine 
async def on_ready():
    print('Bot is online!')

@asyncio.coroutine
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)
    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(5)

@client.event
@asyncio.coroutine
async def on_message(message):
    with open('users.json', 'r') as f: # <- CREATE BEFORE YOUR FIRST START THIS FILE
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)

    global author_global, channel_global
    channel = message.channel
    channel_global = channel
    author = message.author
    author_global = author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)

@asyncio.coroutine
async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

@asyncio.coroutine
async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

@asyncio.coroutine
async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end

@client.event
@asyncio.coroutine
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

    role = discord.utils.get(member.server.roles, name='Member')
    await client.add_roles(member, role)

@client.command(pass_context=True)
@asyncio.coroutine
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        title = 'Help',
        #description = 'Ich hoffe dir geht es gut ^^',
        colour = discord.Colour.dark_blue())
    embed.add_field(name='help', value='Helps you with hard commands!', inline=False)
    embed.add_field(name='ping', value='Returns Pong!', inline=False)
    embed.add_field(name='echo', value='Echos your text!', inline=False)
    embed.add_field(name='displayembed', value='Shows an example for an embed!', inline=False)
    embed.add_field(name='clear', value='Clears an amount of messages!', inline=False)
    embed.set_author(name='PythonBot')
    await client.send_message(author, embed=embed)
    await client.say(author.mention + ' Please look to your DM!')

@client.event
@asyncio.coroutine
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    print(channel,'{} deleted: {}'.format(author, content))
    #await client.send_message(channel,'{} deleted: {}'.format(author, content))

@client.command()
@asyncio.coroutine
async def ping():
    await client.say('Pong!')

@client.command()
@asyncio.coroutine
async def echo(*args):
    global author_global, channel_global
    author = author_global
    channel = channel_global
    output = ''
    for word in args:
        output += word + ' '
    await client.purge_from(channel, limit=1)
    await client.say(author.mention + ' '+ output)

@client.event
@asyncio.coroutine
async def on_reaction_add(reaction,user):
    channel = reaction.message.channel
    reaction_msg = '{} has added {} to the message: {}'.format(user.name,reaction.emoji,reaction.message.content)
    print(reaction_msg)
    await client.send_message(channel, reaction_msg)

@client.event
@asyncio.coroutine
async def on_reaction_remove(reaction,user):
    channel = reaction.message.channel
    reaction_msg = '{} has removed {} from the message: {}'.format(user.name,reaction.emoji,reaction.message.content)
    print(reaction_msg)
    await client.send_message(channel, reaction_msg)

@client.command()
@asyncio.coroutine
async def displayembed():
    global author_global
    embed = discord.Embed(
        title = 'Hallo',
        description = 'Ich hoffe dir geht es gut ^^',
        colour = discord.Colour.dark_blue())
    embed.set_footer(text='Bis später.')
    url = author_global.avatar_url
    embed.set_thumbnail(url=url)
    embed.set_author(name=author_global.name)
    await client.say(embed=embed)

@asyncio.coroutine
async def del_msg(channel, limit=1): 
    await client.purge_from(channel, limit=limit)

@client.command(pass_context=True)
@asyncio.coroutine
async def clear(ctx, amount=100):
    author = ctx.message.author
    channel = ctx.message.channel
    deleted = await client.purge_from(channel, limit=(amount+1))
    await client.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))
    

#LINKS
#https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.logs_from
#https://stackoverflow.com/questions/43561288/discord-py-how-to-get-logs-from-a-dm-channel
#https://youtu.be/udLRPEB1lks


#-------------------------MUSIC--------------
@client.command(pass_context=True)
@asyncio.coroutine
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    author = ctx.message.author
    if channel != None:
        await client.join_voice_channel(channel)
    else:
        await client.send_message(ctx.message.channel, author.mention + ', You have to be in a voice channel!')

@client.command(pass_context=True)
@asyncio.coroutine
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
@asyncio.coroutine
async def play(ctx, url):
    channel = ctx.message.channel
    server = ctx.message.server
    author = ctx.message.author
    voice_client = client.voice_client_in(server)
    await client.send_message(ctx.message.channel, author.mention + ' song added!')
    #player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    if not(server.id in players):
        players[server.id] = player
        player.start()
    #del_msg(channel)
    

@client.command(pass_context=True)
@asyncio.coroutine
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@client.command(pass_context=True)
@asyncio.coroutine
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
@asyncio.coroutine
async def skip(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
@asyncio.coroutine
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

def check_queue(id):
    print('next')
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()
        print('next')

#------------------------------------------------------------------------------------
# @client.command
# @asyncio.coroutine
# async def load(extension):
#     try:
#         client.load_extension(extension)
#         print('Loaded {}'.format(extension))
#     except Exception as error:
#         print('{} cannot be loaded. [{}]'.format(extension, error))

# @client.command
# @asyncio.coroutine
# async def unload(extension):
#     try:
#         client.unload_extension(extension)
#         print('Unloaded {}'.format(extension))
#     except Exception as error:
#         print('{} cannot be unloaded. [{}]'.format(extension, error))

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.loop.create_task(change_status())
    client.run(TOKEN)
