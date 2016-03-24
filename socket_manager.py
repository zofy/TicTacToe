import json
from kernel import Game
from ttt.models import LoggedUser, Player


class Manager(object):
    def __init__(self, server, users={}, connections={}, currently_unavailable=set()):
        self.server = server
        self.users = users
        self.connections = connections

    def get_client(self, id):
        for client in self.server.clients:
            if client['id'] == id:
                return client
        print('Sorry client terminated his connection.')

    def send_request(self, client, name):
        requested_id = self.users[name]
        if requested_id in self.connections:
            self.server.send_message(client, json.dumps({"answer": 'unavailable', "player": name}))
        else:
            self.connections[client['id']] = requested_id
            self.connections[requested_id] = client['id']

            c = self.get_client(requested_id)
            if c is None:
                self.server.send_message(client, json.dumps({"connection_drop": name}))
            else:
                self.server.send_message(c, json.dumps({"name": client['name']}))
        print(self.connections)

    def send_answer(self, client, answer):
        challenger = self.get_client(self.connections[client['id']])
        self.server.send_message(challenger, json.dumps({"answer": answer, "player": client['name']}))
        if answer == 'Refuse':
            self.delete_connections(client)

    def player_vs_player(self, client, point):
        opponent = self.get_client(self.connections[client[id]])
        self.server.send_message(opponent, json.dumps({'point': point}))

    def player_vs_computer(self, client, p_point):
        point = client['game'].create_point(p_point)
        c_point = client['game'].play(point)  # kernel computes his move
        if c_point[0] is None:
            self.server.send_message(client,
                                     json.dumps({"end": c_point[1],
                                                 "point": c_point[2]}))  # server sends msg (his move) to user
            if c_point[1] == 'Player':
                p = Player.objects.get(name=client['name'])  # if player wins, then his score changes
                p.vs_comp += 1
                p.save()
        else:
            self.server.send_message(client, json.dumps({"point": c_point}))
        print(c_point)

    def read_json(self, client, msg):
        if msg['status'] == 0:
            self.manage_0(client, msg)
        elif msg['status'] == 1:
            self.manage_1(client, msg)
        elif msg['status'] == 2:
            self.manage_2(client, msg)

    def manage_0(self, client, msg):
        if 'request' in msg:
            self.send_request(client, msg['request'])
        elif 'answer' in msg:
            self.send_answer(client, msg['answer'])
        else:
            self.manage_logged_user(client, msg['name'])

    def manage_1(self, client, msg):
        client.setdefault('game', Game())
        if 'refresh' in msg:
            client['game'].refresh()
        else:
            self.player_vs_computer(client, msg['point'])

    def manage_2(self, client, msg):
        if 'point' in msg:
            self.player_vs_player(client, msg['point'])
        else:
            client['status'] = 2
            client['name'] = msg['name']
            self.players[msg['name']] = client['id']
            if 'connection' in msg:
                p1 = msg['connection'][0]
                p2 = msg['connection'][1]
                self.connections[self.players[p1]] = self.players[p2]
                self.connections[self.players[p2]] = self.players[p1]
                self.server.send_message(client, json.dumps({"start": 1}))

    def delete_connections(self, client):
        del self.connections[self.connections[client['id']]]
        del self.connections[client['id']]

    def logout_0(self, client):
        if client['id'] in self.connections:
            c = self.get_client(self.connections[client['id']])
            self.server.send_message(c, json.dumps({"connection_drop": client['name']}))
            self.delete_connections(client)
        del self.users[client['name']]
        LoggedUser.objects.get(name=client['name']).delete()  # delete logged user from db
        self.server.send_message_to_all('make_request')

    # checks whether message contains json
    def check_message(self, func):
        def wraper(client, server, message, *args, **kwargs):
            try:
                msg = json.loads(message)
                print(msg)
            except:
                return func(client, server, message)
            else:
                self.read_json(client, msg)

        return wraper

    # called when user goes away from page
    def user_logout(self, func):
        def wraper(client, *args, **kwargs):
            if client['status'] == 0:
                self.logout_0(client)
            func(client, self.server)

        return wraper

    # creates new LoggedUser
    def manage_logged_user(self, client, name):
        if name not in self.users:
            LoggedUser(name=name).save()  # create logged user
        self.users.setdefault(name, client['id'])
        self.server.send_message_to_all('make_request')
        client['status'] = 0
        client['name'] = name
