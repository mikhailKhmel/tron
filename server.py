import asyncio
import json

from player import Player, PlayerEncoder

players = {}


def add_player(addr):
    if len(players) < 4:
        players[addr] = Player()
        r = PlayerEncoder().encode(players[addr])
        return r


async def handle_msg(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')[0]

    print(f"Received {message!r} from {addr!r}")

    msg = ''
    if message.startswith('connect'):
        msg = add_player(addr)

    writer.write(msg.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(handle_msg, '', 9999)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


asyncio.run(main())
