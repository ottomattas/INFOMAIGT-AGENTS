# Bandit Agent

## Description
In the lecture, we learned about the k-armed Bandit problem. We saw several strategies to find the best reward in this general setting (epsilon-greedy, upper-confidence bound, etc). Furthermore, we saw how a strategy for the k-armed bandit problem can be applied to finding an optimal move in a simple turn-based two player game using simulations. In this exercise, we give you a Python framework to apply your knowledge in practice for the following game.

The game has a rectangular board and a set of shapes. Two players take turns placing stones on the board until one player forms one of the given shapes. That player then wins. If the board is full the game is a draw. In this exercise, you are supposed to program an agent that is capable of playing this game and produces a valid turn within a given time bound.

Your agent should be able to work with any board size, objective shapes and time bound. Your task is to program an agent that consistently wins against a random agent. You are supposed to use the strategies from the lecture or very similar strategies. We will test your agent and look at the code. The number of points for this exercise are based on two criteria:

1. How well does your agent perform against a random agent (see below for some benchmarks to give you an idea of the expected performance).
2. Do you employ an agent based on simulations of the game.

While we encourage creative solutions, we are aware that there are problem-specific ideas which work quite well in this scenario, but they will stop working in what is to come later in the course. This is also why we are not fixing the shapes we are using in advance. We want you to produce a general agent that can deal with many different situations.

## How to use the code
###### *Template files provided in the course are uploaded to the [./Assets](./Assets) folder.*

Make sure you followed the instructions on how to install Python on the "Implementation Projects" page, then download and unzip the attached files. The setup of the project is very straightforward:

- main.py: initialises everything and runs the games.
- game.py: makes the players take turns, and checks when someone has won.
- board.py: tracks the board state, and has utility functions for finding open spots, checking if the board is full, etc.
- random_agent.py: the random agent you'll be playing against.
- bandit_agent.py: a template into which you will implement your own agent.

The code relies on the *numpy* library, so **you should install this** by running `pip install numpy` from a terminal (or `pip3 install numpy` on some Linux distros).

If you installed Python properly, you will be able to run the program by opening up a terminal in the directory where you put the files, and running `python main.py` (or `./main.py` on Linux; you may need to change `python` to `python3` on the first line of that file for this to work). The program has the following arguments available (also viewable by running the program with the `--help` argument):

- --games <number> : plays the given number of games, default is one.
- --size <number>: plays on a board with the given side length, default is ten.
- --time <number>: the number of milliseconds each agent is allowed to spend per move.
- --print-board <option>: with option `all`, prints the board state after every move. With option `final`, only shows the final board state. When this argument is not given, no board state will be printed.
- --parallel <number>: if present, the program will run the given number of games in parallel. It is recommended to only use this when you're ready to do large-scale tests, as it makes debugging harder.
- positional argument "objectives": the path to a file containing the objective shapes. A file shapes.txt is provided to show what this looks like, but we will use different shapes when testing your submission.

So, for example, you might run the program like this:
```
python main.py --games 100 --size 8 --time 500 --print-board final shapes.txt
```
to run 100 games on an 8x8 board with 500ms per move, printing only the final board state.

## Implementing your agent
In the provided code, you will find a bandit_agent.py file: this is where you should implement your agent. It has a make_move method that takes a Game object as a parameter. It also already takes care of measuring the time for your move. You can access the current board state via game.board. Note that for this assignment, **you are not allowed to use knowledge about the objective shapes** to help your agent decide which move to make (i.e. don't try to come up with a strategy yourself and program it into your agent).

You are free to modify any parts of the provided code that you wish, but keep in mind that **you will only submit the bandit_agent.py** file! Your agent should therefore not rely on changes to any other part of the code.

Finally, a small hint: your agent will need to do a lot of simulations based on a random agent. It just so happens that a random agent is already implemented, as it is the opponent you will be playing against. An easy way to simulate a game is to create a copy of the board (look up how to create a deep copy in Python, to avoid modifying the original unintentionally) and then use the `Game.from_board` method to create a new game from the given board state, using two new random agents. Then you can just play the game by calling `Game.play()`, which returns the agent that won the game, or `None` if it was a tie.

## Benchmarks
We will test your code on seven different cases. Here we give you the results of student submissions on three test cases we used last year. At least one of these cases will also be used this year. The cases were as follows:

1. Tic-tac-toe, 100ms per move
2. 3x3 X-shape, 8x8 board, 500ms per move
3. 3x3 block without centre, 8x8 board, 1000ms per move

In the table below, we show the performance of student submissions on these test cases. The format is wins/losses/draws.
| grade         | case 1           | case 2        | case 3        |
| ------------- | -------------    | ------------- | ------------- |
| 10            | 955/12/33    | 100 / 0 / 0   | 94/0/6   |
| 7             | 837/140/23   | 97/2/1    | 56/8/36    |
| 7             | 686/275/39  | 87/13/0  | 94/0/6   |
| 3             | 439/463/98  | 50/40/10  | 8/7/85   |

As you can see, the submission that was graded a 10 is winning almost all its games. The submissions that received a 7 do well in some cases, but underperform in others. The submission that received a 3 has about the same performance as a random agent.

Note that the tests are run on a fairly powerful PC (Core i9 9900K), your performance may be a bit worse in your local tests, as you will be able to perform fewer roll-outs in the given time.

## Submission
You will work on this project individually. You should **submit only your bandit_agent.py** file. Make sure to enter your name and student number in the space provided at the top of this file.
