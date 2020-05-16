import random
import engine
import numpy as np


class monte_carlo_sim_ai:
    def __init__(self):
        self.BOARD_SIZE = engine.BOARD_SIZE
        self.NUM_MC_SIMULATIONS = 10
        self.current_board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.ships_remaining = engine.SHIP_CHARS[:]  # copy values, not by reference
        self.locs_hit_not_sunk = []  # have to make sure ships are placed where we hit but haven't sunk
        self.locs_sunk = []  # locs where we sunk and hence where new ships shouldn't be
        self.shots_fired = []  # list of locs that we fired at, regardless of their outcome

        self.most_recent_move = None

    def next_move(self, response):
        if response is not None:
            is_hit = response[0]
            ship_sunk = response[1]

        # do the Monte Carlo Simulation to get the frequencies
        frequencies = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        for i in range(self.NUM_MC_SIMULATIONS):
            current_board_copy = [row[:] for row in self.current_board]
            engine.restart_game(current_board_copy, self.ships_remaining, self.locs_hit_not_sunk, self.locs_sunk)
            frequencies = np.add(frequencies, engine.get_flattened_board(self.shots_fired))
        max_coords = np.where(frequencies == np.amax(frequencies))  # get the coords of the highest values in the matrix
        self.most_recent_move = max_coords[0]  # if there are ties, just get the first one
        return self.most_recent_move

    def restart(self):
        pass
