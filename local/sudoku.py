import math
import random
import unittest
from typing import List, Tuple
from local.exact_cover import Matrix


class Board:
    """
    Sudoku board.
    """
    rows: List[List[int]]
    """
    Rows of the board.

    Each row is a list of values for each column.
    """
    dim: int
    """
    Number of cells alongside a box.
    """
    dim_sq: int
    """
    Number of cells alongside the board.

    Equal to self.dim ** 2.
    """

    def __init__(self, rows: List[List[int]]):
        self.rows = rows
        self.dim_sq = len(self.rows)
        self.dim = math.isqrt(self.dim_sq)

    def __repr__(self) -> str:
        return repr(self.rows)

    @classmethod
    def blank(cls, dim: int) -> "Board":
        """
        Return an empty board.

        :param dim: number of cells alongside a box; the board is dim**2 cells wide
        :return: blank board
        """
        dim_sq = dim ** 2
        return Board([[0 for _ in range(dim_sq)] for _ in range(dim_sq)])

    @classmethod
    def random(cls, dim: int) -> "Board":
        """
        Return an empty board with some random presets filled in.

        :param dim: number of cells alongside a box; the board is dim**2 cells wide
        :return: random board
        """
        dim_sq = dim ** 2
        rows = [[0 for _ in range(dim_sq)] for _ in range(dim_sq)]

        for value in range(1, dim + 1):
            col = random.randrange(0, dim_sq)
            row = random.randrange(0, dim_sq)
            rows[col][row] = value

        return Board(rows)

    def verify(self) -> bool:
        """
        Verify that the board is a valid Sudoku solution.

        :return: board is valid solution
        """
        # Each row contains all values
        for row in self.rows:
            if len(set(row)) != self.dim_sq:
                return False

        # Each column contains all values
        for col in range(self.dim_sq):
            column = {self.rows[row][col] for row in range(self.dim_sq)}
            if len(column) != self.dim_sq:
                return False

        # Each box contains all values
        for box_col in range(0, self.dim_sq, self.dim):
            for box_row in range(0, self.dim_sq, self.dim):
                box = {self.rows[box_col + col_offset][box_row + row_offset] for col_offset in range(self.dim) for row_offset in range(self.dim)}
                if len(box) != self.dim_sq:
                    return False

        return True

    def to_matrix(self) -> Matrix[Tuple[int, int, int], str]:
        """
        Convert the board into an instance of the exact cover problem.

        Possible value assignments for each cell are elements / rows.
        Constraints on the value assignments are subsets / columns.

        https://en.wikipedia.org/w/index.php?title=Exact_cover&oldid=1134545756#Sudoku

        :return: exact cover instance
        """
        dim = math.isqrt(self.dim_sq)
        matrix = Matrix()

        # Each cell contains exactly one value
        for row in range(self.dim_sq):
            for col in range(self.dim_sq):
                matrix.add_column("r{}c{}".format(row, col), {(row, col, value) for value in range(1, self.dim_sq + 1)})

        # Each row contains all values
        for row in range(self.dim_sq):
            for value in range(1, self.dim_sq + 1):
                matrix.add_column("r{}#{}".format(row, value), {(row, col, value) for col in range(self.dim_sq)})

        # Each column contains all values
        for col in range(self.dim_sq):
            for value in range(1, self.dim_sq + 1):
                matrix.add_column("c{}#{}".format(col, value), {(row, col, value) for row in range(self.dim_sq)})

        # Each box contains all values
        for box_row in range(0, self.dim_sq, dim):
            for box_col in range(0, self.dim_sq, dim):
                for value in range(1, self.dim_sq + 1):
                    matrix.add_column(
                        "b{}:{}#{}".format(box_row, box_col, value),
                        {(box_row + row_offset, box_col + col_offset, value) for row_offset in range(dim) for col_offset in range(dim)}
                    )

        # Reduce matrix using preset values
        for col, columns in enumerate(self.rows):
            for row, value in enumerate(columns):
                if value > 0:
                    matrix.cover_column((row, col, value))

        return matrix

    def solve(self) -> "Board":
        """
        Fill in the empty cells on the board to form a Sudoku solution.

        :return: Sudoku solution
        """
        matrix = self.to_matrix()
        assignment = next(matrix.algorithm_x([]))
        rows = [row.copy() for row in self.rows]

        for row in assignment:
            x, y, value = row
            rows[y][x] = value

        return Board(rows)

    def remove_values(self, n_removed: int) -> "Board":
        """
        Remove cells from the board.

        :param n_removed: number of cells to be removed
        :return: copy of original board with cells removed
        """
        rows = [row.copy() for row in self.rows]

        for _ in range(n_removed):
            col, row = random.randrange(self.dim_sq), random.randrange(self.dim_sq)
            while rows[col][row] == 0:
                col, row = random.randrange(self.dim_sq), random.randrange(self.dim_sq)
            rows[col][row] = 0

        return Board(rows)

    def falsify_row(self):
        """
        Create a duplicate value in a random row.
        """
        col = random.choice(range(self.dim_sq))
        print(f"Falsified row {col}")
        row0, row1 = random.sample(range(self.dim_sq), 2)
        assert row0 != row1
        self.rows[col][row0] = self.rows[col][row1]

    def falsify_column(self):
        """
        Create a duplicate value in a random column.
        """
        row = random.choice(range(self.dim_sq))
        print(f"Falsified column {row}")
        col0, col1 = random.sample(range(self.dim_sq), 2)
        assert col0 != col1
        self.rows[col0][row] = self.rows[col1][row]

    def falsify_box(self):
        """
        Create a duplicate value in a random box.
        """
        box_col = random.randrange(self.dim) * self.dim
        box_row = random.randrange(self.dim) * self.dim
        print(f"Falsified box {box_col}:{box_row}")
        square = [(box_col + col_offset, box_row + row_offset) for col_offset in range(self.dim) for row_offset in range(self.dim)]

        cell0, cell1 = random.sample(square, 2)
        assert cell0 != cell1
        self.rows[cell0[1]][cell0[0]] = self.rows[cell1[1]][cell1[0]]

    def falsify(self, n_errors: int):
        """
        Randomly create duplicate values to falsify a Sudoku solution.

        :param n_errors: number of errors
        """
        for _ in range(n_errors):
            selection = random.randrange(3)
            if selection == 0:
                self.falsify_row()
            elif selection == 1:
                self.falsify_column()
            else:
                self.falsify_box()


class TestBoard(unittest.TestCase):
    def test_solve_random(self):
        board = Board.random(3)
        solved = board.solve()
        assert solved.verify()

    def test_solve_hard(self):
        hard = Board([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 8, 5],
            [0, 0, 1, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 7, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 7, 3],
            [0, 0, 2, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 9]
        ])
        """
        A Sudoku designed to work against the brute force algorithm.

        https://www.flickr.com/photos/npcomplete/2361922699
        """
        solved = hard.solve()
        assert solved.verify()

    def test_falsify_verify(self):
        board = Board.random(3)
        solved = board.solve()
        solved.falsify(1)
        assert not solved.verify()

    def test_repeated_falsify(self):
        board = Board.random(3)
        solved = board.solve()
        solved.falsify(40)
