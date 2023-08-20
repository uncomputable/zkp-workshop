import math
import random
import unittest
import logging
from typing import List, Tuple, Iterator
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
        return "\n".join([repr(row) for row in self.rows])

    def __getitem__(self, row: int):
        return self.rows[row]

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
            row = random.randrange(dim_sq)
            col = random.randrange(dim_sq)
            rows[row][col] = value

        return Board(rows)

    def verify(self) -> bool:
        """
        Verify that the board is a valid Sudoku solution.

        :return: board is valid solution
        """
        for columns in self.rows:
            if not self.verify_area(columns):
                return False

        for col in range(self.dim_sq):
            rows = [self.rows[row][col] for row in range(self.dim_sq)]
            if not self.verify_area(rows):
                return False

        for box_row in range(0, self.dim_sq, self.dim):
            for box_col in range(0, self.dim_sq, self.dim):
                box = [self.rows[box_row + row_offset][box_col + col_offset]
                       for row_offset in range(self.dim) for col_offset in range(self.dim)]
                if not self.verify_area(box):
                    return False

        return True

    def verify_area(self, area: List[int]) -> bool:
        """
        Verify that the area consists of unique, nonzero values.

        :param area: row, column or box
        :return: area is valid
        """
        return 0 not in area and len(set(area)) == self.dim_sq

    def verify_shuffling(self, shuffled_values: Iterator[int]) -> bool:
        """
        Verify that this board is consistent with the other board.

        Consistency means that there is a one-to-one mapping from the values of this board to values of the other board.
        If there is a mapping, then this board was obtained from the other one by shuffling values.
        If there is an inconsistency, then it is impossible to obtain this board from the other one.

        :param shuffled_values: iterator over nonzero values of other board
        :return: this board is consistent with other board
        """
        mapping = {}

        for row, columns in enumerate(self.rows):
            for col, original_value in enumerate(columns):
                if original_value > 0:
                    shuffled_value = next(shuffled_values)

                    if original_value in mapping:
                        # Mapped same value to different values
                        if mapping[original_value] != shuffled_value:
                            logging.info("Mapped same value to different values")
                            return False
                    else:
                        mapping[original_value] = shuffled_value

        # Mapped different values to the same value
        if len(mapping.values()) != len(set(mapping.values())):
            logging.info("Mapped different values to same value")
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
        for box_row in range(0, self.dim_sq, self.dim):
            for box_col in range(0, self.dim_sq, self.dim):
                for value in range(1, self.dim_sq + 1):
                    matrix.add_column(
                        "b{}:{}#{}".format(box_row, box_col, value),
                        {(box_row + row_offset, box_col + col_offset, value) for row_offset in range(self.dim) for col_offset in range(self.dim)}
                    )

        # Reduce matrix using preset values
        for row, columns in enumerate(self.rows):
            for col, value in enumerate(columns):
                if value > 0:
                    matrix.cover_column((row, col, value))

        return matrix

    def solve(self) -> "Board":
        """
        Fill in the empty cells on the board to form a Sudoku solution.

        :return: Sudoku solution
        """
        matrix = self.to_matrix()
        logging.info(f"Solving {len(matrix.rows)} elements and {len(matrix.cols)} constraints")
        assignment = next(matrix.algorithm_x([]))
        rows = [row.copy() for row in self.rows]

        for assigned_row in assignment:
            row, col, value = assigned_row
            rows[row][col] = value

        return Board(rows)

    def remove_values(self, n_remove: int) -> "Board":
        """
        Remove cells from the board.

        :param n_remove: number of cells to be removed
        :return: copy of original board with cells removed
        """
        rows = [row.copy() for row in self.rows]

        cells = random.sample([(row, col) for row in range(self.dim_sq) for col in range(self.dim_sq)], n_remove)
        for cell in cells:
            rows[cell[0]][cell[1]] = 0

        return Board(rows)

    def to_puzzle(self) -> "Board":
        """
        Convert a complete Sudoku solution into a partial solution by removing values.

        :return: partial solution (copy)
        """
        n_clues = math.ceil(self.dim_sq ** 2 * 0.2)
        logging.info(f"Sudoku with {n_clues} clues")
        return self.remove_values(self.dim_sq ** 2 - n_clues)

    def falsify_row(self):
        """
        Create a duplicate value in a random row.
        """
        row = random.randrange(self.dim_sq)
        logging.debug(f"Falsified row {row}")
        col0, col1 = random.sample(range(self.dim_sq), 2)
        assert col0 != col1
        self.rows[row][col0] = self.rows[row][col1]

    def falsify_column(self):
        """
        Create a duplicate value in a random column.
        """
        col = random.randrange(self.dim_sq)
        logging.debug(f"Falsified column {col}")
        row0, row1 = random.sample(range(self.dim_sq), 2)
        assert row0 != row1
        self.rows[row0][col] = self.rows[row1][col]

    def falsify_box(self):
        """
        Create a duplicate value in a random box.
        """
        box_row = random.randrange(self.dim) * self.dim
        box_col = random.randrange(self.dim) * self.dim
        logging.debug(f"Falsified box {box_row}:{box_col}")
        box = [(box_row + row_offset, box_col + col_offset) for row_offset in range(self.dim) for col_offset in range(self.dim)]

        cell0, cell1 = random.sample(box, 2)
        assert cell0 != cell1
        self.rows[cell0[0]][cell0[1]] = self.rows[cell1[0]][cell1[1]]

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
