import asyncio
import json

import pygame

from config import Config

last_message = None

players = []

async def tcp_echo_client(message):
    global last_message
    global players
    reader, writer = await asyncio.open_connection('', 9999)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(1000000)
    print(f'Received: {data.decode()!r}')
    if data:
        d = data.decode()
        d = d.replace("[\'", '')
        d = d.replace("\']", '')
        d = d.replace("\'", '')
        l = d.split(', {')
        for i in range(1,len(l)):
            l[i] = '{' + l[i]
        players.clear()
        for p in l:
            players.append(json.loads(p))
        try:
            last_message = json.loads(d)
        except:
            pass
    print('Close the connection')
    writer.close()


class Client(object):

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.sc = pygame.display.set_mode(Config.window)
        asyncio.run(tcp_echo_client('connection'))
        if last_message == -1:
            exit(0)
        self.player = players[len(players)-1]['id']
        pygame.display.update()
        self.main_cycle()

    def render(self):
        for player in players:
            pygame.draw.rect(self.sc, player['color'],
                             (player['lightcycle']['head'][0] - 2, player['lightcycle']['head'][1] - 2, 5,
                              5))  # render head
            for tail in player['lightcycle']['tail']:  # render tails
                pygame.draw.rect(self.sc, player['color'], (tail[0], tail[1], 1, 1))
        # if type(last_message) == type(dict()):
        #     for player in last_message['light']:
        #         pass

    def main_cycle(self):
        previous_key = players[self.player]['lightcycle']['direction']
        while True:
            self.sc.fill((0, 0, 0))
            self.clock.tick(Config.speed)
            self.render()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        asyncio.run(tcp_echo_client('ready:' + str(self.player)))
                    elif i.key == pygame.K_UP:
                        if previous_key == [0, 1]:
                            continue
                        players[self.player]['lightcycle']['direction'] = [0, -1]
                        asyncio.run(tcp_echo_client('new_direction:' + str(players[self.player]['id']) + ':[0,-1]'))
                    elif i.key == pygame.K_DOWN:
                        if previous_key == [0, -1]:
                            continue
                        players[self.player]['lightcycle']['direction'] = [0, 1]
                        asyncio.run(tcp_echo_client('new_direction:' + str(players[self.player]['id']) + ':[0,1]'))
                    elif i.key == pygame.K_RIGHT:
                        if previous_key == [-1, 0]:
                            continue
                        players[self.player]['lightcycle']['direction'] = [1, 0]
                        asyncio.run(tcp_echo_client('new_direction:' + str(players[self.player]['id']) + ':[1,0]'))
                    elif i.key == pygame.K_LEFT:
                        if previous_key == [1, 0]:
                            continue
                        players[self.player]['lightcycle']['direction'] = [-1, 0]
                        asyncio.run(tcp_echo_client('new_direction:' + str(players[self.player]['id']) + ':[-1,0]'))
                    previous_key = players[self.player]['lightcycle']['direction']
            asyncio.run(tcp_echo_client('get_updates:' + str(players[self.player]['id'])))
            pygame.display.update()


client = Client()
