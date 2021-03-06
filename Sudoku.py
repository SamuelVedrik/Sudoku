import tkinter as tk
from typing import List
import random
import copy

TEMPLATE_SUDOKU = "template.txt"
PUZZLE_SIZE = 30

class Sudoku:
    """
    A completed sudoku board.

    The board is represent`ed by a nested list. Each nested list inside
    the main list represents a 3x3 cell, formatted as such:

    0 1 2
    3 4 5
    6 7 8

    Where the numbers above correspond to the index of the nested list.

    The arrangement of each of the 3x3 cell is the same as above.

    """
    _board: List[List[int]]

    def __init__(self):
        self._board = None
        self.generate_board()

    def generate_board(self) -> None:
        """
        Generates a board based on the template. This method must be called
        during initialization.

        :return: None
        """
        result = []
        with open(TEMPLATE_SUDOKU, 'r') as template:
            lines = template.readlines()
            for line in lines:
                # Creates a list of individual digits from the line
                cells = [int(char) for char in str(line.strip())]
                result.append(cells)
        self._board = result

    def render(self, drawer):
        """
        Draws the sudoku board.
        :param drawer: SudokuDrawer
        :return: None
        """
        drawer.draw_board(self._board)

    def shuffle(self):
        """
        Randomly shuffles the board to create a new, unique sudoku board
        that is still correct.

        This function performs 100 transformations.
        :return: None
        """
        functions = [self._shuffle_value_randomly,
                     self._shuffle_big_randomly,
                     self._shuffle_small_randomly]

        for _ in range(100):
            function_choice = functions[random.randint(0, 2)]
            function_choice()

    def generate_puzzle(self):
        """
        Generates a random puzzle based on the current board with
        PUZZLE_SIZE numbers left.
        :return: List[List[int]], representing the board. 0 represents
        an empty cell.
        """

        result = copy.deepcopy(self._board)
        # First, goes through each cell to make sure all cells have something
        # removed.
        remaining = self._initial_removal(81 - PUZZLE_SIZE, result)

        # Then, picks random cells and removes one until there are no more
        # remainders.
        self._completer_removal(remaining, result)

        return result

    def _completer_removal(self, remaining, result):

        while remaining > 0:
            random_cell = random.randint(0, 8)
            while result[random_cell].count(0) > 7:
                random_cell = random.randint(0, 8)

            replaced = random.randint(0, 8)
            while result[random_cell][replaced] == 0:
                replaced = random.randint(0, 8)

            result[random_cell][replaced] = 0

            remaining -= 1

    def _initial_removal(self, remaining, result):
        order = [i for i in range(9)]
        random.shuffle(order)
        for i in order:
            num_replaced = int(random.normalvariate(5, 1))
            replaced_index = random.sample(range(9), num_replaced)
            for j in replaced_index:
                result[i][j] = 0

            remaining -= num_replaced
        return remaining

    #   ==== TRANSFORMATION FUNCTIONS ====
    def _shuffle_big_randomly(self):

        choice = random.randint(0,1)
        swap_a, swap_b = random.randint(0,2), random.randint(0,2)
        if choice == 0:
            self._shuffle_big_column(swap_a, swap_b)
        else:
            self._shuffle_big_row(swap_a, swap_b)

    def _shuffle_small_randomly(self):
        def generate_tuple():
            first = random.randint(0, 8)
            second = random.randint(((first//3) * 3), ((first//3) * 3) + 2)
            while second == first:
                second = random.randint(((first // 3) * 3),
                                        ((first // 3) * 3) + 2)
            return first, second

        choice = random.randint(0,1)
        swap_a, swap_b = generate_tuple()
        if choice == 0:
            self._shuffle_small_column(swap_a, swap_b)
        else:
            self._shuffle_small_row(swap_a, swap_b)

    def _shuffle_big_row(self, row_a, row_b):
        """
        Prerequisite: 0 <= row_a, row_b, <= 2
        """

        self._board[row_a * 3:row_a * 3 + 3], self._board[row_b * 3:row_b * 3 + 3] = \
            self._board[row_b * 3:row_b * 3 + 3], self._board[row_a * 3:row_a * 3 + 3]


    def _shuffle_small_row(self, row_a, row_b):
        """
        Prerequisite: 0 <= row_a, row_b, <= 9
        max(row_a, row_b) - min(row_a, row_b) <= 2
        """

        cells = range((row_a//3) * 3, ((row_a//3) * 3) + 3)
        slice_a = (row_a%3 * 3, row_a%3 * 3 + 3)
        slice_b = (row_b%3 * 3, row_b%3 *3 + 3)
        for i in cells:

            self._board[i][slice_a[0]:slice_a[1]], self._board[i][slice_b[0]:slice_b[1]] \
                = self._board[i][slice_b[0]:slice_b[1]], self._board[i][slice_a[0]:slice_a[1]]


    def _shuffle_big_column(self, col_a, col_b):
        """
        Prerequisite: 0 <= col_a, col_b, <= 2
        """

        # The +7 so col_a + 6 is in range.
        for i, j in zip(range(col_a, col_a + 7, 3), range(col_b,col_b + 7, 3)):
            self._board[i] , self._board[j] = self._board[j], self._board[i]


    def _shuffle_small_column(self, col_a, col_b):
        """
        Prerequisite: 0 <= col_a, col_b, <= 9
        max(col_a, col_b) - min(col_a, col_b) <= 2
        """

        cells = range(col_a//3, col_a//3 + 7, 3)
        for i in cells:
            for j, k in zip(range(col_a%3, col_a%3 + 7, 3), range(col_b%3, col_b%3 + 7, 3)):
                self._board[i][j], self._board[i][k] = self._board[i][k], self._board[i][j]

    def _shuffle_value_randomly(self):
        first = random.randint(1, 9)
        second = random.randint(1, 9)
        while second == first:
            second = random.randint(1, 9)
        self._shuffle_value(first, second)

    def _shuffle_value(self, val_a, val_b):
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] == val_a:
                    self._board[i][j] = val_b
                elif self._board[i][j] == val_b:
                    self._board[i][j] = val_a


class SudokuDrawer:
    """
    A drawer for Sudoku using Tkinter.
    """

    def __init__(self, root):
        self.root = root

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
    mySudoku.shuffle()
    puzzle = mySudoku.generate_puzzle()

    root = tk.Tk()
    drawer = SudokuDrawer(root)

    mySudoku.render(drawer)
    drawer.draw_board(puzzle)

    root.mainloop()

