import json
from kernel import Game
from ttt.models import LoggedUser, Player


class Manager(object):
    def __init__(self, server, users={}, connections={}, currently_unavailable=set()):
        self.server = server
        self.users = users
        self.connections = connections
        self.currently_unavailable = currently_unavailable

    def get_client(self, id):
        print(type(self.server.clients))
        for client in self.server.clients:
            if client['id'] == id:
                return client
        print('Sorry client terminated his connection.')

    def send_request(self, client, name):
        for id in self.users[name]['ids']:
            if id not in self.currently_unavailable:
                self.currently_unavailable.add(id)
                self.connections[id] = client['id']
                self.connections[client['id']] = id
                try:
                    c = self.get_client(id)
                except:
                    self.server.send_message(client, json.dumps({"connection_drop": name}))
                else:
                    self.server.send_message(c, json.dumps({"name": client['name']}))
                break
        self.server.send_message(client, json.dumps({"answer": 'unavailable'}))

    def send_answer(self, client, answer):
        challenger = self.get_client(self.connections[client['id']])
        self.server.send_message(challenger, json.dumps({"answer": answer, "player": client['name']}))
        if answer == 'no':
            del self.connections[self.connections[client['id']]]
            del self.connections[client['id']]

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
            pass

    def manage_0(self, client, msg):
        if 'request' in msg:
            self.send_request(client, msg['request'])
            print(self.connections)
        elif 'answer' in msg:
            self.currently_unavailable.remove(client['id'])
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
        pass

    def delete_connections(self, client):
        if client['id'] in self.connections:
            try:
                self.currently_unavailable.remove(self.connections[client['id']])
                self.currently_unavailable.remove(client['id'])
            except KeyError:
                print('This error is expected, on of the users in c_u is never in a set.')

            self.server.send_message(self.get_client(self.connections[client['id']]), json.dumps({"connection_drop": client['name']}))
            del self.connections[self.connections[client['id']]]
            del self.connections[client['id']]

    # checks whether message contains json
    def check_message(self, func):
        def wraper(client, server, message, *args, **kwargs):
            try:
                msg = json.loads(message)
            except:
                return func(client, server, message)
            else:
                self.read_json(client, msg)

        return wraper

    # called when user goes away from page
    def user_logout(self, func):
        def wraper(client, *args, **kwargs):
            # ak bol user v connections, potom poslem spravu ze spojenie zlyhalo
            self.delete_connections(client)
            if client['status'] == 0:
                if self.users[client['name']]['count'] == 1:
                    del self.users[client['name']]
                    LoggedUser.objects.get(name=client['name']).delete()  # delete logged user from db
                else:
                    self.users[client['name']]['count'] -= 1
                    self.users[client['name']]['ids'].remove(client['id'])
                self.server.send_message_to_all('make_request')
            func(client, self.server)
        return wraper

    # creates new LoggedUser
    def manage_logged_user(self, client, name):
        if name not in self.users:
            LoggedUser(name=name).save()  # create logged user
        self.users.setdefault(name, {'count': 0, 'ids': []})
        self.users[name]['count'] += 1
        self.users[name]['ids'].append(client['id'])
        self.server.send_message_to_all('make_request')
        client['status'] = 0
        client['name'] = name
