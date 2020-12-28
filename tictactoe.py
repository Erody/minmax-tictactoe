from math import inf
from node import Node


def minmax(node, depth, player, start_depth):
    if depth == 0 or node.value == inf or node.value == -inf:
        return node.value, node

    best_value = inf * -player
    best_node = node

    for child in node.children:

        val, node = minmax(child,  depth-1, -player, start_depth)
        if (val * player) > (best_value * player):
            if depth == start_depth:
                best_node = node
            best_value = val

    return best_value, best_node


def choose_symbol():
    while True:
        player_symbol = input("Please choose your symbol(X/O): ").upper()
        if player_symbol in ['X', 'O']:
            return player_symbol
        else:
            print('Invalid symbol. Please choose either X or O.')
            continue


def convert_board(board, player_symbol, ai_symbol):
    xoboard = []
    for x in board:
        if x == 0:
            xoboard.append('_')
        elif x == 1:
            xoboard.append(player_symbol)
        else:
            xoboard.append(ai_symbol)
    return xoboard


def print_game(xoboard):
    line1 = " ".join([str(x).rjust(2)
                      for i, x in enumerate(xoboard) if i <= 2]).rjust(15)
    line2 = " ".join([str(x).rjust(2)
                      for i, x in enumerate(xoboard) if i > 2 and i <= 5]).rjust(15)
    line3 = " ".join([str(x).rjust(2)
                      for i, x in enumerate(xoboard) if i > 5]).rjust(15)

    footer = '/'*20 + '\n'
    header = ''.ljust(len(footer)-1, '/') + '\n'

    print(header + line1 + '\n' + line2 + '\n' + line3 + '\n' + footer)


def player_move(board):
    while True:
        move = int(input('Make your move! Enter a number between 0 and 8: '))
        if type(move) is int and move in range(9):
            if board[move] == 0:
                board[move] = 1
                break
            else:
                print("Move impossible. Please choose the index of an empty field!")
                continue
        else:
            print("Move impossible. Make sure to choose a number between 0 and 8!")
            continue
    return board


def ai_move(old_board, new_board):
    i = None
    for index, (first, second) in enumerate(zip(old_board, new_board)):
        if first != second:
            i = index
    new_board[i] = -1
    return new_board


def is_game_over(state):
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [
        0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    if 0 not in state:
        return True, None
    for combo in winning_combinations:
        if board[combo[0]] != 0 and board[combo[1]] != 0 and board[combo[2]] != 0:
            if board[combo[0]] == board[combo[1]] == board[combo[2]]:
                # board[combo[0]] is equal to the player who won.
                return True, board[combo[0]]
    return False, None


if __name__ == "__main__":
    board = [
        0, 0, 0,
        0, 0, 0,
        0, 0, 0
    ]
    depth = 9
    symbols = ['X', 'O']
    player_symbol = choose_symbol()
    ai_symbol = 'X' if player_symbol == 'O' else 'O'
    xoboard = convert_board(board, player_symbol, ai_symbol)
    print_game(xoboard)

    while True:
        player = 1
        board = player_move(board)
        over, winner = is_game_over(board)
        depth = depth-1
        xoboard = convert_board(board, player_symbol, ai_symbol)
        print_game(xoboard)
        if over:
            if winner == None:
                print('The game ended in a draw!')
                break
            elif winner == 1:
                print('Congratulations! You beat the ai.')
                break
            else:
                print('You lost!')
                break

        state = Node(depth, -player, board)
        val, node = minmax(state, depth, -player, depth)
        board = ai_move(board, node.board)
        depth = depth-1
        xoboard = convert_board(board, player_symbol, ai_symbol)
        print_game(xoboard)
        over, winner = is_game_over(board)
        if over:
            if winner == None:
                print('The game ended in a draw!')
                break
            elif winner == 1:
                # This should never occur. If it does, something went wrong.
                print('Congratulations! You beat the ai.')
                break
            else:
                print('You lost!')
                break
