import argparse
import json
import random
import string

import discord
from discord.ext import tasks

import gss
import utils


# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--refresh', type=float, help='Refresh rate (seconds)', default=30.0)
parser.add_argument('--token', type=str, help='discord token', default=None)
parser.add_argument('--print-guilds-info', action='store_true')
args = parser.parse_args()

if args.token is not None:
    token = args.token
else:
    with open('token.txt', 'r') as f:
        token = f.readline()

# Configuration file
with open('config.json', 'r') as f:
    config = json.load(f)
'''
# show bot configuration
for bot in config['bots']:
    print(bot)
    for server in bot['servers']:
        print(server)
'''

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'GSS bot logged in as {client.user}')

    # show bot servers and channels information
    if args.print_guilds_info:
        for guild in client.guilds:
            print('guild id  ', guild.id)
            print('guild name', guild.name)
            for channel in guild.text_channels:
                 print(f'> {channel.id:<22} {channel}')

    # delete older messages if not in messageid
    for bot in config['bots']:
        guildid = bot['guildid']
        channelid = bot['channelid']

        messageid_list = []
        for server in bot['servers']:
            messageid_list.append(server['messageid'])

        channel = client.get_guild(guildid).get_channel(channelid)
        messages = await channel.history(limit=64).flatten()

        for message in messages:
            if message.author.id == client.user.id and message.id not in messageid_list:
                await message.delete()

    # create loop for status messages
    print('GSS bot ready, starting tasks')
    await status_setup()
    status_update.start()


async def status_setup():
    for bot in config['bots']:
        guildid = bot['guildid']
        channelid = bot['channelid']

        channel = client.get_guild(guildid).get_channel(channelid)

        for server in bot['servers']:
            if server['type'] in ['ts3', 'arma3']:
                message_str = f'{server["desc"]} : status bot initialization...'
            else:
                raise NotImplementedError

            # try to get and edit messageid message
            try:
                message = await client.get_guild(guildid).get_channel(channelid).fetch_message(server['messageid'])
                await message.edit(content=message_str, embed=None)
            except Exception as e:
                message = await channel.send(message_str, embed=None)

            server['message'] = message


@tasks.loop(seconds=args.refresh)
async def status_update():
    print(f'GSS bot status update {random.choice(string.ascii_letters)}')
    for bot in config['bots']:
        for server in bot['servers']:
            if server['type'] == 'ts3':
                server_status = gss.TS3(server['ip'], server['port'])
                message = server_status.get_embed(server['desc'])
            elif server['type'] == 'arma3':
                server_status = gss.Arma3(server['ip'], server['port'])
                message = server_status.get_embed(server['desc'])
            else:
                raise NotImplementedError

            await server['message'].edit(content=None, embed=message)


@client.event
async def close():
    print(f'GSS closing')
    for bot in config['bots']:
        for server in bot['servers']:
            info = dict()
            info['IP'] = server['ip']
            info['PORT'] = server['port']
            message = utils.get_message(server['desc'], info)
            message += 'status bot closed...'
            await server['message'].edit(content=message, embed=None)
            # await server['message'].delete()


client.run(token)
