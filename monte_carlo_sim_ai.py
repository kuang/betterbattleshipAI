import random
import engine
import numpy as np
import itertools
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class MonteCarloSimAi:
    def __init__(self):
        self.BOARD_SIZE = engine.BOARD_SIZE
        self.NUM_MC_SIMULATIONS = 50

        self.current_board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.ships_remaining = engine.SHIP_CHARS[:]  # copy values, not by reference

        self.locs_hit_not_sunk = []  # have to make sure ships are placed where we hit but haven't sunk
        self.locs_sunk = []  # locs where we sunk and hence where new ships shouldn't be
        self.shots_fired = []  # list of locs that we fired at, regardless of their outcome

        self.game_engine = engine.Engine()
        self.DEBUG = False

    def log(self, *args):
        if self.DEBUG:
            for arg in args:
                print(arg)

    # used for testing
    def set_board(self, board):
        self.current_board = board

    def get_locs_of_sunk_ship(self, loc_that_sunk, ship_type):
        ship_size = engine.SHIP_SIZES[ship_type]
        row = loc_that_sunk[0]
        col = loc_that_sunk[1]
        # all the coordinates of the ship that we just sunk
        locs_of_sunk_ship = []
        for direction in range(1, 5):
            if direction == 1:  # up
                for i in range(ship_size):
                    # check if we're out of bounds
                    if row - i < 0:
                        break
                    # if we're at a hit char and we didn't already add this loc, then this is a loc of the sunken ship
                    if self.current_board[row - i][col] == engine.HIT_CHAR:
                        if [row - i, col] not in locs_of_sunk_ship:
                            locs_of_sunk_ship.append([row - i, col])
                    # otherwise if there's a gap then it can't be the same ship, so break
                    else:
                        break
            elif direction == 2:  # down
                for i in range(ship_size):
                    if row + i >= self.BOARD_SIZE:
                        break
                    if self.current_board[row + i][col] == engine.HIT_CHAR:
                        if [row + i, col] not in locs_of_sunk_ship:
                            locs_of_sunk_ship.append([row + i, col])
                    else:
                        break
            elif direction == 3:  # left
                for i in range(ship_size):
                    if col - i < 0:
                        break
                    if self.current_board[row][col - i] == engine.HIT_CHAR:
                        if [row, col - i] not in locs_of_sunk_ship:
                            locs_of_sunk_ship.append([row, col - i])
                    else:
                        break
            else:  # direction = 4, right
                for i in range(ship_size):
                    if col + i >= self.BOARD_SIZE:
                        break
                    if self.current_board[row][col + i] == engine.HIT_CHAR:
                        if [row, col + i] not in locs_of_sunk_ship:
                            locs_of_sunk_ship.append([row, col + i])
                    else:
                        break
        return locs_of_sunk_ship

    def update_state_with_response(self, response):
        if response is not None:
            is_hit = response[0]
            ship_sunk = response[1]
            most_recent_fire = self.shots_fired[-1]
            if is_hit:
                self.log("Hit, updating board, most recent fire is", most_recent_fire)
                self.current_board[most_recent_fire[0]][most_recent_fire[1]] = engine.HIT_CHAR
                if ship_sunk:
                    self.ships_remaining.remove(ship_sunk)
                    # get the coordinates of the sunken ship, add to locs_sunk
                    self.log("just sunk ship " + ship_sunk + " with fire " + str(most_recent_fire))
                    locs_of_sunk_ship = self.get_locs_of_sunk_ship(most_recent_fire, ship_sunk)
                    self.log("locs of just sunk ship:", locs_of_sunk_ship)
                    self.locs_sunk.extend(locs_of_sunk_ship)
                    self.locs_sunk.sort()
                    self.locs_sunk = list(self.locs_sunk for self.locs_sunk, _ in itertools.groupby(self.locs_sunk))
                    self.log("locs after de-duping", self.locs_sunk)
                    # remove the coords in hit not sunk that are in the sunk list now that we've actually sunk
                    new_locs_hit_not_sunk = []
                    for hit_loc in self.locs_hit_not_sunk:
                        should_add_loc = True
                        for sunk_loc in self.locs_sunk:
                            if sunk_loc[0] == hit_loc[0] and sunk_loc[1] == hit_loc[1]:
                                should_add_loc = False
                                break
                        if should_add_loc:
                            new_locs_hit_not_sunk.append(hit_loc)
                    self.locs_hit_not_sunk = new_locs_hit_not_sunk
                    self.log("new locs hit not sunk:", self.locs_hit_not_sunk)
                else:
                    self.locs_hit_not_sunk.append(most_recent_fire)
            else:
                self.current_board[most_recent_fire[0]][most_recent_fire[1]] = engine.MISS_CHAR

    def next_move(self, response):
        self.update_state_with_response(response)
        self.log("response after firing at that loc: ", response)
        # self.log(np.matrix(self.current_board))
        # do the Monte Carlo Simulation to get the frequencies
        frequencies = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        i = 0
        while i < self.NUM_MC_SIMULATIONS:
            current_board_copy = [row[:] for row in self.current_board]
            # self.log("in mc simulation number ", i)
            # self.log("about to restart game in for loop")
            # self.log("Ships remaining: ", self.ships_remaining)
            # self.log("Locs hit not sunk: ", self.locs_hit_not_sunk)
            # self.log("Locs sunk: ", self.locs_sunk)
            # for row in range(engine.BOARD_SIZE):
            #     for col in range(engine.BOARD_SIZE):
            #         if current_board_copy[row][col] != engine.DEFAULT_CHAR:
            #             self.log("current_board[" + str(row) + "][" + str(col) + "] = '" + current_board_copy[row][col] + "'")

            # it's ok for us to access the engine since this new game isn't the real one we're playing from game.py
            # if we couldn't find a valid ship placement, shuffle and try again
            if self.game_engine.restart_game(current_board_copy, self.ships_remaining, self.locs_hit_not_sunk, self.locs_sunk) == -1:
                continue
            self.log("about to add the frequencies")
            frequencies = np.add(frequencies, self.game_engine.get_flattened_board(self.shots_fired))
            i += 1
        self.log("finished for loop")
        # self.log(frequencies)
        max_coords = np.where(frequencies == np.amax(frequencies))  # get the coords of the highest values in the matrix
        max_x = max_coords[0][0]  # max_coords[0] is the list of all the x coordinates in the max pairs, max_coords[1] is same but for y
        max_y = max_coords[1][0]
        self.log("Firing at ", [max_x, max_y])
        if max_x == 0 and max_y == 0:
            self.log("0 and 0 prob")
            self.log(frequencies)
            self.log("ships remaining: ", self.ships_remaining)
            self.log("locs hit not sunk", self.locs_hit_not_sunk)
            self.log("locs sunk ", self.locs_sunk)
            self.log("shots fired", self.shots_fired)
        self.shots_fired.append([max_x, max_y])  # if there are ties, just get the first one
        return self.shots_fired[-1]

    def restart(self):
        self.current_board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.ships_remaining = engine.SHIP_CHARS[:]  # copy values, not by reference

        self.locs_hit_not_sunk = []  # have to make sure ships are placed where we hit but haven't sunk
        self.locs_sunk = []  # locs where we sunk and hence where new ships shouldn't be
        self.shots_fired = []  # list of locs that we fired at, regardless of their outcome

        self.game_engine = engine.Engine()

