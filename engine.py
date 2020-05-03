import numpy as np
import random

# dimension of board- can be changed later
BOARD_SIZE = 10
DEFAULT_CHAR = ' '
HIT_CHAR = 'X'

# inits game board
game_board = [[DEFAULT_CHAR for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
AIRCRAFT_CARRIER_SIZE = 5  # A
BATTLESHIP_SIZE = 4  # B
DESTROYER_SIZE = 3  # D
SUBMARINE_SIZE = 3  # S
PATROL_BOAT_SIZE = 2  # P

# 1 = up, 2 = down, 3 = left, 4 = right
SHIP_DIRECTIONS = [1, 2, 3, 4]

"""
heads up on board stuff: array goes by [ROW, COL]
if game_board[0,5] = 1:
result is
[[ 0.  0.  0.  0.  0.  1.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]]
"""


# prints to console for debugging
def print_board_to_console():
    print(np.matrix(game_board))


# set game board to a random positioning of ships
# ships ARE allowed to touch
def set_random_ships():
    place_rand_ship(AIRCRAFT_CARRIER_SIZE, 'A')
    place_rand_ship(BATTLESHIP_SIZE, 'B')
    place_rand_ship(DESTROYER_SIZE, 'D')
    place_rand_ship(SUBMARINE_SIZE, 'S')
    place_rand_ship(PATROL_BOAT_SIZE, 'P')


# place a ship of size ship_size, with marking ship_marking
# idea: pick random x y. check if ship can be placed there. if yes, place, otherwise, pick new x y
def place_rand_ship(ship_size, ship_marking):
    ship_placed_validly = False
    while not ship_placed_validly:
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        # no ship at this coord yet
        if game_board[row][col] == DEFAULT_CHAR:
            random.shuffle(SHIP_DIRECTIONS)  # choose random direction
            for direction in SHIP_DIRECTIONS:
                if check_valid_ship_placement(ship_size, direction, row, col):
                    place_ship(ship_size, ship_marking, direction, row, col)
                    ship_placed_validly = True
                    break


# checks if a ship of size ship_size can be placed in direction direction at row col
def check_valid_ship_placement(ship_size, direction, row, col):
    if direction == 1:  # up
        if row - ship_size + 1 < 0:
            return False
        for i in range(ship_size):
            if game_board[row-i][col] != DEFAULT_CHAR:
                return False
    elif direction == 2:  # down
        if row + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if game_board[row+i][col] != DEFAULT_CHAR:
                return False
    elif direction == 3:  # left
        if col - ship_size + 1 < 0:
            return False
        for i in range(ship_size):
            if game_board[row][col-i] != DEFAULT_CHAR:
                return False
    else:  # direction = 4, right
        if col + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if game_board[row][col+i] != DEFAULT_CHAR:
                return False
    return True


def place_ship(ship_size, ship_marking, direction, row, col):
    if direction == 1:  # up
        for i in range(ship_size):
            game_board[row-i][col] = ship_marking
    elif direction == 2:  # down
        for i in range(ship_size):
            game_board[row+i][col] = ship_marking
    elif direction == 3:  # left
        for i in range(ship_size):
            game_board[row][col-i] = ship_marking
    else:  # direction = 4, right
        for i in range(ship_size):
            game_board[row][col+i] = ship_marking


def has_game_ended():
    for row in game_board:
        for item in row:
            if item != DEFAULT_CHAR and item != HIT_CHAR: return False
    return True


# ship_hit should be the character of the type of ship
def is_ship_sunk(ship_hit):
    for row in game_board:
        for item in row:
            if item == ship_hit:
                return False
    return True


# update game for attack on row, col
# returns tuple (hit/miss, null/which ship sunk, game still on/game over)
def update_gameboard(row, col):
    current = game_board[row][col]
    if current == DEFAULT_CHAR or current == HIT_CHAR:  # nothing there or they already hit it, miss
        game_board[row][col] = HIT_CHAR
        return 0, 0, 0
    else:  # hit
        game_board[row][col] = HIT_CHAR
        ship_sunk = is_ship_sunk(current)
        if ship_sunk:
            game_ended = int(has_game_ended())
            return 1, current, game_ended
        return 1, 0, 0


# set_random_ships()
# game_board[0][0] = 'P'
# game_board[0][1] = 'P'
# print_board_to_console()

# print(update_gameboard(0,1))
# print_board_to_console()
# print(update_gameboard(0,0))
# print_board_to_console()

# print(has_game_ended())
