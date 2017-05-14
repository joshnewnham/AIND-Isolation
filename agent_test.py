"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import random 

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer(3, game_agent.custom_score, 10)
        self.player2 = game_agent.MinimaxPlayer(3, game_agent.custom_score, 10)
        self.game = isolation.Board(self.player1, self.player2)
    
    def test_min_max(self):
        width, height = 7, 7
        #timeout = float("-inf")
        timeout = 10.

        self.player1 = game_agent.MinimaxPlayer(
            search_depth=3, 
            score_fn=game_agent.custom_score, 
            timeout=timeout)
        self.player2 = game_agent.MinimaxPlayer(
            search_depth=4, 
            score_fn=game_agent.custom_score, 
            timeout=timeout)
        self.game = isolation.Board(self.player1, self.player2, width=width, height=height)

        self.game.apply_move((random.randint(0, self.game.width-1), random.randint(0, self.game.height-1)))
        self.game.apply_move((random.randint(0, self.game.width-1), random.randint(0, self.game.height-1)))
        print(self.game.to_string())

        # players take turns moving on the board, so player1 should be next to move
        assert(self.player1 == self.game.active_player)

        # get a list of the legal moves available to the active player
        print(self.game.get_legal_moves())

        # play the remainder of the game automatically -- outcome can be "illegal
        # move", "timeout", or "forfeit"
        winner, history, outcome = self.game.play()
        print("\nWinner: {}\nOutcome: {}".format("player 1" if winner == self.player1 else "player 2", outcome))
        print("\nstate:\n{}".format(self.game.to_string()))
        print("\nhistory:\n{}".format(history))

if __name__ == '__main__':
    unittest.main()
