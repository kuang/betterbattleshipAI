import random
from engine import BOARD_SIZE, get_game_board, SHIP_CHARS


class monte_carlo_sim_ai:
    def __init__(self):
        self.BOARD_SIZE = BOARD_SIZE
        self.NUM_MC_SIMULATIONS = 10
        self.current_board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.remaining_ships = SHIP_CHARS[:]  # copy values, not by reference
        self.locs_hit_not_sunk = []  # have to make sure ships are placed where we hit but haven't sunk

    def next_move(self, response):
        # first move
        if response is None:
            pass

    def restart(self):
        pass
