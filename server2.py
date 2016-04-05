import json
import logging
import signal

import time
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import os
import django
from tornado.options import options

from kernel import Game

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TicTacToe.settings")
django.setup()
from ttt.models import LoggedUser

'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes.
'''

LoggedUser.objects.all().delete()

is_closing = False


def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True


def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []
    users = {}
    connections = {}
    games = {}
    players = {}

    def open(self):
        print 'new connection'
        WSHandler.clients.append(self)

    def on_message(self, message):
        print 'message received:  %s' % message
        self.check_message(message)
        # Reverse Message and send it back
        # print 'sending back message: %s' % message[::-1]
        # self.write_message(message[::-1])

    def on_close(self):
        print 'connection closed'
        self.user_logout()
        WSHandler.clients.remove(self)

    def check_origin(self, origin):
        host = self.request.headers.get('Host')
        print(host)
        print(origin)
        return True

    # checks whether message contains json
    def check_message(self, message):
        try:
            msg = json.loads(message)
            msg['status']
        except:
            print('No json file')
        else:
            self.read_json(msg)

    def read_json(self, msg):
        if msg['status'] == 0:
            self.manage_0(msg)
        elif msg['status'] == 1:
            self.manage_1(msg)
        elif msg['status'] == 2:
            self.manage_2(msg)

    def manage_0(self, msg):
        if 'request' in msg:
            self.send_request(msg['request'])
        elif 'answer' in msg:
            self.send_answer(msg['answer'])
        else:
            self.manage_user(msg['name'])

    def manage_1(self, msg):
        WSHandler.games.setdefault(self, Game())
        if 'refresh' in msg:
            WSHandler.games[self].refresh()
        else:
            self.player_vs_computer(msg['point'])

    def manage_2(self, msg):
        if 'point' in msg:
            self.player_vs_player(msg['point'])
        elif 'color' in msg:
            opponent = WSHandler.connections[self]
            opponent.write_message(json.dumps({"color": msg['color']}))
        elif 'connection' in msg:
            print('Connecting players...')
            p1 = msg['connection'][0]
            p2 = msg['connection'][1]
            if not self.wait_until(10, msg['connection']):
                self.write_message(json.dumps({"connection_drop": 'Opponent'}))
            else:
                WSHandler.connections[WSHandler.players[p1]] = WSHandler.players[p2]
                WSHandler.connections[WSHandler.players[p2]] = WSHandler.players[p1]
                self.write_message(json.dumps({"go": 1}))
        else:
            print('Adding player ' + msg['name'])
            WSHandler.players[msg['name']] = self

    # waiting for players to connect
    def wait_until(self, timeout, players, period=1):
        must_end = time.time() + timeout
        while time.time() < must_end:
            if players[1] in WSHandler.players and players[0] in WSHandler.players:
                print('All players connected.')
                return True
            time.sleep(period)
        print('Players have not been connected.')
        return False

    def player_vs_player(self, point_idx):
        try:
            opponent = WSHandler.connections[self]
        except KeyError:
            print('Connection probably dropped down.')
        else:
            print('sending point')
            opponent.write_message(json.dumps({"point": point_idx}))
            opponent.write_message(json.dumps({"go": 1}))

    def player_vs_computer(self, p_point):
        point = WSHandler.games[self].create_point(p_point)
        c_point = WSHandler.games[self].play(point)  # kernel computes his move
        if c_point[0] is None:
            self.write_message(
                    json.dumps({"end": c_point[1],
                                "point": c_point[2]}))  # server sends msg (his move) to user
        else:
            self.write_message(json.dumps({"point": c_point}))
        print(c_point)

    def send_msg_to_users(self):
        for user in WSHandler.users:
            user.write_message('make_request')

    def find_user(self, name):
        for user in WSHandler.users:
            if WSHandler.users[user] == name:
                return user

    def send_request(self, name):
        requested_user = self.find_user(name)
        if requested_user is None:
            self.write_message(json.dumps({"connection_drop": name}))
            return
        if requested_user in WSHandler.connections:
            self.write_message(json.dumps({"answer": 'unavailable', "player": name}))
        else:
            WSHandler.connections[self] = requested_user
            WSHandler.connections[requested_user] = self
            requested_user.write_message(json.dumps({"name": WSHandler.users[self]}))
        print(self.connections)

    def send_answer(self, answer):
        challenger = WSHandler.connections[self]
        challenger.write_message(json.dumps({"answer": answer, "player": WSHandler.users[self]}))
        if answer == 'Refuse':
            self.delete_connections()

    def delete_connections(self):
        try:
            del WSHandler.connections[WSHandler.connections[self]]
            del WSHandler.connections[self]
        except KeyError:
            pass

    def manage_user(self, name):
        if name not in WSHandler.users:
            LoggedUser.objects.create(name=name).save()  # create logged user
            WSHandler.users[self] = name
            self.send_msg_to_users()
            print(WSHandler.users)
            print(LoggedUser.objects.all())

    def user_logout(self):
        if self in WSHandler.users:
            self.logout0()
        elif self in WSHandler.games:
            del WSHandler.games[self]
            print('Games: ', WSHandler.games)

    def logout0(self):
        try:
            LoggedUser.objects.get(name=WSHandler.users[self]).delete()  # delete logged user from db
        except:
            pass
        del WSHandler.users[self]
        self.send_msg_to_users()
        print(WSHandler.users)
        print(LoggedUser.objects.all())


application = tornado.web.Application([
    (r'/ws', WSHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    http_server.listen(8889)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()
