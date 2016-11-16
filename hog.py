"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    k = 0
    roll_one = 1   #if a one is rolled, B becomes 0
    total_score = 0
    while k < num_rolls:
        current_roll = dice()
        if current_roll == 1:
            roll_one = 0
        total_score = total_score + current_roll
        k = k + 1
    return total_score * roll_one
    # END Question 1

def is_prime(n):
    if n == 1 or n== 0:
        return False
    prime = True
    k = n - 1
    while k > 1:
        if n % k == 0:
            prime = False
        k = k - 1
    return prime

def next_prime(n):
    k = n + 1   # checks first number after n if it is prime
    prime = False   # assumes value is not prime
    while not prime:
        prime = is_prime(k)   # checks if value is prime, setting prime to True
        k = k + 1
    return k - 1  # minus one negates the k + 1 above after finding first prime

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls == 0:
        total = max(opponent_score // 10, opponent_score % 10) + 1
    if num_rolls != 0:
        total = roll_dice(num_rolls, dice)
    if is_prime(total):
        total = next_prime(total)
    return total
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    s0 = score0
    s1 = score1
    if s0 >= 100:
        s0 = s0 - 100
    if s1 >= 100:
        s1 = s1 - 100
    if (s0 % 10) == (s1 // 10) and (s0 // 10) == (s1 % 10):
        return True
    return False
    # END Question 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    while score0 < goal and score1 < goal:
        if player == 0:
            strat0 = strategy0(score0, score1)
            current_turn = take_turn(strat0, score1, select_dice(score0, score1))
            if current_turn == 0:
                score1 = score1 + strat0
            score0 = score0 + current_turn
        else:
            strat1 = strategy1(score1, score0)
            current_turn = take_turn(strat1, score0, select_dice(score1, score0))
            if current_turn == 0:
                score0 = score0 + strat1
            score1 = score1 + current_turn
        if is_swap(score0, score1) == True:
            score0, score1 = score1, score0
        player = other(player)

    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def average_and_return(*args):
        n = num_samples
        tot_sum = 0
        while n > 0:
            result = fn(*args)
            tot_sum = tot_sum + result
            n = n - 1
        return tot_sum / num_samples
    return average_and_return
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    n = 1
    max_val = 0
    max_num = 1
    while n <= 10:
        avg = make_averaged(roll_dice, num_samples)(n, dice)
        if avg > max_val:
            max_val = avg
            max_num = n
        n = n + 1
    return max_num
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    max_bacon = max(opponent_score // 10, opponent_score % 10) + 1
    if is_prime(max_bacon):
        max_bacon = next_prime(max_bacon)
    if max_bacon >= margin:
        return 0
    return num_rolls
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    swap_bacon = max(opponent_score // 10, opponent_score % 10) + 1
    if is_prime(swap_bacon):
        swap_bacon = next_prime(swap_bacon)
    swap_possible = is_swap(swap_bacon + score, opponent_score)
    if swap_possible and (score + swap_bacon) < opponent_score:
        return 0
    else:
        return num_rolls

    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    First part incorporates idea of swap_strategy.
    Next part prevents any unfavorable swaps in the opponents favor.
    The next part checks if using Free Bacon will get to 100 right away.
    Next, if close to 100, there are smaller rolls that are safer to play.
    Finally, if margin is 6 or more, the final strategy will use Free Bacon...
    Otherwise, I found 4 to be the most optimal roll.
    """
    # BEGIN Question 10
    #incorporates idea of swap_strategy for favorable swaps
    swap_bacon = max(opponent_score // 10, opponent_score % 10) + 1
    if is_prime(swap_bacon):
        swap_bacon = next_prime(swap_bacon)
    swap_possible = is_swap(swap_bacon + score, opponent_score)
    if swap_possible and (score + swap_bacon) < opponent_score:
        return 0
        #prevents unfavorable swaps
    if swap_possible and (score + swap_bacon) > opponent_score:
        return 4
    if (score + swap_bacon) >= 100: #checks if Free Bacon will get to 100
        return 0
    # if close to 100, smaller rolls can be more optimal to reaching 100
    if 88 <= score <= 97:
        return 3
    if score > 97:
        return 2
    #incorporates idea of bacon_strategy
    margin = 6
    max_bacon = max(opponent_score // 10, opponent_score % 10) + 1
    if is_prime(max_bacon):
        max_bacon = next_prime(max_bacon)
    if max_bacon >= margin:
        return 0
    return 4
    # END Question 10
    # and not (is_swap and score + max_bacon > opponent_score):


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
