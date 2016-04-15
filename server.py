from websocket_server import WebsocketServer
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TicTacToe.settings")
django.setup()
from ttt.models import MenuUser
from socket_manager import Manager

PORT = 9001
server = WebsocketServer(PORT)
manager = Manager(server)


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])


# Called for every client disconnecting
# @manager.user_logout
def client_left(client, server):
    manager.user_logout(client)
    print("Client disconnected")


# Called when a client sends a message
# @status_check
@manager.check_message
def message_received(client, server, message):
    print(message)


server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
# clear all LoggedUsers
MenuUser.objects.all().delete()
# then run server
server.run_forever()
