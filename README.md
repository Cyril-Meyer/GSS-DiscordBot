# GSS-DiscordBot
Game Server Status Discord Bot

### Usage

* Create a `token.txt` file and place your Discord bot token inside.
  * you can also use the `--token` parameter instead.
* Edit the example `config.json` file to work with your Discord channels and game servers.
  * For each discord channel, you need to create a `bot` entry in the `bots` list.
    * `guildid` (`--print-guilds-info` display all the server and channel IDs the bot belongs to)
    * `channelid`
    * `servers`
  * For each game server, you need to create a `server` entry in the `servers` list.
    * `type`
    * `ip`
    * `port`
    * `desc`
  * Currently, the supported game servers are:
    * arma
    * In theory and with a few modifications: any server supporting [Valve's Server Query Protocol](https://developer.valvesoftware.com/wiki/Server_queries)
    thanks to [python-a2s](https://github.com/Yepoleb/python-a2s).

```
usage: main.py [-h] [--refresh REFRESH] [--token TOKEN] [--print-guilds-info]

optional arguments:
  -h, --help           show this help message and exit
  --refresh REFRESH    Refresh rate (seconds)
  --token TOKEN        discord token
  --print-guilds-info
```

**setup venv and install dependency**
```
python -m venv venv
# windows
.\venv\Scripts\activate.bat
pip install -U pip
pip install discord.py==1.7.3
pip install python-a2s==1.3.0
```

**run with docker**
```
docker build -t gssdiscordbot .
docker run --rm -it -d --name gssdiscordbot-container gssdiscordbot

# view logs
docker logs -f gssdiscordbot-container

# stop container
docker attach gssdiscordbot-container
- CTRL+C -
```
