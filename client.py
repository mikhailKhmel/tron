import asyncio
import json

import pygame

from config import Config


class Client(object):

    def __init__(self):
        pygame.init()
        self.sc = pygame.display.set_mode(Config.window)
        pygame.display.update()


async def tcp_echo_client(message):

    reader, writer = await asyncio.open_connection(
        '', 9999)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    r = json.loads(data.decode())
    print('Close the connection')
    writer.close()

client = Client()
