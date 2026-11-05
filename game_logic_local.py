from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_base import GameLogicBase


class GameLogicLocal(GameLogicBase):
    ROWS = 6
    COLS = 7

    def __init__(self):
        # YOUR CODE HERE
        super().__init__() # call constructor of the the base class
        self._board = [
            [' ',' ',' ',' ',' ',' ',' '], # row 0
            [' ',' ',' ',' ',' ',' ',' '], # row 1
            [' ',' ',' ',' ',' ',' ',' '], # row 2
            [' ',' ',' ',' ',' ',' ',' '], # row 3
            [' ',' ',' ',' ',' ',' ',' '], # row 4
            [' ',' ',' ',' ',' ',' ',' '], # row 5
            ]
        self._state = GameState.TURN_RED # red starts the game

    def get_state(self) -> GameState:
        # retruns a GameState enumeration constant
        # YOUR CODE HERE
        return self._state


    def drop_token(self, player: GameToken, column: int) -> DropState:
        # returns a DropToken (DROP_OK, COLUMN_INVALID, COLUMN_FULL, WRONG_PLAYER)

        # YOUR CODE HERE 
        if not ((player == GameToken.RED and self.get_state() == GameState.TURN_RED) or (player == GameToken.YELLOW and self.get_state() == GameState.TURN_YELLOW)):
            return DropState.WRONG_PLAYER

        elif(not 0 <= column < self.COLS):
            return DropState.COLUMN_INVALID

        elif(self._board[0][column] != GameToken.EMPTY):
            return DropState.COLUMN_FULL
        
        for row in range(self.ROWS):
            if self._board[5-row][column] == GameToken.EMPTY:
                self._board[5-row][column] = player
                break

        winner =  self._check_winner()
        if winner == GameToken.RED:
            self._state = GameState.WON_RED
        elif winner == GameToken.YELLOW:
            self._state = GameState.WON_YELLOW

        elif (self._board[0].count(GameToken.EMPTY) == 0):
            self._state = GameState.DRAW
            return DropState.DROP_OK
        
        else:
            self._state = GameState.TURN_YELLOW if self._state == GameState.TURN_RED else GameState.TURN_RED
        
        
        return DropState.DROP_OK 

    def _check_winner(self) -> GameToken:
            
            def is_four_in_a_row(symbol:str, row:int, col:int, d_row:int, d_col:int) -> bool:
                for i in range(4):
                    if not (0 <= row + i * d_row < self.ROWS and 0 <= col + i * d_col < self.COLS):
                        return False
                    if self._board[row + i * d_row][col + i * d_col] != symbol:
                        return False
                return True
    
            # Loop through each cell in the board
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    if self._board[row][col] in (GameToken.RED, GameToken.YELLOW):  # Only check cells with a player's symbol
                        symbol = self._board[row][col]
    
                        # Check horizontally, vertically, and both diagonals
                        if (is_four_in_a_row(symbol, row, col, 0, 1) or  # Horizontal
                            is_four_in_a_row(symbol, row, col, 1, 0) or  # Vertical
                            is_four_in_a_row(symbol, row, col, 1, 1) or  # Diagonal \
                            is_four_in_a_row(symbol, row, col, 1, -1)):  # Diagonal /
                            return symbol
            return GameToken.EMPTY