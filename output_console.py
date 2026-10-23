from ansi import Ansi
from game_token import GameToken
from output_base import OutputBase


class OutputConsole(OutputBase):
    VERTICAL_OFFSET = 2         # this is the row where the board starts
    STATUS_LINE_OFFSET = 15     # can print here w/o distroying board visuals 

    def __init__(self):
        Ansi.clear_screen()
        Ansi.reset()

    def draw_grid(self) -> None:
        # YOUR CODE HERE (replace the code below with your own code)
        Ansi.reset()
        Ansi.gotoXY(1,OutputConsole.VERTICAL_OFFSET)
        print("┌────┬────┬────┬────┬────┬────┬────┐")
        print("│    │    │    │    │    │    │    │")
        print("├────┼────┼────┼────┼────┼────┼────┤")
        print("│    │    │    │    │    │    │    │")
        print("├────┼────┼────┼────┼────┼────┼────┤")
        print("│    │    │    │    │    │    │    │")
        print("├────┼────┼────┼────┼────┼────┼────┤")
        print("│    │    │    │    │    │    │    │")
        print("├────┼────┼────┼────┼────┼────┼────┤")
        print("│    │    │    │    │    │    │    │")
        print("├────┼────┼────┼────┼────┼────┼────┤")
        print("│    │    │    │    │    │    │    │")
        print("└────┴────┴────┴────┴────┴────┴────┘")

    def draw_token(self, x: int, y: int, token: GameToken = GameToken.EMPTY) -> None:
        # YOUR CODE HERE (replace the code below with your own code)
        Ansi.gotoXY(3 + 5*x, OutputConsole.VERTICAL_OFFSET + 1 + 2*y)
        if token == GameToken.EMPTY:
            print("  ")  
        if token == GameToken.RED:
            Ansi.set_foreground(1, True)
            print("██")
        if token == GameToken.YELLOW:
            Ansi.set_foreground(3, True)
            print("██")
        Ansi.reset()

    # if you need more output (e.g., a status line), add a method here
    # YOUR CODE HERE
"""
┌ ┐
└ ┘
├ ┤
┼ ─ │
┬ ┴ 
██ 
https://de.wikipedia.org/wiki/Unicodeblock_Rahmenzeichnung
"""


if __name__ == '__main__':
    # use the code below to test your implementation

    # for testing only
    from input_console import InputConsole
    from input_base import Keys

    oc = OutputConsole()
    row, col = 3, 3

    oc.draw_grid()                          # you should see only the grid now
    oc.draw_token(col, row, GameToken.RED)  # now there is a red token at 3,3
    Ansi.reset()
    Ansi.gotoXY(1,OutputConsole.STATUS_LINE_OFFSET+1); # one below status line
    print("""After implementing OutputConsole, you should be able to move a red 
token up, down, left, and right through the board. Press ESC to quit.""")

    # this is an extended test
    input = InputConsole()
    while True:

        key = input.read_key()

        Ansi.gotoXY(1,OutputConsole.STATUS_LINE_OFFSET); # move to status line
        Ansi.clear_line() # clear status line
        Ansi.reset()
        print(f"Last key pressed: {key}, Type: {type(key)}") # output on status line
    
        oc.draw_token(col, row, GameToken.EMPTY)  # clear old token

        if key == Keys.RIGHT: col = (col + 1) % 7  # 7 columns in connect 4
        if key == Keys.LEFT:  col = (col - 1) % 7
        if key == Keys.DOWN:  row = (row + 1) % 6  # 6 rows in connect 4
        if key == Keys.UP:    row = (row - 1) % 6

        if key == Keys.ENTER: row, col = 0, 0  # jump to top left position
        
        if (key == Keys.ESC):  # Abort with ESC
            Ansi.gotoXY(1,OutputConsole.STATUS_LINE_OFFSET+2); # move to status line
            Ansi.clear_line() # clear status line
            print("Aborted on use request.")
            break
        oc.draw_token(col, row, GameToken.RED)  # draw new token
