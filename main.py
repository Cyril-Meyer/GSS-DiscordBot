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
parser.add_argument('--refresh', type=float, help='Refresh rate (seconds)', default=10.0)
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

    # delete older messages
    for bot in config['bots']:
        guildid = bot['guildid']
        channelid = bot['channelid']

        channel = client.get_guild(guildid).get_channel(channelid)
        messages = await channel.history(limit=64).flatten()

        for m in messages:
            if m.author.id == client.user.id:
                await m.delete()

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
            if server['type'] == 'arma':
                message = f'{server["desc"]} : status bot initialization...'
            else:
                raise NotImplementedError

            message = await channel.send(message)
            server['message'] = message


@tasks.loop(seconds=args.refresh)
async def status_update():
    print(f'GSS bot status update {random.choice(string.ascii_letters)}')
    for bot in config['bots']:
        for server in bot['servers']:
            if server['type'] == 'arma':
                server_status = gss.Arma3(server['ip'], server['port'])
                message = utils.get_message(server['desc'], server_status.get_info())
            else:
                raise NotImplementedError

            await server['message'].edit(content=message)


client.run(token)
