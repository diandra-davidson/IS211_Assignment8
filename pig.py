#!/usr/bin/env
# -*- coding: utf-8 -*-
"""IS211 Assignment 7 by Diandra Vega"""


import sys
import random
import argparse


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--player1', help='Choose player type of player one.'
                                      ' [Human | Computer]')
PARSER.add_argument('--player2', help='Choose player type of player two.'
                                      ' [Human | Computer]')
PARSER.add_argument('--timed', help='How long the game will run in seconds.')
ARGS = PARSER.parse_args()


class Player(object):
    """Players in game of Pig"""
    def __init__(self, score=0):
        """Constructor"""
        self.score = score


    def playerChoice(self):
        """Roll or hold"""
        playerdecision = raw_input("Do you want to roll or hold? [r|h] ")

        while True:
            if playerdecision is 'r':
                roll = playerdecision
                return roll
                break
            elif playerdecision is 'h':
                hold = playerdecision
                return hold
                break
            else:
                print "Invalid choice."
                break


    def totalScore(self, points=0):
        """Tally player score"""
        self.score += points
        result = self.score
        return result


class Game(object):
    """Play a game of Pig"""

    def status(self, firstscore, secondscore):
        """Check if any player hit a score of 100"""
        if firstscore >= 100:
            result = "Player 1 wins!"
            print result
            sys.exit(1)
        elif secondscore >= 100:
            result = "Player 2 wins!"
            print result
            sys.exit(1)
        else:
            return False


    def rollDice(self, player, choice=None):
        """Roll the dice"""
        dice = list(xrange(1, 7))
        roll = 'r'
        hold = 'h'

        if choice is None:
            playerchoice = player.playerChoice()
        else:
            playerchoice = choice

        if playerchoice is roll:
            diceroll = random.choice(dice)
            player.totalScore(diceroll)
            result = "You rolled a {}. Your turn now ends. Your total" \
                     " score is {}.\n".format(diceroll, player.score)
            print result
            return diceroll, player.score

        elif playerchoice is hold:
            result = "You decided to hold. Your turn now ends. Your total" \
                     " score is {}.\n".format(player.score)
            print result
            return playerchoice, player.score


class HumanPlayer(Player):
    """Human player derived from Player()"""


class ComputerPlayer(Player):
    """Computer player derived from Player()"""

    def makeChoice(self):
        """Computer makes a choice using it's own logic."""
        return


class PlayerFactory(object):
    """Factory class - Instantiates the correct object as request comes in.
    Also doubles as a proxy pattern for timed games."""


class TimedGameProxy(Game):
    """Proxy class - Will check if time in game is up, then determine which
    player has the highest score to declare the winner."""

    def processTime(self, playerone, playertwo, time):
        """Time a game in seconds with two players"""
        raise Exception
        return


def processTurn(player, choice=None):
    """Process the turn"""
    playgame = Game()

    if choice is None:
        plyr_choice = player.playerChoice()
    else:
        plyr_choice = choice

    plyr_result = playgame.rollDice(player, plyr_choice)

    if plyr_choice is 'h':
        turn_ends = True
        return plyr_choice, turn_ends

    if plyr_result[0] != 1:
        turn_ends = False
        return turn_ends

    if plyr_result[0] == 1:
        turn_ends = True
        return plyr_result[0], turn_ends


def playGame():
    """Run the game"""
    playgame = Game()
    playerone = Player()
    playertwo = Player()
    start_plyr_one = "Player 1's turn begins:" + "\n"
    start_plyr_two = "Player 2's turn begins:" + "\n"

    while True:
        while playgame.status(playerone.score, playertwo.score) == False:
            print "\n" + start_plyr_one
            plyr_one_turn = processTurn(playerone)

            if plyr_one_turn == False:
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    continue
            elif plyr_one_turn == (1, True):
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    print "Since you rolled a 1, your turn will now end."
                    break
            elif plyr_one_turn == ('h', True):
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    break

        while playgame.status(playerone.score, playertwo.score) == False:
            print "\n" + start_plyr_two
            plyr_two_turn = processTurn(playertwo)

            if plyr_two_turn == False:
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    continue
            elif plyr_two_turn == (1, True):
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    print "Since you rolled a 1, your turn will now end."
                    break
            elif plyr_two_turn == ('h', True):
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    break
        continue
    return


if __name__ == '__main__':
    """Run the game"""
    print playGame()
