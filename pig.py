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
        """Initialize player object with socore"""
        self.score = score


    def totalScore(self, points=0):
        """Tally player score"""
        self.score += points
        result = self.score
        return result


class HumanPlayer(Player):
    """Human player derived from Player()"""
    def playerChoice(self, choice):
        """Roll or hold"""
        self.choice = choice
        if self.choice is 'h':
            turn_ends = True
        elif self.choice is 'r':
            turn_ends = False
        else:
            return "Invalid Choice"
        return choice, turn_ends


class ComputerPlayer(Player):
    """Computer player derived from Player()"""
    def __init__(self, score=0, turntotal=0):
        """Initialize computer player object"""
        Player.__init__(self, score)
        self.turntotal = turntotal


    def makeChoice(self, dice=0):
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

    def definePlayer(self, player):
        """Determine player type"""
        if player.lower() == 'human':
            return HumanPlayer()
        elif player.lower() == 'computer':
            return ComputerPlayer()


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


    def checkTimer(self, firstscore, secondscore, start_time, maxtime):
        """Check if game timer has been reached"""
        calcTime = TimedGameProxy(maxtime)
        curr_time_elapsed = calcTime.processTime(start_time, maxtime)

        if curr_time_elapsed is True:
            print "Time's up!"
            if firstscore > secondscore:
                print "Player 1 wins!"
                sys.exit(1)
            elif secondscore > firstscore:
                print "Player 2 wins!"
                sys.exit(1)
        else:
            pass


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


    def playGame(self, p_one, p_two, timer=0):
        """Run the game"""
        definePlayers = PlayerFactory()
        playerone = definePlayers.definePlayer(p_one)
        playertwo = definePlayers.definePlayer(p_two)
        p_one_name = "Player 1"
        p_two_name = "Player 2"
        start_plyr_one = "{} 's turn: \n".format(p_one_name)
        start_plyr_two = "{} 's turn: \n".format(p_two_name)


        if timer != 0:
            start_time = time.time()


        while True:
            ### Reset counters at beginning of loop ###
            pone_counter = 0
            ptwo_counter = 0

            while self.status(playerone.score, playertwo.score) == False:
                print "\n" + start_plyr_one
                if p_one == 'human':
                    choice = raw_input("Do you want to roll or hold? [r|h] ")
                    plyr_one_turn = playerone.playerChoice(choice)

                    if plyr_one_turn[1] == False:
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            break
                        else:
                            roll = self.rollDice(playerone, plyr_one_turn[0])
                            if roll == 1:
                                time.sleep(2)

                                if timer != 0:
                                    self.checkTimer(playerone.score,
                                                    playertwo.score,
                                                    start_time,
                                                    timer)
                                break

                            else:
                                time.sleep(1)
                                if timer != 0:
                                    self.checkTimer(playerone.score,
                                                    playertwo.score,
                                                    start_time,
                                                    timer)
                                continue

                    elif plyr_one_turn == ('h', True):
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break
                        else:
                            self.rollDice(playerone, plyr_one_turn[0])
                            time.sleep(1)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            break

                elif p_one == 'computer':
                    ### Reset turntotal at beginning of computer turn ###
                    playerone.turntotal = 0
                    choice = playerone.makeChoice(pone_counter)

                    if choice == ('r', False):
                        print "{} rolls!".format(p_one_name)
                        plyr_one_turn = self.rollDice(playerone, choice[0])
                        pone_counter += plyr_one_turn
                        if timer != 0:
                            self.checkTimer(playerone.score,
                                            playertwo.score,
                                            start_time,
                                            timer)

                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break

                        elif plyr_one_turn == 1:
                            playerone.turntotal += pone_counter
                            time.sleep(2)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            break

                        else:
                            time.sleep(2)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            continue

                    elif choice == ('h', True):
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break
                        else:
                            print "{} decided to hold." \
                                  " Turn ends.".format(p_one_name)
                            self.rollDice(playerone, choice[0])
                            time.sleep(2)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)

                            break

            while self.status(playerone.score, playertwo.score) == False:
                print "\n" + start_plyr_two
                if p_two == 'human':
                    choice = raw_input("Do you want to roll or hold? [r|h] ")
                    plyr_two_turn = playertwo.playerChoice(choice)

                    if plyr_two_turn[1] == False:
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break
                        else:
                            roll = self.rollDice(playertwo, plyr_two_turn[0])
                            if roll == 1:
                                time.sleep(3)
                                if timer != 0:
                                    self.checkTimer(playerone.score,
                                                    playertwo.score,
                                                    start_time,
                                                    timer)
                                break
                            else:
                                if timer != 0:
                                    self.checkTimer(playerone.score,
                                                    playertwo.score,
                                                    start_time,
                                                    timer)
                                continue

                    elif plyr_two_turn == ('h', True):
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break
                        else:
                            self.rollDice(playerone, plyr_one_turn[0])
                            time.sleep(1)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            break

                elif p_two == 'computer':
                    ### Reset turntotal at beginning of computer turn ###
                    playertwo.turntotal = 0
                    choice = playertwo.makeChoice(ptwo_counter)

                    if choice == ('r', False):
                        print "{} rolls!".format(p_two_name)
                        plyr_two_turn = self.rollDice(playertwo, choice[0])
                        ptwo_counter += plyr_two_turn
                        self.checkTimer(playerone.score,
                                        playertwo.score,
                                        start_time,
                                        timer)
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break
                        elif plyr_two_turn == 1:
                            playertwo.turntotal += ptwo_counter
                            time.sleep(2)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            break
                        else:
                            time.sleep(2)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            continue

                    elif choice == ('h', True):
                        if self.status(playerone.score,
                                       playertwo.score) == True:
                            print self.status(playerone.score, playertwo.score)
                            break
                        else:
                            print "{} decided to hold." \
                                  " Turn ends.".format(p_two_name)
                            self.rollDice(playertwo, choice[0])
                            time.sleep(2)
                            if timer != 0:
                                self.checkTimer(playerone.score,
                                                playertwo.score,
                                                start_time,
                                                timer)
                            break
                    else:
                        raise Exception("Something went wrong")
        return


class TimedGameProxy(Game):
    """Proxy class - Will check if time in game is up, then determine which
    player has the highest score to declare the winner."""

    def __init__(self, maxtime):
        """Initialize new object"""
        self.maxtime = maxtime


    def processTime(self, start_time, maxtime):
        """Time a game in seconds with two players"""
        elapsed_time = time.time() - start_time

        if elapsed_time >= float(maxtime):
            return True
        elif elapsed_time != float(maxtime):
            return False


    def playTimedGame(self, playerone, playertwo, maxtime):
        """Play a timed game of Pig"""
        self.playGame(playerone, playertwo, maxtime)
        return


if __name__ == '__main__':
    """Run the game"""
    if ARGS.player1 and ARGS.player2 and not ARGS.timed:
        playgame = Game()
        print playgame.playGame(ARGS.player1, ARGS.player2)
    elif ARGS.player1 and ARGS.player2 and ARGS.timed:
        playgame = TimedGameProxy(ARGS.timed)
        print playgame.playTimedGame(ARGS.player1, ARGS.player2, ARGS.timed)
    else:
        print "Invalid arguments specified. Please see python pig.py -h for " \
              "help."
        os.system('python pig.py -h')
