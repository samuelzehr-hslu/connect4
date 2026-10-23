import sys
from output_console import *
from input_console import InputConsole
from game_state import GameState
from player_base import PlayerBase
from input_base import Keys


class PlayerConsole(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        self._output = OutputConsole() # use this class for console output
        self._input = InputConsole() # use this class for console input

    def play_turn(self) -> int:
        # YOUR CODE HERE
        # TODO: return desired column from user input (0..6) using
        # use self._input to read keys, use self._output to draw current token position
        row, col = -1, 0 #Header

        Ansi.gotoXY(1, self._output.STATUS_LINE_OFFSET)  # move cursor below the board
        print(f"Player {self._player.name}'s turn.")

        while True:
            self._output.draw_token(col, row, self._player)  # draw token at current position
            Ansi.reset()
            key = self._input.read_key()  # get key from user input
            self._output.draw_token(col, row, GameToken.EMPTY)  # clear old token

            if key == Keys.LEFT:    col = (col - 1) % 7  # move left (wrap around)
            if key == Keys.RIGHT:   col = (col + 1) % 7  # move right (wrap around)

            if key == Keys.ENTER:
                Ansi.gotoXY(1, self._output.STATUS_LINE_OFFSET + 2)
                return col  # return selected column

    def draw_board(self, board: list, state: GameState) -> None:
        # YOUR CODE HERE
        # TODO: draw grid with tokens using self._output
        self._output.draw_grid()

        for row, line in enumerate(board):
            for col, token in enumerate(line):
                self._output.draw_token(col, row, token)   # x = col, y = row
        Ansi.reset()


if __name__ == '__main__':
    # use the code below to test your implementation

    # creates an empty board
    board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
    
    # put some tokens at 'impossible' locations
    # note: board[row][column] 
    board[0][0] = GameToken.RED     # top left corner
    board[0][6] = GameToken.YELLOW  # top right corner
    board[4][3] = GameToken.RED     # 2nd but last row, middle position

    p = PlayerConsole(GameToken.YELLOW)  # this is the yellow player ('0')

    Ansi.clear_screen() # make sure terminal is 'clean'
    Ansi.reset()

    # draw board for the player yellow using console output (color text)
    # also tell the yellow player that it's yellow's turn
    p.draw_board(board, GameState.TURN_YELLOW)  
    # you should now see the board with the 3 'impossible' tokens
    
    # now let's ask yellow for their turn (using console input/ output)
    pos = p.play_turn()

    # first reset colors and move the cursor below the board
    Ansi.reset()
    Ansi.gotoXY(1, p._output.STATUS_LINE_OFFSET)  # move cursor below the board

    # print out the position for you to check if it's correct
    Ansi.clear_line()  # clear status line
    print(f"Position selected: {pos}")

    row = 5  # put yellow's token in to last row
    board[row][pos] = GameToken.YELLOW # put yellow's token on the board

    # now, after yellow has made their turn, redraw board for the *yellow*
    # player so they can see what has changed (using console input/ output)
    # also tell the *yellow* player that it's now reds's turn
    p.draw_board(board, GameState.TURN_RED)

    Ansi.gotoXY(1, p._output.STATUS_LINE_OFFSET + 1)
    # ...
