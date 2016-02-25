from websocket_server import WebsocketServer
from kernel import Game

# Called for every client connecting (after handshake)

def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    # point = client['game'].create_point(message)
    # c_point = client['game'].play(point)
    # server.send_message(client, str(c_point))
    # print("Client(%d) said: %s" % (client['id'], c_point))
    # print("His game is %s" % client['game'])
    # server.send_message(client, '0')
    print('msg recieved')
    server.send_message_to_all("Client %d said: %s" % (client['id'], message))


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
