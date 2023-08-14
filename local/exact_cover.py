from collections import defaultdict
from typing import Set, List, Dict, TypeVar, Iterator, Generic
import unittest
import bisect

Row = TypeVar("Row")
"""
Row label.
"""
Col = TypeVar("Col")
"""
Column label.
"""


class Matrix(Generic[Row, Col]):
    """
    Instance of the exact cover problem:

    Given a set X and a collection S of subsets of X,
    find a subcollection S* of S such that each element from X occurs exactly once in (a subset in) S*.
    We call S* a partition of X.

    This can be represented as a matrix.
    Each subset is a column. Each element is a row.
    The cell (element, subset) is 1 if element is contained in subset, and 0 otherwise.
    A solution is a collection of rows where each column is 1 in exactly one row.

    https://en.wikipedia.org/wiki/Exact_cover
    """
    rows: Dict[Row, List[Col]]
    """
    Maps each row label to a list of labels of columns where this row is member.

    This holds redundant data that we use to (un)cover columns.
    """
    cols: Dict[Col, Set[Row]]
    """
    Maps each column label to the set of labels of rows that are member.

    This is what we use most of the time.
    """

    def __init__(self):
        self.rows = defaultdict(list)
        self.cols = defaultdict(set)

    def __repr__(self) -> str:
        return repr(self.rows)

    def __eq__(self, other: "Matrix") -> bool:
        return self.rows == other.rows and self.cols == other.cols

    def is_empty(self) -> bool:
        """
        Return whether the matrix is empty.
        """
        return len(self.cols) == 0

    def add_row(self, row: Row, cols: List[Col]):
        """
        Add a row to the matrix.

        :param row: row label
        :param cols: list of labels of columns where this row is member
        """
        self.rows[row] = cols
        for col in cols:
            self.cols[col].add(row)

    def add_column(self, col: Col, rows: Set[Row]):
        """
        Add a column to the matrix.

        :param col: column label
        :param rows: set of labels of rows that are member
        """
        self.cols[col] = rows
        for row in rows:
            bisect.insort(self.rows[row], col)

    def choose_column(self) -> Col:
        """
        Choose the next column to work on.

        This is a deterministic choice, so we return exactly one column.

        :return: next column
        """
        return min(self.cols, key=lambda i: len(self.cols[i]))

    def choose_row(self, c: Col) -> Iterator[Row]:
        """
        Choose the next row to work on.

        Because this is a nondeterministic choice, we have to iterate over all possible rows.

        :param c: chosen column
        :return: iterator of next rows
        """
        for r in list(self.cols[c]):
            yield r

    def cover_column(self, r: Row) -> List[Set[Row]]:
        """
        Remove row r from the matrix.

        :param r: chosen row
        :return: list of removed columns
        """
        removed_cols = []

        # Delete all columns j inside row r (where r[j] == 1)
        # Because row r already covers them
        for j in self.rows[r]:
            # Delete all rows i inside column j (where i[j] == 1)
            # Because row i would cover the same column as row r
            # We keep self.rows constant and remove i from self.cols instead
            for i in self.cols[j]:
                for col in self.rows[i]:
                    if col != j:  # Cannot change self.cols[j] while iterating over it
                        self.cols[col].remove(i)

            removed_cols.append(self.cols.pop(j))

        return removed_cols

    def uncover_column(self, removed_cols: List[Set[Row]]):
        """
        Undo removing a particular row from the matrix.

        Because all the required information is contained in the removed columns,
        the removed row is not passed to this function.

        :param removed_cols: list of removed columns
        """
        # Restore each removed column j
        for j in removed_cols:
            # Restore each row i inside column j (where i[j] == 1)
            for i in j:
                # Add row i to each column, including j
                for col in self.rows[i]:
                    self.cols[col].add(i)

    def algorithm_x(self, selected_rows: List[Row] = None) -> Iterator[List[Row]]:
        """
        Solve the exact cover problem.

        Uses Donald Knuth's Algorithm X.

        https://arxiv.org/pdf/cs/0011047.pdf

        The idea of using dictionaries to efficiently represent rows and columns is by Ali Assaf.
        This is much easier than implementing Dancing Links.

        https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

        :param selected_rows:
        :return: iterator over solutions
        """
        if self.is_empty():
            yield selected_rows

        c = self.choose_column()
        for r in self.choose_row(c):
            selected_rows.append(r)
            removed_cols = self.cover_column(r)

            for solution in self.algorithm_x(selected_rows):
                yield solution

            self.uncover_column(removed_cols)
            selected_rows.pop()


class TestMatrix(unittest.TestCase):
    def get_matrix(self):
        matrix = Matrix()
        matrix.add_row("A", [1, 4, 7])
        matrix.add_row("B", [1, 4])
        matrix.add_row("C", [4, 5, 7])
        matrix.add_row("D", [3, 5, 6])
        matrix.add_row("E", [2, 3, 6, 7])
        matrix.add_row("F", [2, 7])
        return matrix

    def test_cover_uncover(self):
        matrix = self.get_matrix()

        for row in matrix.rows:
            cols = matrix.cover_column(row)
            matrix.uncover_column(cols)
            self.assertEqual(self.get_matrix(), matrix)

    def test_cover_until_empty(self):
        matrix = self.get_matrix()
        for row in matrix.rows:
            matrix.cover_column(row)
        self.assertTrue(matrix.is_empty())

    def test_cover_b(self):
        expected = defaultdict(set)
        expected[2] = {"E", "F"}
        expected[3] = {"D", "E"}
        expected[5] = {"D"}
        expected[6] = {"D", "E"}
        expected[7] = {"E", "F"}

        matrix = self.get_matrix()
        matrix.cover_column("B")
        self.assertEqual(expected, matrix.cols)

    def test_algorithm_x(self):
        matrix = self.get_matrix()
        solution = next(matrix.algorithm_x([]))
        self.assertEqual(["B", "D", "F"], solution)
