import json

from websocket_server import WebsocketServer
from kernel import Game
from ttt.models import LoggedUser

connections = {}
users = {"names": ["Martin", "Ashton"]}


# deletes logged user from db
def user_logout(func):
    def wraper(client, server, *args, **kwargs):
        if client['status'] == 0:
            users['names'].remove(client['name'])
            LoggedUser.objects.get(name=client['name']).delete()  # delete logged user from db
            server.send_message_to_all('make_request')

    return wraper


# checks whether message contains status
def status_check(func):
    def wraper(client, server, message, *args, **kwargs):
        try:
            msg = json.loads(message)
        except:
            return func(client, server, message)
        else:
            read_json(client, msg)

    return wraper


# reads json file and decides what to do according status
def read_json(client, msg):
    if msg['status'] == 0:
        LoggedUser(name=msg['name']).save()  # create logged user
        server.send_message_to_all('make_request')
        users['names'].append(msg['name'])
        client['status'] = msg['status']
        client['name'] = msg['name']
    elif msg['status'] == 1:
        if 'refresh' in msg:
            client['game'] = None
        else:
            p_point = msg['point']
            playerVsComputer(client, server, p_point)


# Called for every client connecting (after handshake)
def new_client(client, server):
    server.send_message_to_all('Hey all, new client has joined us!')
    print("New client connected and was given id %d" % client['id'])


# Called for every client disconnecting
@user_logout
def client_left(client, server):
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
    point = client['game'].create_point(p_point)
    c_point = client['game'].play(point)  # kernel computes his move
    if c_point is not None:
        server.send_message(client, str(c_point))  # server sends msg to user
    else:
        # check who wins
        # create object Score
        # send result message to client
        pass
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
    print(users)
    print(message)


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
