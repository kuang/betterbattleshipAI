import engine
import random_ai
# parameter: higher order function from the AI that is called to get next move
# ex. model.get_next_move


def start_game(model_func_next_move):
    engine.set_random_ships()
    game_over = False
    num_turns = 0
    move_response = None
    while not game_over:
        next_hit = model_func_next_move(move_response)
        move_response = engine.update_gameboard(next_hit[0], next_hit[1])
        # engine.print_board_to_console()
        num_turns += 1
        game_over = move_response[2]
        # print(move_response)
    print('NUMBER OF MOVES: ' + str(num_turns))

start_game(random_ai.next_move)