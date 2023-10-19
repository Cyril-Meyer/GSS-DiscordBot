import argparse
import discord
from discord.ext import tasks
import json

import gss


# Arguments
parser = argparse.ArgumentParser()
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
    status_update.start()


@tasks.loop(seconds=10.0)
async def status_update():
    for bot in config['bots']:
        guildid = bot['guildid']
        channelid = bot['channelid']

        channel = client.get_guild(guildid).get_channel(channelid)

        for server in bot['servers']:
            message = None
            if server['type'] == 'arma':
                server_status = gss.Arma3(server['ip'], server['port'])
                message = server_status.get_info()
            else:
                raise NotImplementedError
            await channel.send(message)


client.run(token)
