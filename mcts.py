import monte_carlo_sim_ai
import math


class Node(object):
    def __init__(self, mc_sim, parent):
        # use mc_sim to get the board state
        self.mc_sim = mc_sim
        self.parent = parent
        self.children = []
        self.wins = 0
        self.losses = 0
        self.win_rate = self.wins / self.losses
        # the move that got you to this node
        self.move = (0,0)

    def add_child(self, obj):
        self.children.append(obj)

    def get_win_rate(self):
        if self.losses == 0:
            return self.wins
        return self.wins / self.losses

    def get_total_num_sims_parent(self):
        sum_sims = 0
        for child in self.children:
            sum_sims += child.wins + child.losses
        return sum_sims


class MCTS:
    # the constant c defined in lecture
    def __init__(self, max_time, mc_sim):
        self.c = 1 / math.sqrt(2)
        self.max_time = max_time
        self.max_iters = 1000
        # use this guy to keep track of the board
        self.mc_sim = mc_sim
        self.root = Node(self.mc_sim, None)

    # returns the child that is optimal from the root
    def start_search(self, root):
        i = 0
        while i < self.max_iters:
            leaf = self.select(root)
            # TODO expand the leaf?
            child = self.expand(leaf)
            # simulation_result = rollout(child)
            simulation_result = rollout(leaf)
            backpropagate(leaf, simulation_result)
            i += 1
        return self.best_child(root)

    def select(self, node):
        # while we're not at a leaf
        while len(node.children) > 0:
            node = self.apply_uct(node)
        return node

    # gets the best child using the UCB method applied to trees
    def apply_uct(self, node):
        max_val = -1
        max_node = None
        for child in node.children:
            ucb = self.calc_ucb(child, node.get_total_num_sims_parent())
            if ucb > max_val:
                max_val = ucb
                max_node = child
        return max_node

    def calc_ucb(self, child, total_num_sims_parent):
        num_times_child_tried = child.wins + child.losses
        prob_win = child.wins / num_times_child_tried
        second_term = self.c * (math.sqrt(math.log(total_num_sims_parent) / num_times_child_tried))
        return prob_win + second_term

    def expand(self, leaf):
        valid_moves = leaf.mc_sim.get_all_valid_moves()
        child_sim = monte_carlo_sim_ai.MonteCarloSimAi()

        child = Node(0, leaf)
    #     TODO implement smarter logic for choosing a new move


    def rollout(self, node):
        while non_terminal(node):
            node = rollout_policy(node)
        return result(node)

    # function for randomly selecting a child node
    def rollout_policy(self, node):
        return pick_random(node.children)

    def backpropagate(self, node, result):
        if is_root(node) return
        node.stats = update_stats(node, result)
        backpropagate(node.parent)

    def best_child(self, node):

    # pick child with highest number of visits

    def next_move(self, response):
        self.mc_sim.update_state_with_response(response)
        # TODO
