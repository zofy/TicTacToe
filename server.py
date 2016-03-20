from websocket_server import WebsocketServer
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TicTacToe.settings")
django.setup()
from ttt.models import LoggedUser
from socket_manager import Manager

PORT = 9001
server = WebsocketServer(PORT)
manager = Manager(server)


# def make_available(client):
#     try:
#         currently_unavailable.remove(connections[client['id']])
#         currently_unavailable.remove(connections[connections[client['id']]])
#     except KeyError:
#         print('This error is expected, on of the users in c_u is never in a set.')
#
#
# # deletes logged user from db
# def user_logout(func):
#     def wraper(client, server, *args, **kwargs):
#         # ak bol user v connections, potom poslem spravu ze spojenie zlyhalo
#         if client['id'] in connections:
#             server.send_message(get_client(connections[client['id']]), json.dumps({"connection_drop": client['name']}))
#             make_available(client)
#         if client['status'] == 0:
#
#             if users[client['name']]['count'] == 1:
#                 del users[client['name']]
#                 LoggedUser.objects.get(name=client['name']).delete()  # delete logged user from db
#             else:
#                 users[client['name']]['count'] -= 1
#                 users[client['name']]['ids'].remove(client['id'])
#             server.send_message_to_all('make_request')
#         func(client, server)
#     return wraper
###
#
# def playerVsPlayer(client, server, message):
#     if client['game'] is None:
#         client['game'] = Game()
#     point = client['game'].create_point(message)
#
#     if client['id'] in connections:
#         id = connections[client['id']]  # finds game partner
#         server.send_message(get_client(id), str(point))  # sends msg to game partner
#     else:
#         c_point = client['game'].play(point)  # kernel computes his move
#         server.send_message(client, str(c_point))  # server sends msg to user
#         print(c_point)


# Called for every client connecting (after handshake)
def new_client(client, server):
    server.send_message_to_all('Hey all, new client has joined us!')
    print("New client connected and was given id %d" % client['id'])


# Called for every client disconnecting
# @user_logout
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
# @status_check
@manager.check_message
def message_received(client, server, message):
    print(message)


server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
# clear all LoggedUsers
LoggedUser.objects.all().delete()
# then run server
server.run_forever()
