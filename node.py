from math import inf
from termcolor import colored

# Tree builder


class Node(object):
    def __init__(self, depth, player, board, value=0):
        self.depth = depth
        self.player = player
        self.value = value
        self.board = board
        self.children = []
        self.moves = []
        self.get_possible_moves()
        self.create_children()

    def __repr__(self):
        board = self.board[:]
        line1 = " ".join([str(x).rjust(2)
                          for i, x in enumerate(board) if i <= 2]).rjust(15)
        line2 = " ".join([str(x).rjust(2)
                          for i, x in enumerate(board) if i > 2 and i <= 5]).rjust(15)
        line3 = " ".join([str(x).rjust(2)
                          for i, x in enumerate(board) if i > 5]).rjust(15)

        colored_value = self.value
        if self.value == inf:
            colored_value = colored(self.value, 'green')
        elif self.value == -inf:
            colored_value = colored(self.value, 'red')
        footer = '{} {} {}'.format('/'*10, colored_value, '/'*10) + '\n'
        header = ''.ljust(len(footer)-1, '/') + '\n'

        return header + line1 + '\n' + line2 + '\n' + line3 + '\n' + footer

    def get_possible_moves(self):
        for i, node in enumerate(self.board):
            if node == 0:
                self.moves.append(i)

    def make_move(self, move, player):
        board = self.board[:]
        board[move] = player
        return board

    def create_children(self):
        if self.depth > 0 and self.value != inf and self.value != -inf:
            for move in self.moves:
                board = self.make_move(move, self.player)
                self.children.append(
                    Node(self.depth-1, -self.player, board, self.evaluate(board)))

    def evaluate(self, board):
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [
            0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for combo in winning_combinations:
            if board[combo[0]] != 0 and board[combo[1]] != 0 and board[combo[2]] != 0:
                if board[combo[0]] == board[combo[1]] == board[combo[2]]:
                    # board[combo[0]] is equal to the player who won. So if computer won this will be inf * -1, if user won it will be inf * 1
                    return inf * board[combo[0]]
        return 0  # if no player won, return 0
