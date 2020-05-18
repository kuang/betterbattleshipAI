import engine
import random_ai
import naive_ai
import monte_carlo_sim_ai as mcsim

monte_carlo_sim_ai = mcsim.MonteCarloSimAi()


def test_locs_to_place():
    game_engine.restart_game(None, engine.SHIP_CHARS, [[0, 0], [9, 9]], [])


def test_unplaceable():
    game_engine.restart_game(None, engine.SHIP_CHARS, [], [0, 0])


def test_place_on_hit():
    current_board = [[' ' for _ in range(engine.BOARD_SIZE)] for _ in range(engine.BOARD_SIZE)]
    current_board[0][0] = engine.HIT_CHAR
    current_board[4][1] = engine.HIT_CHAR
    # game_engine.restart_game(current_board, engine.SHIP_CHARS, [[4, 1]], [])
    game_engine.restart_game(current_board, engine.SHIP_CHARS, [[0, 0], [4, 1]], [[1, 0]])


def test_infinite_loop_bug():
    current_board = [[' ' for _ in range(engine.BOARD_SIZE)] for _ in range(engine.BOARD_SIZE)]
    current_board[1][8] = 'O'
    current_board[3][5] = 'O'
    current_board[4][1] = 'O'
    current_board[6][0] = 'O'
    current_board[6][7] = 'O'
    current_board[7][3] = 'O'
    current_board[9][3] = 'O'
    locs_hit_not_sunk = []
    locs_sunk = []
    game_engine.restart_game(current_board, engine.SHIP_CHARS, locs_hit_not_sunk, locs_sunk)


def test_get_locs_of_sunk():
    # only ship remaining is P
    current_board = [['O', 'X', 'X', 'X', 'O', 'O', ' ', ' ', ' ', ' '],
                     ['O', ' ', 'O', 'O', ' ', 'O', ' ', ' ', ' ', 'O'],
                     ['X', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' '],
                     ['X', ' ', 'O', ' ', 'O', ' ', ' ', ' ', ' ', ' '],
                     ['X', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O'],
                     ['X', 'O', 'X', 'X', 'X', 'O', ' ', 'O', ' ', ' '],
                     ['X', ' ', ' ', ' ', 'O', 'O', ' ', ' ', ' ', ' '],
                     ['O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', 'O', 'X', 'X', 'X', 'X', 'O', ' ', ' ', ' ']]
    monte_carlo_sim_ai.set_board(current_board)
    # locs_sunk = [[0, 1], [2, 0], [3, 0], [4, 0], [5, 0], [5, 2], [6, 0], [9, 2], [9, 3]]
    # locs_hit_not_sunk = [[0, 3], [0, 2], [5, 3], [5, 4], [9, 4], [9, 5]]
    # shots_fired = [[1, 9], [5, 7], [3, 2], [4, 6], [0, 3], [2, 3], [0, 5], [0, 2], [0, 1], [0, 4], [1, 2], [4, 0],  [7, 0], [2, 0], [1, 0], [4, 1], [3, 0], [5, 0], [6, 0], [1, 3], [3, 4], [2, 7], [6, 4], [7, 6], [5, 3], [7, 3], [5, 4], [5, 5], [5, 1], [4, 3], [5, 2], [1, 5], [9, 1], [4, 9], [9, 4], [9, 5], [9, 6], [9, 2], [6, 5], [9, 3]]
    # get the locs of the Destroyer up top
    print("Locs of destroyer, should be (0,1), (0,2), (0,3): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([0, 1], 'D'))
    print("Locs of destroyer, should be (0,1), (0,2), (0,3): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([0, 2], 'D'))
    print("Locs of destroyer, should be (0,1), (0,2), (0,3): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([0, 3], 'D'))
    print("Locs of destroyer as a sub, should be (0,1), (0,2), (0,3): ",
          monte_carlo_sim_ai.get_locs_of_sunk_ship([0, 3], 'S'))

    print("Locs of attacker, should be (2,0) - (6,0): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([2, 0], 'A'))
    print("Locs of attacker, should be (2,0) - (6,0): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([3, 0], 'A'))
    print("Locs of attacker, should be (2,0) - (6,0): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([4, 0], 'A'))
    print("Locs of attacker, should be (2,0) - (6,0): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([5, 0], 'A'))
    print("Locs of attacker, should be (2,0) - (6,0): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([6, 0], 'A'))

    print("Locs of battleship, should be (9,2) - (9,5): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([9, 2], 'B'))
    print("Locs of battleship, should be (9,2) - (9,5): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([9, 3], 'B'))
    print("Locs of battleship, should be (9,2) - (9,5): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([9, 4], 'B'))
    print("Locs of battleship, should be (9,2) - (9,5): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([9, 5], 'B'))

    print("Locs of sub, should be (5,2) - (5,4): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([5, 2], 'S'))
    print("Locs of sub, should be (5,2) - (5,4): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([5, 3], 'S'))
    print("Locs of sub, should be (5,2) - (5,4): ", monte_carlo_sim_ai.get_locs_of_sunk_ship([5, 4], 'S'))


game_engine = engine.Engine()
for i in range(1):
    test_get_locs_of_sunk()
    # game_engine.print_board_to_console()
    print('\n')
