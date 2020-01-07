import tkinter as tk
from typing import List, Dict

TEMPLATE_SUDOKU = "template.txt"

class Sudoku:
    """
    The board is formatted as such:
    Each nested list represents a 3x3 cell. Considering the index of the list:

    0 1 2
    3 4 5
    6 7 8

    """
    def __init__(self):
        self.board = None
        self.drawer = SudokuDrawer()
        self.generate_board()

    def generate_board(self) -> None:
        result = []
        with open(TEMPLATE_SUDOKU, 'r') as template:
            lines = template.readlines()
            for line in lines:
                # Creates a list of individual digits from the line
                cells = [int(char) for char in str(line.strip())]
                result.append(cells)
        self.board = result

    def render(self):
        self.drawer.draw_board(self.board)
        self.drawer.root.mainloop()

    def shuffle(self):
        pass

    def _shuffle_cell_row(self, row_a, row_b):
        """
        Prerequisite: 0 <= row_a, row_b, <= 2
        """

        self.board[row_a*3:row_a*3 + 3], self.board[row_b*3:row_b*3 + 3] = \
            self.board[row_b*3:row_b*3 + 3], self.board[row_a*3:row_a*3 + 3]

    def _shuffle_row(self, row_a, row_b):
        """
        Prerequisite: 0 <= row_a, row_b, <= 9
        max(row_a, row_b) - min(row_a, row_b) <= 2
        """


        cells = range((row_a//3) * 3, ((row_a//3) * 3) + 3)
        for i in cells:
            self.board[i][row_a*3:(row_a*3) + 3], self.board[i][row_b*3:(row_b*3) + 3] \
                = self.board[i][row_b*3:(row_b*3) + 3], self.board[i][row_a*3:(row_a*3) + 3]

    def _shuffle_cell_column(self, col_a, col_b):
        """
        Prerequisite: 0 <= col_a, col_b, <= 2
        """

        # The +7 so col_a + 6 is in range.
        for i, j in zip(range(col_a, col_a + 7, 3), range(col_b,col_b + 7, 3)):
            self.board[i] , self.board[j] = self.board[j], self.board[i]

    def _shuffle_column(self, col_a, col_b):
        """
        Prerequisite: 0 <= col_a, col_b, <= 9
        max(col_a, col_b) - min(col_a, col_b) <= 2
        """

        cells = range(col_a//3, col_a//3 + 7, 3)
        for i in cells:
            for j, k in zip(range(col_a%3, col_a%3 + 7, 3), range(col_b%3, col_b%3 + 7, 3)):
                self.board[i][j], self.board[i][k] = self.board[i][k], self.board[i][j]

class SudokuDrawer:

    def __init__(self):
        self.root = tk.Tk()

    def draw_board(self, board: List[List]):
        container = tk.Frame(self.root, relief=tk.SOLID, borderwidth=1)
        for big_cell, j in zip(board, range(len(board))):
            cell_container = tk.Frame(container, relief=tk.SOLID, borderwidth=1)
            for i in range(len(big_cell)):
                cell = tk.Label(cell_container, text=big_cell[i]) if big_cell[i] != 0 else tk.Label(cell_container, text=" ")
                cell.config(relief=tk.SOLID, font = ("Arial", 13), borderwidth=1)
                cell.grid(row=i//3, column=i%3, ipadx=4, ipady=3)
            cell_container.grid(row=j//3, column=j%3)

        container.pack()


if __name__ == "__main__":
    mySudoku = Sudoku()
    # mySudoku._shuffle_cell_row(0, 2)
    # mySudoku._shuffle_row(0,2)
    # mySudoku._shuffle_cell_column(0,2)
    mySudoku._shuffle_column(7,8)
    mySudoku.render()
