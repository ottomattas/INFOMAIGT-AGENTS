# Monte Carlo Tree Search Agent

## Description

In the lecture, we learned about the Monte Carlo Tree Search (MCTS). We saw how it can be used to explore the game tree. Also, we saw how it can be used together with some base agent. In this exercise, you will take a random base agent for the same game as the previous project, and apply MCTS to it. In addition, you will implement an agent based on a score function.

Your agent should be able to work with any board size, objective shapes and time bound. Your task is to show that you can make the base agent better by applying MCTS. We will test both your agents against a random agent and look at the code. The number of points for this exercise is based on several criteria:

1. How much does the random agent improve by applying MCTS? (80%)
2. Does your score-based agent consistently beat a random agent? (20%)

While we encourage creative solutions, we forbid you to use neural networks in this exercise. This is also why we are not fixing the shapes, board sizes and time-bounds we are using to test your agent. We want you to produce a general agent that can deal with many different situations.

## How to use the code

See the Bandit Agent assignment for a description of the main files and how to use them. The new template supplies two different agent files, score_agent.py and mcts_agent.py. These are currently both random agents, but your task is to turn the ScoreAgent class into an agent that plays the game according to a policy defined by some score function, and to turn the MCTSAgent class into an agent that performs MCTS, using roll-outs with random agents for the simulation.

## Benchmarks

We will test your MCTS agent on several different cases. Here we give you the results of student submissions on three test cases we used last year. At least one of these cases will also be used this year. The cases were as follows:

1. Tic-tac-toe, 100ms per move
2. 3x3 X-shape, 8x8 board, 500ms per move
3. All rotations of a 4x2 L-shape, 8x8 board, 500ms per move

In the table below, we show the performance of student submissions on these test cases. The format is wins/losses/draws.

| grade         | case 1           | case 2        | case 3        |
| ------------- | -------------    | ------------- | ------------- |
| 10            | 943 / 28 / 29    | 100 / 0 / 0   | 100 / 0 / 0   |
| 8             | 636 / 295 / 69   | 95 / 5 / 0    | 91 / 9 / 0    |
| 6             | 644 / 156 / 200  | 69 / 16 / 15  | 82 / 18 / 0   |

As you can see, the submission that was graded a 10 is winning almost all its games. The submission that received an 8 does well in two cases, but underperforms in the first. The submission that received a 6 does better than a random agent, but there is a lot of room for improvement.

The score agent should be able to win (almost) all games in every test case against a random agent.

Note that the tests are run on a fairly powerful PC (Core i9 9900K), your performance may be a bit worse in your local tests, as you will be able to perform fewer roll-outs in the given time.

## Submission

You will work on this project individually. You should submit only your **score_agent.py and mcts_agent.py files**. Make sure to enter your name and student number in the space provided at the top of this file.
