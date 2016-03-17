import json
from websocket_server import WebsocketServer
from kernel import Game
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TicTacToe.settings")
django.setup()
from ttt.models import LoggedUser, Player

connections = {}
users = {}
currently_unavailable = set()


def make_available(client):
    try:
        currently_unavailable.remove(connections[client['id']])
        currently_unavailable.remove(connections[connections[client['id']]])
    except KeyError:
        print('This error is expected, on of the users in c_u is never in a set.')


# deletes logged user from db
def user_logout(func):
    def wraper(client, server, *args, **kwargs):
        # ak bol user v connections, potom poslem spravu ze spojenie zlyhalo
        if client['id'] in connections:
            server.send_message(get_client(connections[client['id']]), json.dumps({"connection_drop": client['name']}))
            make_available(client)
        if client['status'] == 0:

            if users[client['name']]['count'] == 1:
                del users[client['name']]
                LoggedUser.objects.get(name=client['name']).delete()  # delete logged user from db
            else:
                users[client['name']]['count'] -= 1
                users[client['name']]['ids'].remove(client['id'])
            server.send_message_to_all('make_request')
        func(client, server)
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


# creates new LoggedUser
def manage_logged_user(client, name):
    if name not in users:
        LoggedUser(name=name).save()  # create logged user
    users.setdefault(name, {'count': 0, 'ids': []})
    users[name]['count'] += 1
    users[name]['ids'].append(client['id'])
    server.send_message_to_all('make_request')
    client['status'] = 0
    client['name'] = name


def send_request(client, server):
    if client['id'] in connections:
        # sends challenge message
        server.send_message(get_client(connections[client['id']]), json.dumps({"name": client['name']}))
    else:
        # sends currently unavailable message
        server.send_message(client, json.dumps({"answer": 'unavailable'}))


def send_answer(client, server, answer):
    server.send_message(get_client(connections[client['id']]), json.dumps({"answer": answer, "player": client['name']}))
    if answer == 'no':
        del connections[connections[client['id']]]
        del connections[client['id']]


def make_connection(client, server, name):
    for id in users[name]['ids']:
        if id not in currently_unavailable:
            currently_unavailable.add(id)
            connections[id] = client['id']
            connections[client['id']] = id


# reads json file and decides what to do according status
def read_json(client, msg):
    if msg['status'] == 0:
        print(msg)
        if 'request' in msg:
            make_connection(client, server, msg['request'])
            print(connections)
            send_request(client, server)
        elif 'answer' in msg:
            currently_unavailable.remove(client['id'])
            send_answer(client, server, msg['answer'])
        else:
            manage_logged_user(client, msg['name'])
    elif msg['status'] == 1:
        if 'refresh' in msg:
            client.setdefault('game', Game())
            client['game'].refresh()
        else:
            p_point = msg['point']
            player_vs_computer(client, server, p_point)


def connect_clients(id1, id2):
    connections[id1] = id2
    connections[id2] = id1


def get_client(id):
    for c in server.clients:
        if c['id'] == id:
            return c
    print('Sorry client terminated his connection.')


def player_vs_computer(client, server, p_point):
    if client['game'] is None:
        client['game'] = Game()
    point = client['game'].create_point(p_point)
    c_point = client['game'].play(point)  # kernel computes his move
    if c_point[0] is None:
        server.send_message(client,
                            json.dumps({"end": c_point[1], "point": c_point[2]}))  # server sends msg (his move) to user
        if c_point[1] == 'Player':
            p = Player.objects.get(name=client['name'])
            p.vs_comp += 1
            p.save()
    else:
        server.send_message(client, json.dumps({"point": c_point}))
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


# Called for every client connecting (after handshake)
def new_client(client, server):
    server.send_message_to_all('Hey all, new client has joined us!')
    print("New client connected and was given id %d" % client['id'])


# Called for every client disconnecting
@user_logout
def client_left(client, server):
    if client['id'] in connections:
        del connections[connections[client['id']]]
        del connections[client['id']]
    print("Client(%d) disconnected" % client['id'])
    print(connections)


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
# clear all LoggedUsers
LoggedUser.objects.all().delete()
# then run server
server.run_forever()
