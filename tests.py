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


    def testTurnEndsAtOne(self):
        """Player turn ends at dice roll of one"""
        player = pig.Player()
        result = pig.processTurn(player, 'r')
        while True:
            if result == (1, True):
                self.assertEqual(result, (1, True), "Turn did not end at 1")
                break
            else:
                continue


    def testPlayerHold(self):
        """Turn ends if player holds"""
        playgame = pig.Game()
        playerone = pig.Player()
        result = playgame.rollDice(playerone, 'h')
        self.assertEqual(result[0], 'h', "Turn did not end at hold")


    def testScoreAddsToTotal(self):
        """Turn score adds to total"""
        playgame = pig.Game()
        playerone = pig.Player()
        rolldice = playgame.rollDice(playerone, 'r')
        self.assertEqual(rolldice[0], playerone.score,
                         "Score did not add to total score")

    def testComputerPlayer(self):
        """Test Computer Rolls and Holds"""
        computer = pig.ComputerPlayer()
        computer_choice = computer.makeChoice()
        result = pig.processTurn(computer, computer_choice)
        if computer.score < 25:
            self.assertEqual(('h', True), result, "Computer did not hold when"
                                                  " score is less than 25")
        elif computer.score > 25:
            self.assertEqual(True, result, "Computer did not roll when score"
                                           "is above 25")


    def testTimedGame(self):
        """Testing timed games"""
        game_proxy = pig.GameProxy()
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
