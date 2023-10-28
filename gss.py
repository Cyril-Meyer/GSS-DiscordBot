import datetime
import telnetlib

import a2s
import discord
import mcstatus


class GSS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

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


class Arma3(GSS):
    def get_embed(self, desc):
        address = (self.ip, self.port + 1)

        try:
            info = a2s.info(address)
            info_players = a2s.players(address)
            online = True
            color = 0x00ff00
        except Exception as e:
            online = False
            color = 0xff0000

        embed = discord.Embed(title=desc, color=color)
        embed.set_thumbnail(url='https://arma3.com/assets/img/logos/arma3.png')

        if online:
            embed.add_field(name="Server information",
                            value=f"{info.server_name}\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Ping** *{f'{round(info.ping*1000)} ms'}*\n",
                            inline=False)

            players_message = f'{info.player_count}/{info.max_players}'

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
        embed.set_thumbnail(url='https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/android-icon-192x192.png')

        if online:
            embed.add_field(name="Server information",
                            value=f"{status.description}\n"
                                  f"**IP** *{self.ip}*\n"
                                  f"**Port** *{self.port}*\n"
                                  f"**Version** *{status.version.name}*\n"
                                  f"**Ping** *{f'{round(status.latency*1000)} ms'}*\n",
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
