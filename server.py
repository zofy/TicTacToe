from websocket_server import WebsocketServer
from kernel import Game

connections = {}


# Called for every client connecting (after handshake)

def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")
    server.send_message(client, str([client['id'] for client in server.clients]))


# Called for every client disconnecting
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


def playerVsPlayer(client, server, message):
    if client['game'] is None:
        client['game'] = Game()
    point = client['game'].create_point(message)

    if client['id'] in connections:
        id = connections[client['id']] # finds game partner
        server.send_message(get_client(id), str(point)) # sends msg to game partner
    else:
        c_point = client['game'].play(point) # kernel computes his move
        server.send_message(client, str(c_point)) # server sends msg to user
        print(c_point)


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'

    if client['status'] == 1:
        playerVsPlayer(client, server, message)
    elif client['status'] == 0:
        pass
        # playerVsComputer(client, server, message)
    elif client['status'] == -1:
        server.send_message(client, str([client['id'] for client in server.clients]))

PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
