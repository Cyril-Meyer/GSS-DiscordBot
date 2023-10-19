import a2s


class GSS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_info(self):
        raise NotImplementedError


class Arma3(GSS):
    def get_info(self):
        output = ''
        address = (self.ip, self.port+1)

        info = a2s.info(address)
        output += f'{info.server_name}\n'
        output += f'{"ping :":<10} {round(info.ping*1000)}ms\n'
        output += f'{"joueurs :":<10} {info.player_count}/{info.max_players}\n'

        info = a2s.players(address)
        for p in info:
            output += f'> {p.name:<16} {round(p.duration/3600)}h\n'
        return output
