import engine
import random_ai
import naive_ai


# parameter: higher order function from the AI that is called to get next move.
# return: number of turns it took to win
# ex. model.get_next_move
def start_game(model_func_next_move):
    engine.restart_game()
    game_over = False
    num_turns = 0
    move_response = None
    while not game_over:
        next_hit = model_func_next_move(move_response)
        # print(move_response)
        # print(next_hit)
        move_response = engine.update_gameboard(next_hit[0], next_hit[1])
        # engine.print_board_to_console()
        num_turns += 1
        game_over = move_response[2]
    print('NUMBER OF MOVES: ' + str(num_turns))
    return num_turns


def compute_avg_score(num_simulations, ai_next_move, ai_restart):
    total_score = 0
    for _ in range(num_simulations):
        total_score += start_game(ai_next_move)
        ai_restart()
    return total_score/num_simulations


naive_ai = naive_ai.NaiveAI()
# start_game(naive_ai.next_move)
# Every AI should have a "next_move" function that takes in move_response as well as a "restart" that resets all the relevant variables
print("random AI's avg score: " + str(compute_avg_score(100, random_ai.next_move, random_ai.restart)))
# print("naive AI's avg score: " + str(compute_avg_score(2, naive_ai.next_move, naive_ai.restart)))
