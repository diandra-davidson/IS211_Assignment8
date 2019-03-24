#!/usr/bin/env
# -*- coding: utf-8 -*-
"""IS211 Assignment 7 by Diandra Vega"""


import sys
import random
import argparse


#PARSER = argparse.ArgumentParser()
#PARSER.add_argument('--player1', help='Choose player type of player one.'
#                                      ' [Human | Computer]')
#PARSER.add_argument('--player2', help='Choose player type of player two.'
#                                      ' [Human | Computer]')
#PARSER.add_argument('--timed', help='How long the game will run in seconds.')
#ARGS = PARSER.parse_args()


class Player(object):
    """Players in game of Pig"""
    def __init__(self, score=0):
        """Constructor"""
        self.score = score


    def playerChoice(self, choice):
        """Roll or hold"""
#        playerdecision = raw_input("Do you want to roll or hold? [r|h] ")
        self.choice = choice

        if self.choice is 'h':
            turn_ends = True
        elif self.choice is 'r':
            turn_ends = False
        else:
            return "Invalid Choice"
        return choice, turn_ends


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

        if choice is roll:
            diceroll = random.choice(dice)
            player.totalScore(diceroll)
            print "You rolled a {}. Your total score is {}." \
                  "\n".format(diceroll, player.score)

            if diceroll == 1:
                print "You rolled a {}. Your turn now ends. Your total score" \
                      " is {}.\n".format(diceroll, player.score)
            return diceroll

        elif choice is hold:
            print "You decided to hold. Your turn now ends. Your total " \
                  "score is {}.\n".format(player.score)
            return choice


class HumanPlayer(Player):
    """Human player derived from Player()"""


class ComputerPlayer(Player):
    """Computer player derived from Player()"""

    def __init__(self, score=0, turntotal=0):
        Player.__init__(self, score)
        self.turntotal = turntotal

    def makeChoice(self, dice):
        """Computer makes a choice using it's own logic."""
        self.turntotal += dice
        computer_score = self.score

        if dice == 1:
            turn_ends = True
            return turn_ends
        elif 100 - computer_score >= 25:
            if self.turntotal < 25:
                choice = 'r'
                turn_ends = False

            elif self.turntotal >= 25:
                choice = 'h'
                turn_ends = True
            return choice, turn_ends


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
            choice = raw_input("Do you want to roll or hold? [r|h] ")
            plyr_one_turn = playerone.playerChoice(choice)

            if plyr_one_turn[1] == False:
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    roll = playgame.rollDice(playerone, plyr_one_turn[0])
                    if roll == (1, True):
                        break
                    else:
                        continue
            elif plyr_one_turn == ('h', True):
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    break

        while playgame.status(playerone.score, playertwo.score) == False:
            print "\n" + start_plyr_two
            choice = raw_input("Do you want to roll or hold? [r|h] ")
            plyr_two_turn = playerone.playerChoice(choice)

            if plyr_two_turn[1] == False:
                if playgame.status(playerone.score, playertwo.score) == True:
                    print playgame.status(playerone.score, playertwo.score)
                    break
                else:
                    roll = playgame.rollDice(playertwo, plyr_two_turn[0])
                    if roll == (1, True):
                        break
                    else:
                        continue
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
