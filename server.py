from websocket_server import WebsocketServer
from kernel import Game

games = {}


# Called for every client connecting (after handshake)

def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    games[client['id']] = Game()
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    point = games[1].create_point(message)
    c_point = games[client['id']].play(point)
    server.send_message(client, str(c_point))
    print(c_point)


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
