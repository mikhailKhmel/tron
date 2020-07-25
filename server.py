import asyncio

from config import Config
from player import Player, PlayerEncoder

players = {}


def msg_info_about_players():
    res = str([PlayerEncoder().encode(players[i]) for i in range(len(players))])
    return res


def add_player():
    if len(players) < 4:
        players[len(players)] = Player(len(players))
        return msg_info_about_players()
    else:
        return '-1'


def update_players():
    for member in players.values():
        member.lightcycle['tail'].append(member.lightcycle['head'])
        member.lightcycle['head'] = [
            member.lightcycle['head'][0] + member.lightcycle['direction'][0],
            member.lightcycle['head'][1] + member.lightcycle['direction'][1]]


def check_game_over():
    res = 0
    for member in players.values():
        future_head = [member.lightcycle['head'][0] + member.lightcycle['direction'][0],
                       member.lightcycle['head'][1] + member.lightcycle['direction'][1]]
        if future_head in member.lightcycle['tail'] or future_head[0] < 0 or future_head[0] > Config.h_window \
                or future_head[1] < 0 or future_head[1] > Config.w_window:
            res += 1
            break
        else:
            for other_member in players.values():
                if member is other_member:
                    continue
                if future_head in other_member.lightcycle['tail']:
                    res += 1
    return True if res > 0 else False


def check_ready_all_players():
    c = 0
    for player in players.values():
        if player.ready:
            c += 1
    return True if c == len(players) else False


async def handle_msg(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')[0]

    print(f"Received {message!r} from {addr!r}")

    msg = ''

    if message.startswith('connect'):
        msg = add_player()
    # message = 'request_type:id:other_info'
    elif message.startswith('ready'):
        message_list = message.split(':')
        id = int(message_list[1])
        players[id].ready = True
        msg = msg_info_about_players()
    elif message.startswith('get_update'):
        if check_ready_all_players():
            if not check_game_over():
                update_players()
                msg = msg_info_about_players()
            else:
                msg = 'End Game'
                players.clear()
    elif message.startswith('new_direction'):
        message_list = message.split(':')
        id = int(message_list[1])
        message_list[2] = message_list[2].replace('[','')
        message_list[2] = message_list[2].replace(']', '')
        new_direction_str = message_list[2].split(',')
        new_direction = [int(new_direction_str[0]), int(new_direction_str[1])]
        players[id].lightcycle['direction'] = new_direction

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
