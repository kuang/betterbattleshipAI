import numpy as np
import random

# dimension of board- can be changed later
BOARD_SIZE = 10
DEFAULT_CHAR = ' '
HIT_CHAR = 'X'
MISS_CHAR = 'O'

# inits game board
# AIRCRAFT_CARRIER_SIZE = 5  # A
# BATTLESHIP_SIZE = 4  # B
# DESTROYER_SIZE = 3  # D
# SUBMARINE_SIZE = 3  # S
# PATROL_BOAT_SIZE = 2  # P
SHIP_CHARS = ['A', 'B', 'D', 'S', 'P']
SHIP_SIZES = {'A': 5, 'B': 4, 'D': 3, 'S': 3, 'P': 2}

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


class Engine:
    def __init__(self):
        self.game_board = [[DEFAULT_CHAR for i in range(
            BOARD_SIZE)] for j in range(BOARD_SIZE)]

    def restart_game(self, initial_board=None, ships_remaining=SHIP_CHARS, locs_to_place_ships=None, unplaceable_locs=None):
        if locs_to_place_ships is None:
            locs_to_place_ships = []
        if unplaceable_locs is None:
            unplaceable_locs = []
        if initial_board is not None:
            self.game_board = initial_board
        else:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    self.game_board[i][j] = DEFAULT_CHAR
        self.set_random_ships(
            ships_remaining, locs_to_place_ships, unplaceable_locs)

    # converts ships (excluding shots_fired on ships) to 1 and everything else to 0
    # useful for calculations in monte carlo simulations
    def get_flattened_board(self, shots_fired):
        # create a copy of the game board
        flattened_board = [row[:] for row in self.game_board]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # if it's a ship or a place we already fired at, set to 0
                if flattened_board[i][j] not in SHIP_CHARS or [i, j] in shots_fired:
                    flattened_board[i][j] = 0
                else:
                    flattened_board[i][j] = 1
        return flattened_board

    # prints to console for debugging
    def print_board_to_console(self):
        print(np.matrix(self.game_board))

    # set game board to a random positioning of ships
    # ships ARE allowed to touch
    def set_random_ships(self, ships_remaining, locs_to_place_ships, unplaceable_locs):
        for ship in ships_remaining:
            if ship not in SHIP_CHARS:
                print('Error, ship ' + ship + ' does not exist')
                continue
            locs_to_place_ships = self.place_rand_ship(
                SHIP_SIZES[ship], ship, locs_to_place_ships, unplaceable_locs)

    # place a ship of size ship_size, with marking ship_marking
    # idea: pick random x y. check if ship can be placed there. if yes, place, otherwise, pick new x y
    # returns locs_to_place_ships that are left after placing a ship
    def place_rand_ship(self, ship_size, ship_marking, locs_to_place_ships, unplaceable_locs):
        ship_placed_validly = False
        locs_count = 0
        while not ship_placed_validly:
            row = random.randint(0, BOARD_SIZE-1)
            col = random.randint(0, BOARD_SIZE-1)
            placeable_chars = [DEFAULT_CHAR]
            allow_place_on_hit = False
            # if we still have to place these ships on hits, then allow them to be placed there
            if len(locs_to_place_ships) > 0:
                allow_place_on_hit = True
            # first go through the locs to place ships, then we can go back to random
            if locs_count < len(locs_to_place_ships):
                row = locs_to_place_ships[locs_count][0]
                col = locs_to_place_ships[locs_count][1]
                allow_place_on_hit = True
                placeable_chars = [DEFAULT_CHAR, HIT_CHAR]
            # no ship at this coord yet
            if self.game_board[row][col] in placeable_chars:
                random.shuffle(SHIP_DIRECTIONS)  # choose random direction
                for direction in SHIP_DIRECTIONS:
                    if self.check_valid_ship_placement(ship_size, direction, row, col, allow_place_on_hit, unplaceable_locs):
                        self.place_ship(ship_size, ship_marking,
                                        direction, row, col)
                        ship_placed_validly = True
                        break
            locs_count += 1
        # if a ship was placed at a location that it should be, then remove the loc
        return [loc for loc in locs_to_place_ships if self.game_board[loc[0]][loc[1]] not in SHIP_CHARS]

    # checks if a ship of size ship_size can be placed in direction direction at row col
    # allow_place_on_hit means that a ship can be placed on a hit spot, useful for monte carlo placements

    def check_valid_ship_placement(self, ship_size, direction, row, col, allow_place_on_hit, unplaceable_locs):
        PLACEABLE_CHARS = [DEFAULT_CHAR]
        if allow_place_on_hit:
            PLACEABLE_CHARS.append(HIT_CHAR)
        if direction == 1:  # up
            if row - ship_size + 1 < 0:
                return False
            for i in range(ship_size):
                if self.game_board[row-i][col] not in PLACEABLE_CHARS or [row-i, col] in unplaceable_locs or self.is_loc_adjacent_to_ship(row-i, col):
                    return False
                # if game_board[row][col] == HIT_CHAR:
                #     return False
        elif direction == 2:  # down
            if row + ship_size > BOARD_SIZE:
                return False
            for i in range(ship_size):
                if self.game_board[row+i][col] not in PLACEABLE_CHARS or [row+i, col] in unplaceable_locs or self.is_loc_adjacent_to_ship(row+i, col):
                    return False
        elif direction == 3:  # left
            if col - ship_size + 1 < 0:
                return False
            for i in range(ship_size):
                if self.game_board[row][col-i] not in PLACEABLE_CHARS or [row, col - i] in unplaceable_locs or self.is_loc_adjacent_to_ship(row, col-i):
                    return False
        else:  # direction = 4, right
            if col + ship_size > BOARD_SIZE:
                return False
            for i in range(ship_size):
                if self.game_board[row][col+i] not in PLACEABLE_CHARS or [row, col + i] in unplaceable_locs or self.is_loc_adjacent_to_ship(row, col-i):
                    return False
        return True

    # returns true if loc is next to a ship, false otherwise
    def is_loc_adjacent_to_ship(self, row, col):
        # up
        if row-1 >= 0 and self.game_board[row-1][col] != DEFAULT_CHAR:
            return True
        # down
        if row+1 < BOARD_SIZE and self.game_board[row+1][col] != DEFAULT_CHAR:
            return True
        # left
        if col-1 >= 0 and self.game_board[row][col-1] != DEFAULT_CHAR:
            return True
        # right
        if col+1 < BOARD_SIZE and self.game_board[row][col+1] != DEFAULT_CHAR:
            return True
        return False

    def place_ship(self, ship_size, ship_marking, direction, row, col):
        if direction == 1:  # up
            for i in range(ship_size):
                self.game_board[row-i][col] = ship_marking
        elif direction == 2:  # down
            for i in range(ship_size):
                self.game_board[row+i][col] = ship_marking
        elif direction == 3:  # left
            for i in range(ship_size):
                self.game_board[row][col-i] = ship_marking
        else:  # direction = 4, right
            for i in range(ship_size):
                self.game_board[row][col+i] = ship_marking

    def has_game_ended(self):
        for row in self.game_board:
            for item in row:
                # at the end of the game, no more ships will be left on the board
                if item in SHIP_CHARS:
                    return False
        return True

    # ship_hit should be the character of the type of ship
    def is_ship_sunk(self, ship_hit):
        for row in self.game_board:
            for item in row:
                if item == ship_hit:
                    return False
        return True

    # update game for attack on row, col
    # returns tuple (hit/miss, null/which ship sunk, game still on/game over)
    def update_gameboard(self, row, col):
        current = self.game_board[row][col]
        # nothing there and it's not somewhere they already hit, so miss
        if current not in SHIP_CHARS and current != HIT_CHAR:
            self.game_board[row][col] = MISS_CHAR
            return 0, 0, 0
        else:  # hit
            self.game_board[row][col] = HIT_CHAR
            ship_sunk = self.is_ship_sunk(current)
            if ship_sunk:
                game_ended = int(self.has_game_ended())
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
