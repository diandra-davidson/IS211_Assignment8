#!/usr/bin/env
# -*- coding: utf-8 -*-
"""IS211 Assignment 7 by Diandra Vega"""


import sys
import random
import argparse
import os
import time


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

            if diceroll == 1:
                print "You rolled a {}. Your turn now ends. Your total score" \
                      " is {}.\n".format(diceroll, player.score)
            else:
                print "You rolled a {}. Your total score is {}." \
                      "\n".format(diceroll, player.score)

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

    def makeChoice(self, dice=0):
        """Computer makes a choice using it's own logic."""
        self.turntotal += dice
        computer_score = self.score
        print self.turntotal

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

        elif 100 - computer_score < 25:
            new_hold = 100 - computer_score
            if self.turntotal <= new_hold:
                choice = 'r'
                turn_ends = False
            else:
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


def playGame(p_one, p_two):
    """Run the game"""
    playgame = Game()

    if p_one.lower() == 'human':
        p_one_name = "Player 1"
        playerone = Player()
    elif p_one.lower() == 'computer':
        p_one_name = "Computer Player 1"
        playerone = ComputerPlayer()

    if p_two.lower() == 'human':
        p_two_name = "Player 2"
        playertwo = Player()
    elif p_two.lower() == 'computer':
        p_two_name = "Computer Player 2"
        playertwo = ComputerPlayer()


    start_plyr_one = "{} 's turn: \n".format(p_one_name)
    start_plyr_two = "{} 's turn: \n".format(p_two_name)

    while True:
        ### Reset counter at beginning of loop ###
        counter = 0
        while playgame.status(playerone.score, playertwo.score) == False:
            print "\n" + start_plyr_one
            if p_one == 'human':
                choice = raw_input("Do you want to roll or hold? [r|h] ")
                plyr_one_turn = playerone.playerChoice(choice)

                if plyr_one_turn[1] == False:
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    else:
                        roll = playgame.rollDice(playerone, plyr_one_turn[0])
                        if roll == 1:
                            time.sleep(3)
                            break
                        else:
                            time.sleep(1)
                            continue
                elif plyr_one_turn == ('h', True):
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    else:
                        playgame.rollDice(playerone, plyr_one_turn[0])
                        time.sleep(1)
                        break
            elif p_one == 'computer':
                ### Reset turntotal at beginning of computer turn ###
                playerone.turntotal = 0
                choice = playerone.makeChoice(counter)

                if choice == ('r', False):
                    print "{} rolls!".format(p_one_name)
                    plyr_one_turn = playgame.rollDice(playerone, choice[0])
                    counter += plyr_one_turn
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    elif plyr_one_turn == 1:
                        time.sleep(3)
                        playerone.turntotal += counter
                        break
                    else:
                        time.sleep(2)
                        continue
                elif choice == ('h', True):
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    else:
                        print "{} decided to hold. Turn ends.".format(p_one_name)
                        playgame.rollDice(playerone, choice[0])
                        playerone.turntotal = 0
                        time.sleep(2)
                        break

        while playgame.status(playerone.score, playertwo.score) == False:
            print "\n" + start_plyr_two
            if p_two == 'human':
                choice = raw_input("Do you want to roll or hold? [r|h] ")
                plyr_two_turn = playertwo.playerChoice(choice)

                if plyr_two_turn[1] == False:
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    else:
                        roll = playgame.rollDice(playertwo, plyr_two_turn[0])
                        if roll == (1, True):
                            time.sleep(3)
                            break
                        else:
                            continue
                elif plyr_two_turn == ('h', True):
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    else:
                        break
            elif p_two == 'computer':
                choice = playertwo.makeChoice()

                if choice == ('r', False):
                    print "{} rolls!".format(p_two_name)
                    plyr_two_turn = playgame.rollDice(playertwo, choice[0])
                    if playgame.status(playerone.score,
                                       playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    elif plyr_two_turn == 1:
                        time.sleep(3)
                        break
                    else:
                        time.sleep(2)
                        continue
                elif choice == ('h', True):
                    if playgame.status(playerone.score, playertwo.score) == True:
                        print playgame.status(playerone.score, playertwo.score)
                        break
                    else:
                        print "{} decided to hold. Turn ends.".format(p_two_name)
                        playgame.rollDice(playertwo, choice[0])
                        time.sleep(2)
                        break
                else:
                    print "Something happened!"
    return


if __name__ == '__main__':
    """Run the game"""
    if ARGS.player1 and ARGS.player2:
        print playGame(ARGS.player1, ARGS.player2)
    else:
        print "Invalid arguments specified. Please see python pig.py -h for " \
              "help."
        os.system('python pig.py -h')
