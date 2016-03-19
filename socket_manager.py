import json

from ttt.models import LoggedUser


class Manager(object):

    def __init__(self, server, users={}, connections={}, currently_unavailable=set()):
        self.server = server
        self.users = users
        self.connections = connections
        self.currently_unavailable = currently_unavailable

    # reads json file and decides what to do according status
    def read_json(self, client, msg):
        print(msg)
        if msg['status'] == 0:
            # if 'request' in msg:
            #     make_connection(client, server, msg['request'])
            #     print(connections)
            #     send_request(client, server)
            # elif 'answer' in msg:
            #     currently_unavailable.remove(client['id'])
            #     send_answer(client, server, msg['answer'])
            # else:
            self.manage_logged_user(client, msg['name'])
            # elif msg['status'] == 1:
            #     if 'refresh' in msg:
            #         client.setdefault('game', Game())
            #         client['game'].refresh()
            #     else:
            #         p_point = msg['point']
            #         player_vs_computer

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

    def connect_users(self, id1, id2):
        self.connections[id1] = id2
        self.connections[id2] = id1

    def player_vs_player(self, client, point):
        opponent = self.get_client(self.connections[client[id]])
        self.server.send_message(opponent, json.dumps({'point': point}))
