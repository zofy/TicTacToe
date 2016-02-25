class Game(object):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def __init__(self,size=3, game_length=3):
        self.size = size
        self.game_length = game_length
        self.board = ''
        self.me = set()
        self.superior = set()
        self.board_points = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        self.point_move = ()

    def __str__(self):
        return 'Tic Tac Toe: id: %d, size: %d, game length: %d' % (self.id, self.size, self.game_length)

    def print_board(self):
        end = ''
        for i in xrange(self.size, 1, -1):
            end += ' %d  ' % (-i + self.size + 1)
            self.board += '%d ' % i + (self.size - 1) * '___|' + '___\n'
        end += ' %d' % self.size
        self.board = self.board + '1 ' + (self.size - 1) * '   |' + '   \n  ' + end
        return self.board

    def point_number(self, point):
        return (self.size - point[0]) * (self.size * 4 + 2) + (point[1] - 1) * 4 + 3

    def mark_point(self, char, point):
        number = self.point_number(point)
        self.board = self.board[:number] + char + self.board[number + 1:len(self.board)]
        print(self.board)

    def create_point(self, msgFromServer):
        x = msgFromServer[0]
        y = msgFromServer[2]
        return int(x), int(y)

    def check_count(self, direction, point, me):
        count = 0
        a = point[0]
        b = point[1]
        while (a, b) in me:  # in O(N) pre list O(1) pre set
            count += 1
            a += direction[0]
            b += direction[1]
        return count

    def check_win(self, point, me):
        max = 0
        for d in Game.directions:
            count = self.check_count(d, point, me) + self.check_count((-d[0], -d[1]), point, me)
            count -= 1  # 2x point
            if count == self.game_length:
                return True
        return False

    def find_max(self, list):
        idx = -1
        max = -20
        for i in xrange(0, len(list)):
            if list[i] > max:
                max = list[i]
                idx = i
        return idx

    def find_min(self, list):
        idx = -1
        min = 20
        for i in xrange(0, len(list)):
            if list[i] < min:
                min = list[i]
                idx = i
        return idx

    def rec(self, point, player=1, i=0):

        if self.check_win(point, self.superior):
            return -10
        elif self.check_win(point, self.me):
            return 10
        elif i == len(self.board_points):
            return 0
        scores = []
        moves = []

        for step in xrange(i, len(self.board_points)):
            if player == 0:
                point = self.board_points[step]
                self.superior.add(point)
                moves.append(point)
                self.board_points[i], self.board_points[step] = self.board_points[step], self.board_points[i]
                scores.append(self.rec(point, 1, i + 1))
                self.board_points[i], self.board_points[step] = self.board_points[step], self.board_points[i]
                self.superior.remove(point)
            else:
                point = self.board_points[step]
                self.me.add(point)
                moves.append(point)
                self.board_points[i], self.board_points[step] = self.board_points[step], self.board_points[i]
                scores.append(self.rec(point, 0, i + 1))
                self.board_points[i], self.board_points[step] = self.board_points[step], self.board_points[i]
                self.me.remove(point)

        if player == 0:
            min_score_idx = self.find_min(scores)
            self.point_move = moves[min_score_idx]
            return scores[min_score_idx]
        else:
            max_score_idx = self.find_max(scores)
            self.point_move = moves[max_score_idx]
            return scores[max_score_idx]

    def play(self, point):
        self.superior.add(point)
        self.board_points.remove(point)
        if self.check_win(point, self.superior):
            return 'Player won!'
        self.rec(point)
        c_point = self.point_move
        self.me.add(c_point)
        self.board_points.remove(c_point)
        if self.check_win(c_point, self.me):
            print('Computer won!')
        return self.point_move


