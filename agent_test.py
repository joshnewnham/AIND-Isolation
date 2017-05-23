"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import sample_players
import isolation
import game_agent
import random 

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
    
    def test_single_min_max(self):
        width, height = 7, 7
        #timeout = float("-inf")
        timeout = 10.

        self.player1 = game_agent.MinimaxPlayer(
            search_depth=3, 
            score_fn=game_agent.custom_score, 
            timeout=timeout)
        
        self.player2 = sample_players.GreedyPlayer(
            score_fn=game_agent.custom_score_3)

        self.game = isolation.Board(self.player1, self.player2, width=width, height=height)

        #self.game.apply_move((random.randint(0, self.game.width-1), random.randint(0, self.game.height-1)))
        #self.game.apply_move((random.randint(0, self.game.width-1), random.randint(0, self.game.height-1)))
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

    # def _test_single_alpha_pruning(self):
    #     width, height = 7, 7
    #     #timeout = float("-inf")
    #     timeout = 10.

    #     num_games = 10

    #     player_1_wins = 0 
    #     player_2_wins = 0 

    #     for _ in range(0, num_games):

    #         self.player1 = game_agent.AlphaBetaPlayer(
    #             search_depth=20, 
    #             score_fn=game_agent.custom_score, 
    #             timeout=timeout)
            
    #         self.player2 = game_agent.AlphaBetaPlayer(
    #             search_depth=20, 
    #             score_fn=game_agent.custom_score_3, 
    #             timeout=timeout)

    #         #self.player2 = sample_players.GreedyPlayer(sample_players.improved_score)
            
    #         self.game = isolation.Board(self.player1, self.player2, width=width, height=height)

    #         self.game.apply_move((random.randint(0, self.game.width-1), random.randint(0, self.game.height-1)))
    #         self.game.apply_move((random.randint(0, self.game.width-1), random.randint(0, self.game.height-1)))
            
    #         #print(self.game.to_string())

    #         # players take turns moving on the board, so player1 should be next to move
    #         assert(self.player1 == self.game.active_player)

    #         # get a list of the legal moves available to the active player
    #         #print(self.game.get_legal_moves())

    #         # # play the remainder of the game automatically -- outcome can be "illegal
    #         # # move", "timeout", or "forfeit"
    #         winner, history, outcome = self.game.play()

    #         player_1_wins += 1 if winner == self.player1 else 0
    #         player_2_wins += 1 if winner == self.player2 else 0
            
    #         # winner, history, outcome = self.game.play()
    #         # print("\nWinner: {}\nOutcome: {}".format("player 1" if winner == self.player1 else "player 2", outcome))
    #         # print("\nstate:\n{}".format(self.game.to_string()))
    #         # print("\nhistory:\n{}".format(history))

    #     print("summary from {} games; \n\tplayer 1 wins: {} \n\tplayer 2 wins: {}".format(
    #         num_games, player_1_wins, player_2_wins))

if __name__ == '__main__':
    unittest.main()
