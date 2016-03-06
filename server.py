import json

from websocket_server import WebsocketServer
from kernel import Game

connections = {}
users = {'names': ["Martin", "Ashton"]}


def status_check(func):
    def wraper(client, server, message, *args, **kwargs):
        msg = json.loads(message)
        print(message)
        if msg['status'] == 0:
            server.send_message_to_all(json.dumps(str(users['names'])))
            users['names'].append(msg['name'])
            client['status'] = msg['status']
            client['name'] = msg['name']
        elif msg['status'] == 1:
            p_point = msg['point']
            print(p_point)
            playerVsComputer(client, server, p_point)

    return wraper


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    if client['name'] in users['names']:
        users['names'].remove(client['name'])
        server.send_message_to_all(str(users['names']))
    if client['id'] in connections.keys():
        del connections[connections[client['id']]]
        del connections[client['id']]
    print("Client(%d) disconnected" % client['id'])
    print(connections)


def connect_clients(id1, id2):
    connections[id1] = id2
    connections[id2] = id1


def get_client(id):
    for c in server.clients:
        if c['id'] == id:
            return c
    print('Sorry client terminated his connection.')


def playerVsComputer(client, server, p_point):
    if client['game'] is None:
        client['game'] = Game()
    # posielam spravu v tvare: {'status': 1, 'point': [1,1]}
    point = client['game'].create_point(p_point)

    c_point = client['game'].play(point)  # kernel computes his move
    server.send_message(client, str(c_point))  # server sends msg to user
    print(c_point)


def playerVsPlayer(client, server, message):
    if client['game'] is None:
        client['game'] = Game()
    point = client['game'].create_point(message)

    if client['id'] in connections:
        id = connections[client['id']]  # finds game partner
        server.send_message(get_client(id), str(point))  # sends msg to game partner
    else:
        c_point = client['game'].play(point)  # kernel computes his move
        server.send_message(client, str(c_point))  # server sends msg to user
        print(c_point)


# Called when a client sends a message
@status_check
def message_received(client, server, message):
    # pre pripad chatu
    # data = json.loads(message)
    # print(data)
    print(users)


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
