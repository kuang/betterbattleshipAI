import engine
import random_ai
import naive_ai
import det_ai
import monte_carlo_sim_ai as mcsim
import seaborn as sns
import pandas as pd
import matplotlib.pylab as plt

DEBUG = False


# parameter: higher order function from the AI that is called to get next move.
# return: number of turns it took to win
# ex. model.get_next_move
def start_game(model_func_next_move):
    game_engine.restart_game()
    game_over = False
    num_turns = 0
    move_response = None
    while not game_over:
        next_hit = model_func_next_move(move_response)
        # print(move_response)
        # print(next_hit)
        # print("Game board after the move the AI just calculated is made: ")
        move_response = game_engine.update_gameboard(next_hit[0], next_hit[1])
        # game_engine.print_board_to_console()
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


# runs monte carlo sim ai num_moves time and returns the probability table at that instance
def get_mc_prob_table(num_mc_sims, num_moves):
    mc_sim_ai = mcsim.MonteCarloSimAi(num_mc_sims)
    game_engine.restart_game()
    game_over = False
    num_turns = 0
    move_response = None
    while num_turns < num_moves and not game_over:
        next_hit = mc_sim_ai.next_move(move_response)
        move_response = game_engine.update_gameboard(next_hit[0], next_hit[1])
        num_turns += 1
        game_over = move_response[2]
    return mc_sim_ai.get_probability_table()


def show_heatmap(two_dim_table):
    axis = [str(i) for i in range(engine.BOARD_SIZE)]
    df = pd.DataFrame(two_dim_table, columns=axis)
    sns.heatmap(df)
    plt.show()


game_engine = engine.Engine()
naive_ai = naive_ai.NaiveAI()
deterministic_ai = det_ai.DetAI()
monte_carlo_sim_ai = mcsim.MonteCarloSimAi(1000)
# prob_table = get_mc_prob_table(100, 35)
# print(monte_carlo_sim_ai.get_top_n_from_2d_table(prob_table, 5))

# print("random AI's avg score: " + str(compute_avg_score(1, random_ai.next_move, random_ai.restart))) #avg=92? forgot
# print("naive AI's avg score: " + str(compute_avg_score(100, naive_ai.next_move, naive_ai.restart)))  #avg=78.72
print("Deterministic AI's avg score: " + str(compute_avg_score(10000, deterministic_ai.next_move, deterministic_ai.restart)))  #avg=
# print("Monte Carlo Simulation AI's avg score: " + str(compute_avg_score(100, monte_carlo_sim_ai.next_move, monte_carlo_sim_ai.restart)))
# 50.58 with 100 simulations and num mc sim = 10, mc sim = 50 goes to 48.08