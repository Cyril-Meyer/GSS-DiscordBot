import argparse
import discord

parser = argparse.ArgumentParser()
parser.add_argument('--token', type=str, help='discord token', default=None)
args = parser.parse_args()

if args.token is not None:
    token = args.token
else:
    with open('token.txt') as f:
        token = f.readline()


intents = discord.Intents.default()
# intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'logged in as {client.user}')

    '''
    # get bot information
    for guild in client.guilds:
        print('guild id  ', guild.id)
        print('guild name', guild.name)
        for channel in guild.text_channels:
             print(f'> {channel.id:<22} {channel}')
    '''

client.run(token)
