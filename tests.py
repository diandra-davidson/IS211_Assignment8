##!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment 7 by Diandra Vega - Unit tests for pig.py"""


import unittest
import pig


class gameTests(unittest.TestCase):
    """Unit tests for Pig game in pig.py"""
    max_score = 100
    dice_rolls = list(xrange(1, 7))


    def testGameEndsAtMaxScore(self):
        """Game exits when a player reaches a score of 100"""
        piggame = pig.Game()
        player_one = pig.Player()
        player_two = pig.Player()
        plyr_one_score = player_one.score + self.max_score
        plyr_two_score = player_two.score + self.max_score
        with self.assertRaises(SystemExit) as cm:
            piggame.status(plyr_one_score, plyr_two_score)
        self.assertEqual(cm.exception.code, 1, "Game did not exit")

#
    def testTurnEndsAtOne(self):
        """Player turn ends at dice roll of one"""
        playgame = pig.Game()
        player = pig.Player()
        while True:
            result = playgame.rollDice(player, 'r')
            if result == 1:
                self.assertEqual(result, 1, "Turn did not end at 1")
                break
            else:
                continue


    def testPlayerHold(self):
        """Turn ends if player holds"""
        playgame = pig.Game()
        playerone = pig.Player()
        result = playgame.rollDice(playerone, 'h')
        self.assertEqual(result, 'h', "Turn did not end at hold")


    def testScoreAddsToTotal(self):
        """Turn score adds to total"""
        playgame = pig.Game()
        playerone = pig.Player()
        rolldice = playgame.rollDice(playerone, 'r')
        self.assertEqual(rolldice, playerone.score, "Score did not add to"
                                                    " total score")

    def testComputerPlayer(self):
        """Test Ccmputer player logic"""
        play = pig.Game()
        computer = pig.ComputerPlayer()
        rolldice = play.rollDice(computer, 'r')
        computer_choice = computer.makeChoice(rolldice)

        while True:
            if rolldice == 1:
                self.assertEqual((1, True),
                                 (rolldice, computer_choice),
                                 "Turn did not end at one")
                break
            elif 100 - computer.score >= 25 and computer.turntotal < 25:
                self.assertEqual(('r', False), computer_choice,
                                 "Computer did not roll when turn total is less"
                                 " than 25")
                break

            elif 100 - computer.score < 25:
                new_hold = 100 - computer.score
                if computer.turntotal < new_hold:
                    self.assertEqual(('r', True), computer_choice,
                                     "Computer did not roll when score"
                                     " is less than 25 away from winning")
                    break
            else:
                continue


    def testTimedGame(self):
        """Testing timed games"""
        game_proxy = pig.TimedGameProxy()
        computer_one = pig.ComputerPlayer()
        computer_two = pig.ComputerPlayer()
        time_in_seconds = 60
        timer = game_proxy.processTime(computer_one, computer_two,
                                       time_in_seconds)
        if computer_one.score > computer_two.score:
            self.assertEqual("Computer One", timer, "Computer One did not win "
                                                    "with higher score")
        elif computer_two.score > computer_one.score:
            self.assertEqual("Computer Two", timer, "Computer Two did not win "
                                                    "with higher score")


if __name__ == '__main__':
    unittest.main()
