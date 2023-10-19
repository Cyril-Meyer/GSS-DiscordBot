import a2s


class GSS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_info(self):
        raise NotImplementedError


class Arma3(GSS):
    def get_info(self):
        output = dict()
        output['IP'] = self.ip
        output['PORT'] = self.port
        address = (self.ip, self.port+1)

        try:
            info = a2s.info(address)
            info_players = a2s.players(address)
            output['STATUS'] = 'ONLINE'
        except Exception as e:
            output['STATUS'] = 'OFFLINE'
            return output

        output['SERVER NAME'] = info.server_name
        output['PING'] = f'{round(info.ping*1000)} ms'
        output['PLAYERS'] = []
        output['PLAYERS'].append(f'{info.player_count}/{info.max_players}')

        for p in info_players:
            player = f'{p.name:.16} '
            if p.duration < 3600:
                player += f'{round(p.duration/60)} m'
            else:
                player += f'{round(p.duration/3600)} h'
            output['PLAYERS'].append(player)

        return output
