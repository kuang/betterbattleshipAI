import numpy as np
import random

# dimension of board- can be changed later
BOARD_SIZE = 10

# inits game board
game_board = np.zeros((BOARD_SIZE, BOARD_SIZE))
AIRCRAFT_CARRIER_SIZE = 5  # 5
BATTLESHIP_SIZE = 4  # 4
DESTROYER_SIZE = 3  # 3
SUBMARINE_SIZE = 3  # 2
PATROL_BOAT_SIZE = 2  # 1

# 1 = up, 2 = down, 3 = left, 4 = right
SHIP_DIRECTIONS = [1, 2, 3, 4]

"""
heads up on board stuff: numpy array goes by [ROW, COL]
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
    place_rand_ship(AIRCRAFT_CARRIER_SIZE, 5)
    place_rand_ship(BATTLESHIP_SIZE, 4)
    place_rand_ship(DESTROYER_SIZE, 3)
    place_rand_ship(SUBMARINE_SIZE, 2)
    place_rand_ship(PATROL_BOAT_SIZE, 1)


# place a ship of size ship_size, with marking ship_marking
# idea: pick random x y. check if ship can be placed there. if yes, place, otherwise, pick new x y
def place_rand_ship(ship_size, ship_marking):
    ship_placed_validly = False
    while not ship_placed_validly:
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        # no ship at this coord yet
        if game_board[row][col] == 0:
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
            if game_board[row-i][col] != 0:
                return False
    elif direction == 2:  # down
        if row + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            # print(game_board[row][col])
            if game_board[row+i][col] != 0:
                return False
    elif direction == 3:  # left
        if col - ship_size + 1 < 0:
            return False
        for i in range(ship_size):
            if game_board[row][col-i] != 0:
                return False
    else:  # direction = 4, right
        if col + ship_size > BOARD_SIZE:
            return False
        for i in range(ship_size):
            if game_board[row][col+i] != 0:
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

set_random_ships()
print_board_to_console()
