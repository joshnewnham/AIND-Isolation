"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import time

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score_timer(func):
    def inner(game, player):
        start_time = time.time()
        result = func(game, player)
        end_time = time.time()

        elapsed_time = end_time - start_time
        player.time_logging.append(elapsed_time)
        return result 
    return inner

@custom_score_timer
def custom_score(game, player):
    import math 
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    An uber evaluator that captures small heuristics, first evaluating if the 
    game is won (player or opponent) or tied otherwise assessing:
    - Incentivising moving the player towards the center 
    - Ratio of moves remaining between the player and opponent 
    - Incentivising pushing the opponent towards the corner and edge 

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player)) 

    if len(own_moves) != 0 and len(opp_moves) == 0:
        return float("inf")
    elif len(own_moves) == 0 and len(opp_moves) != 0:
        return float("-inf")
    elif len(own_moves) == 0 and len(opp_moves) == 0:
        return -10 

    score = 0.0 

    current_pos = game.get_player_location(player)
    opp_current_pos = game.get_player_location(game.get_opponent(player))    

    # higher score for moving our player closer to the centre 
    center_pos = (game.width/2, game.height/2) 

    # define some weights for each 'heuristic' 
    player_center_weight = 2.0
    weight_moves_difference_weight = 2.0 
    opp_corner_weight = 2.0
    opp_edge_weight = 2.0  

    ## incentives moving towards the center    
    # ... using euclidean distance         
    euclidean_distance = math.sqrt( (center_pos[0] - current_pos[0])**2 + (center_pos[1] - current_pos[1])**2 )
    max_distance = math.sqrt( (center_pos[0])**2 + (center_pos[1])**2 )    
    score += player_center_weight * (1.0 - euclidean_distance/max_distance)  

    ## incentives having more moves than the opponent 
    score += weight_moves_difference_weight * float(len(own_moves))/float(len(opp_moves)) 

    ## incentives pushing the opponent towards the edge
    def is_on_edge(pos):
        return pos[0] == 0 or pos[0] == game.width -1 or pos[1] == 0 or pos[1] == game.height - 1

    def is_in_corner(pos):
        corners = [(0,0), (game.width -1, 0), (game.width -1, game.height - 1), (0, game.height - 1)]
        for corner in corners:
            if pos[0] == corner[0] and pos[1] == corner[1]:
                return True  
                
    opp_on_egde_count = 0 
    opp_in_corner_count = 0 

    for opp_move in opp_moves:
        if is_in_corner(opp_move):
            opp_in_corner_count += 1
        elif is_on_edge(opp_move):
            opp_on_egde_count += 1 

    score += opp_edge_weight * opp_on_egde_count
    score += opp_corner_weight * opp_in_corner_count 

    return score 

@custom_score_timer
def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Aggressive offensive behaviour; add a weight to increase importance of moves that 
    'take-over' the opponents legal position 

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    if len(own_moves) != 0 and len(opp_moves) == 0:
        return float("inf")
    elif len(own_moves) == 0 and len(opp_moves) != 0:
        return float("-inf")
    elif len(own_moves) == 0 and len(opp_moves) == 0:
        return -10 

    player_current_pos = game.get_player_location(player)
    opp_current_pos = game.get_player_location(game.get_opponent(player))    

    max_distance = game.width + game.height 

    score = float(len(own_moves) - len(opp_moves)) 
    
    target_distance = 2 + 1 ## knight move 

    # using manhattan distance (distance from opponent)
    distance = abs(opp_current_pos[0] - player_current_pos[0]) + abs(opp_current_pos[1] - player_current_pos[1])
    distance_from_target = 1.0 - abs(distance-target_distance)
    score += distance_from_target * 2.0      

    return float(score)

@custom_score_timer
def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Similar to the AB_Improved evaluator presented in class; this evaluator 
    returns the squared ratio between the players remaining moves and opponents moves 

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    if len(own_moves) != 0 and len(opp_moves) == 0:
        return float("inf")
    elif len(own_moves) == 0 and len(opp_moves) != 0:
        return float("-inf")
    elif len(own_moves) == 0 and len(opp_moves) == 0:
        return -10 

    if len(own_moves) >= len(opp_moves):
        return (len(own_moves) / len(opp_moves)) ** 2.0 
    else:
        return -(len(opp_moves) / len(own_moves)) ** 2.0


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        """ 
        used to cache scores for game board states to avoid recomputing, key will be the hash of the board and 
        value a tuple (<score>, <[moves]>)
        """
        self.transporition_table = {} 
        """ used to store the time to run the assigned evaluation function """
        self.time_logging = []

    def get_board_state_key(self, board):
        """ return a board state key that will be used as a key for the transporition_table 
            when caching its score 
        """
        return board.hash() 

    def is_game_won(self, game_state):
        """ test if a player has won the game, called by the search methods to test whether to terminate the 
            search 
        """ 
        return (game_state.is_winner(game_state.active_player) or game_state.is_winner(game_state.inactive_player)) 


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1)

        _, move = self._minmax(game, depth)

        return move

    def _minmax(self, game_state, depth):
        """ min and max algorithm 
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = None
        best_move  = None

        best_moves = []

        legal_moves = game_state.get_legal_moves()      

        is_max = game_state.active_player == self

        for m in legal_moves:
            next_game_state = game_state.forecast_move(m)    
            next_game_state_key = self.get_board_state_key(next_game_state)        

            if depth == 1 or self.is_game_won(next_game_state):
                # do we have it cached?                 
                if  next_game_state_key in self.transporition_table:                    
                    score = self.transporition_table[next_game_state_key][0]
                else:                     
                    score = self.score(next_game_state, self)
                    # cache score and move 
                    #self.transporition_table[next_game_state_key] = (score, m)
            else:
                if  next_game_state_key in self.transporition_table:
                    score, move = self.transporition_table[next_game_state_key]
                else:
                    try:
                        score, move = self._minmax(next_game_state, depth-1)
                        self.transporition_table[next_game_state_key] = (score, move)
                    except SearchTimeout:
                        break 

            # first score or new best score? 
            if best_score is None or ((is_max and score > best_score) or (not is_max and score < best_score)):
                best_score = score 
                best_move = m 

                best_moves = [m]
            
            # if matched the current best score then store the move, we will randomly select 
            # which move to take if we have more than 1 
            elif best_score == score:
                best_moves.append(m)

        return best_score, random.choice(best_moves) if len(best_moves) > 0 else (-1,-1)    


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def __init__(self, search_depth=11, score_fn=custom_score, timeout=10.):
        """ Override the constructor to set the search depth 
        """
        IsolationPlayer.__init__(self, search_depth=search_depth, score_fn=score_fn, timeout=timeout)

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
            
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1)

        best_move = (-1, -1)     

        current_depth = 1 
        while True:
            try:
                best_move = self.alphabeta(game, current_depth)                 
            except SearchTimeout: 
                return best_move

            current_depth += 1
        
        return best_move   


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """        
        _, move = self._alphabeta(game, depth, alpha, beta) 
        return move 
              
    def _alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score  = None
        best_move  = (-1,-1)

        best_moves = [best_move]

        legal_moves = game.get_legal_moves()        

        is_max = game.active_player == self

        for m in legal_moves:
            next_game_state = game.forecast_move(m)            

            if depth == 1 or self.is_game_won(next_game_state):
                score = self.score(next_game_state, self)
            else:
                score, _ = self._alphabeta(next_game_state, depth-1, alpha, beta)

            if best_score is None or ((is_max and score > best_score) or (not is_max and score < best_score)):
                best_score = score 
                best_move = m 

                best_moves = [m]

                if is_max:                    
                    if best_score >= beta:
                        return best_score, random.choice(best_moves)
                    # update alpha for alpha-beta pruning 
                    alpha = max(alpha, best_score)                    
                else:                    
                    if best_score <= alpha:
                        return best_score, random.choice(best_moves)
                    # update beta for alpha-beta pruning 
                    beta = min(beta, best_score)                    

            elif best_score == score:
                best_moves.append(m)            

        return best_score, random.choice(best_moves)