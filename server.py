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
# @manager.user_logout
def client_left(client, server):
    manager.user_logout(client)
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
