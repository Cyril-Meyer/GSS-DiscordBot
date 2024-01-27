import datetime
import time
import telnetlib
import socket

import a2s
import discord
import mcstatus
import requests


class GSS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)

    def get_embed(self, desc):
        raise NotImplementedError


class TS3(GSS):
    def get_embed(self, desc):
        color = 0xff0000
        try:
            tn = telnetlib.Telnet(self.ip, self.port)
            if 'TeamSpeak'.encode() in tn.read_until('TeamSpeak'.encode(), timeout=1):
                color = 0x00ff00
            tn.close()
        except Exception as e:
            pass

        embed = discord.Embed(title=desc, color=color)
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/e/ec/TeamSpeak_logo_renovado.png')
        embed.add_field(name="Server information",
                        value=f"**IP** *{self.ip}*\n",
                        inline=False)
        embed.add_field(name="Last update",
                        value=f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                        inline=False)
        return embed


class A2S(GSS):
    def __init__(self, ip, port, qport=None):
        super().__init__(ip, port)
        if qport is not None:
            self.address = (self.ip, qport)

    def get_embed(self, desc, players_name=True):
        try:
            info = a2s.info(self.address)
            info_players = a2s.players(self.address)
            online = True
            color = 0x00ff00
        except Exception as e:
            online = False
            color = 0xff0000

        embed = discord.Embed(title=desc, color=color)

        if online:
            embed.add_field(name="Server information",
                            value=f"{info.server_name}\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Ping** *{f'{round(info.ping*1000)} ms'}*\n",
                            inline=False)

            players_message = f'{info.player_count}/{info.max_players}'

            if players_name:
                for i, p in enumerate(info_players):
                    if i > 32:
                        players_message = players_message + '\n and more...'
                        break

                    player = f'{p.name:.24} '
                    if p.duration < 3600:
                        player += f'{round(p.duration / 60)} m'
                    else:
                        player += f'{round(p.duration / 3600)} h'

                    players_message += f'\n{player}'

            embed.add_field(name="Current players",
                            value=players_message,
                            inline=False)
        else:
            embed.add_field(name="Server information",
                            value=f"**OFFLINE**\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n",
                            inline=False)
        embed.add_field(name="Last update",
                        value=f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                        inline=False)
        return embed


class Arma3(A2S):
    def __init__(self, ip, port, qport=None):
        if qport is None:
            qport = port + 1
        super().__init__(ip, port, qport)

    def get_embed(self, desc):
        embed = super().get_embed(desc)
        embed.set_thumbnail(url='https://arma3.com/assets/img/logos/arma3.png')

        return embed


class ProjectZomboid(A2S):
    def get_embed(self, desc):
        embed = super().get_embed(desc)
        embed.set_thumbnail(url='https://pzwiki.net/w/images/b/b7/PzLogo_BloodSplatter.png')

        return embed


class Enshrouded(A2S):
    def get_embed(self, desc):
        embed = super().get_embed(desc, players_name=False)
        embed.set_thumbnail(url='https://www.enshrouded.com/media/Meta/og-image-1200x628.jpg')

        return embed


class Minecraft(GSS):
    def get_embed(self, desc):
        try:
            server = mcstatus.JavaServer.lookup(f"{self.ip}:{self.port}")
            status = server.status()
            online = True
            color = 0x00ff00
        except Exception as e:
            online = False
            color = 0xff0000

        embed = discord.Embed(title=desc, color=color)
        embed.set_thumbnail(url='https://cdn.icon-icons.com/icons2/2699/PNG/512/minecraft_logo_icon_168974.png')

        if online:
            embed.add_field(name="Server information",
                            value=f"{status.description}\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Version** *{status.version.name}*\n"
                                  f"**Ping** *{f'{round(status.latency)} ms'}*\n",
                            inline=False)

            embed.add_field(name="Current players",
                            value=f"{status.players.online}/{status.players.max}",
                            inline=False)
        else:
            embed.add_field(name="Server information",
                            value=f"**OFFLINE**\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n",
                            inline=False)

        embed.add_field(name="Last update",
                        value=f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                        inline=False)
        return embed


class Eco(GSS):
    def get_embed(self, desc):
        try:
            server = requests.get(f'http://{self.ip}:{self.port+1}/info', timeout=1)
            if not server.status_code == 200:
                raise Exception
            latency = server.elapsed.total_seconds()*1000
            status = server.json()
            online = True
            color = 0x00ff00
        except Exception as e:
            online = False
            color = 0xff0000

        embed = discord.Embed(title=desc, color=color)
        embed.set_thumbnail(url='https://play.eco/assets/images/eco-logo.png')

        if online:
            embed.add_field(name="Server information",
                            value=f"{status['Description']}\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Version** *{status['Version']}*\n"
                                  f"**Ping** *{f'{round(latency)} ms'}*\n"
                                  f"**Time left** *{datetime.timedelta(seconds=round(status['TimeLeft']))}*\n",
                            inline=False)

            players_message = f"{status['OnlinePlayers']}/{status['TotalPlayers']}"

            for i, p in enumerate(status['OnlinePlayersNames']):
                if i > 32:
                    players_message = players_message + '\n and more...'
                    break
                players_message += f'\n{p:.24}'

            embed.add_field(name="Current players",
                            value=players_message,
                            inline=False)

        else:
            embed.add_field(name="Server information",
                            value=f"**OFFLINE**\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n",
                            inline=False)

        embed.add_field(name="Last update",
                        value=f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                        inline=False)
        return embed


class Bannerlord(GSS):
    def get_embed(self, desc):
        try:
            server = requests.get(f'http://{self.ip}:{self.port}/maps/list', timeout=1)
            if not server.status_code == 200:
                raise Exception
            latency = server.elapsed.total_seconds()*1000
            status = server.json()
            online = True
            color = 0x00ff00
        except Exception as e:
            online = False
            color = 0xff0000

        embed = discord.Embed(title=desc, color=color)
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/f/fe/Mount_%26_Blade_II_Bannerlord_logo.png')

        if online:
            embed.add_field(name="Server information",
                            value=f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Map** *{status['currentlyPlaying']}*\n"
                                  f"**Ping** *{f'{round(latency)} ms'}*\n",
                            inline=False)
        else:
            embed.add_field(name="Server information",
                            value=f"**OFFLINE**\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n",
                            inline=False)

        embed.add_field(name="Last update",
                        value=f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                        inline=False)
        return embed


class Paleworld(GSS):
    def get_embed(self, desc):
        try:
            message = "HELLO"
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
            sock.settimeout(1)  # 1s timeout

            t0 = time.time()
            sock.sendto(message.encode('utf-8'), self.address)
            data, address = sock.recvfrom(32)
            t1 = time.time()

            if not address == self.address:
                raise Exception
            if not len(data) >= 8:
                raise Exception

            latency = (t1 - t0) * 1000
            online = True
            color = 0x00ff00
        except Exception as e:
            online = False
            color = 0xff0000

        embed = discord.Embed(title=desc, color=color)
        embed.set_thumbnail(
            url='https://cdn.akamai.steamstatic.com/steam/apps/1623730/capsule_616x353.jpg')

        if online:
            embed.add_field(name="Server information",
                            value=f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Ping** *{f'{round(latency)} ms'}*\n",
                            inline=False)
        else:
            embed.add_field(name="Server information",
                            value=f"**OFFLINE**\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n",
                            inline=False)

        embed.add_field(name="Last update",
                        value=f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                        inline=False)
        return embed
