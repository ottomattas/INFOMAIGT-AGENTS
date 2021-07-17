# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import game as g
from random_agent import RandomAgent

import random
import copy
import time
from copy import deepcopy
import numpy as np


class BanditAgent:
    def __init__(self, timelimit, id):
        self.timelimit = timelimit
        self.id = id

    def make_move(self, game):
        start = time.perf_counter()

        #
        run_simulation = True
        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            # replace the line below with your actual implementation!
            # break
            if run_simulation :
                # Show random success
                print("Random value function:", end="\n\t")
                value_function = get_random_value_function()
                agent_trial(value_function)

                # Show basic success
                print("Basic value function:", end="\n\t")
                value_function = init_value_table()
                agent_trial(value_function)

                # Train proper value function
                value_function = train_value_function(1000)

                # Show bad value function
                print("Bad value function:", end="\n\t")
                agent_trial(reverse_value_function(deepcopy(value_function)))

                # Show proper success
                print("Trained value function:", end="\n\t")
                agent_trial(value_function)

                run_simulation = False
                continue

        # return the best move you've found here
        return game.board.random_free()

    def __str__(self):
        return f'Player {self.id} (BanditAgent)'


def is_tie(board):
    return (is_full(board)) and (not is_win(board, 1)) and (is_win(board, 2))


def is_full(board):
    return not board.__contains__(0)


def is_win(board, player):
    mask = board == player
    out = mask.all(0).any() | mask.all(1).any()
    out |= np.diag(mask).all() | np.diag(mask[:, ::-1]).all()
    return out


def is_terminal(board):
    return is_win(board, 1) or is_win(board, 2) or is_full(board)


def x_move(board, state_values):
    for i in range(3):
        for j in range(3):
            if board[i, j] != 0:
                continue
            move = (i, j)
            board[move] = 1
            if board.tobytes() in state_values:
                board[move] = 0
                continue
            elif is_win(board, 1):
                state_values[board.tobytes()] = 1.0
            elif is_full(board):
                state_values[board.tobytes()] = 0.0
            else:
                state_values[board.tobytes()] = 0.5
                state_values = o_move(board, state_values)
            board[move] = 0
    return state_values


def o_move(board, state_values):
    for i in range(3):
        for j in range(3):
            if board[i, j] != 0:
                continue
            move = (i, j)
            board[move] = 2
            if board.tobytes() in state_values:
                board[move] = 0
                continue
            elif is_win(board, 2):
                state_values[board.tobytes()] = 0.0
            elif is_full(board):
                # should this be 0? Unsure.
                state_values[board.tobytes()] = 1.0
            else:
                state_values[board.tobytes()] = 0.5
                state_values = x_move(board, state_values)
            board[move] = 0
    return state_values


def get_random_value_function():
    value_function = init_value_table()
    for k, v in deepcopy(value_function).items():
        value_function[k] = random.random()
    return value_function


def reverse_value_function(value_function):
    for k, v in deepcopy(value_function).items():
        value_function[k] = 1.0 - value_function[k]
    return value_function


def init_value_table():
    board = np.zeros((3, 3))
    state_values = x_move(board, {board.tobytes(): 0.5})
    return state_values

# def human_input(state):
#     row = input("\nrow: ")
#     col = input("\ncol: ")
#     while int(row) > 2 or int(row) < 0 or int(col) > 2 or int(col) < 0 or state[int(row), int(col)] != 0:
#         print("Invalid!")
#         row = input("\nrow: ")
#         col = input("\ncol: ")
#     return int(row), int(col)


def get_available_actions(state):
    #print(list(zip(list(np.where(state==0)[0]), list(np.where(state==0)[1]))))
    return list(zip(list(np.where(state == 0)[0]), list(np.where(state == 0)[1])))


def get_greedy_action(state, player_id, value_function, maximize):
    candidate_actions = get_available_actions(state)
    if len(candidate_actions) == 0:
        return None, None
    max_value = -np.inf
    if not maximize:
        max_value *= -1
    max_value_actions = [random.choice(candidate_actions)]
    max_value_states = [np.copy(state)]
    for candidate_action in candidate_actions:
        candidate_state = np.copy(state)
        candidate_state[candidate_action] = player_id
        value = value_function[candidate_state.tobytes()]
        # stochastic action decision
        if value == max_value:
            max_value_actions.append(candidate_action)
            max_value_states.append(candidate_state)
        elif maximize:
            if value > max_value:
                max_value = value
                max_value_actions = [candidate_action]
                max_value_states = [candidate_state]
        else:
            if value < max_value:
                max_value = value
                max_value_actions = [candidate_action]
                max_value_states = [candidate_state]

    index = random.choice(range(len(max_value_actions)))
    return max_value_actions[index], max_value_states[index]


class Agent:
    def __init__(self, _id):
        self.id = _id

    def update_value_function(self, state, past_state, value_function):
        return value_function


class AutonomousAgent(Agent):
    def __init__(self, _id, is_learning=False):
        super().__init__(_id)
        self.is_learning = is_learning
        self.stochastic = True


class Random(AutonomousAgent):
    def __init__(self, _id):
        super().__init__(_id, False)

    def get_action(self, state, value_function):
        return random.choice(get_available_actions(state))  # , value_function


class Greedy(AutonomousAgent):
    def __init__(self, _id, step_size=0.001, is_learning=False):
        super().__init__(_id, is_learning)
        self.step_size = step_size

    def get_action(self, state, value_function):
        greedy_action, _ = get_greedy_action(
            state, self.id, value_function, self.id == 1)
        return greedy_action

    def update_value_function(self, state, past_state, value_function):
        result_value_function = deepcopy(value_function)
        if past_state is not None and self.is_learning:
            # temporal difference: update value of previous state based on current state
            result_value_function[past_state.tobytes()] = result_value_function[past_state.tobytes(
            )] + (self.step_size * (result_value_function[state.tobytes()] - result_value_function[past_state.tobytes()]))
        return result_value_function


class E_greedy(Greedy):
    def __init__(self, _id, step_size=0.1, e=0.2, is_learning=True):
        super().__init__(_id, step_size, is_learning)
        self.epsilon = e

    def get_action(self, state, value_function):
        if random.random() <= self.epsilon:
            # , value_function
            return random.choice(get_available_actions(state))
        else:
            return super().get_action(state, value_function)

def train_value_function(n_games=10):
    value_function = init_value_table()
    values = list(value_function.values())
    #print(set(values))
    #print(f"number of distinct state values = {len(set(values))}")
    o_value_function = deepcopy(value_function)
    x_value_function = deepcopy(value_function)

    # train vs Random
    for i in range(n_games):
        x_value_function, o_value_function, _ = game(Random(1), E_greedy(2), x_value_function, o_value_function)
    for i in range(n_games):
        x_value_function, o_value_function, _ = game(E_greedy(1), Random(2), x_value_function, o_value_function)

    # train vs E_greedy (e = 0.5)
    for i in range(n_games):
        x_value_function, o_value_function, _ = game(E_greedy(1,0,0.5,False), E_greedy(2), x_value_function, o_value_function)
    for i in range(n_games):
        x_value_function, o_value_function, _ = game(E_greedy(1), E_greedy(2,0,0.5,False), x_value_function, o_value_function)

    result_value_function = {**x_value_function, **o_value_function}
    values = list(result_value_function.values())
    #print(set(values))
    #print(f"number of distinct state values = {len(set(values))}")
    pickle.dump(result_value_function, open("value_function.pkl", "wb"))
    return result_value_function


def render_state(state):
    for i in range(3):
        for j in range(3):
            cell = state[i, j]
            if cell == 0:
                print(".", end=" ")
            if cell == 1:
                print("X", end=" ")
            if cell == 2:
                print("O", end=" ")
        print("")
    print("")


def game(x_player, o_player, x_value_function, o_value_function, render=False):
    state = np.zeros((3, 3))
    x_past_state = None
    o_past_state = np.copy(state)
    iteration = 0
    while not is_terminal(state):
        x_action = x_player.get_action(state, x_value_function)
        state[x_action] = x_player.id

        # if render:
        #     render_state(state)

        if iteration > 0:
            x_value_function = x_player.update_value_function(
                state, x_past_state, x_value_function)

        x_past_state = np.copy(state)
        end_code = 1

        if is_tie(state):
            end_code = 0
        
        if is_terminal(state):
            return x_value_function, o_value_function, end_code


        o_action = o_player.get_action(state, o_value_function)
        state[o_action] = o_player.id

        # if render:
        #     render_state(state)

        o_value_function = o_player.update_value_function(
            state, o_past_state, o_value_function)
        o_past_state = np.copy(state)
        end_code = 2

        if is_tie(state):
            end_code = 0

        if is_terminal(state):
            return x_value_function, o_value_function, end_code

        iteration += 1


def agent_trial(value_function):
    wins = 0
    games = 0
    for i in range(100):
        _, _, end_code = game(Greedy(1), Random(2), deepcopy(
            value_function), deepcopy(value_function))
        games += 1
        if end_code == 1:
            wins += 1
    for i in range(100):
        _, _, end_code = game(Random(1), Greedy(2), deepcopy(
            value_function), deepcopy(value_function))
        games += 1
        if end_code == 2:
            wins += 1
    ratio = wins / float(games) * 100
    print(f"Won {ratio}% against random agent")
