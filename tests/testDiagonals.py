import unittest
from core.board import Board

class TestBoardDiagonals(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 7)
        self.board.add_to_square(3, 0, "r")
        self.board.add_to_square(4, 1, "r")
        self.board.add_to_square(5, 2, "r")
        self.board.add_to_square(4, 3, "y")
        self.board.add_to_square(3, 4, "y")

    def test_diagonal_segment_down_right_valid(self):
        segment = self.board.get_diagonal_segment(3, 0, 3, up=False)
        self.assertEqual(segment, ['r', 'r', 'r'])

    def test_diagonal_segment_down_right_none(self):
        segment = self.board.get_diagonal_segment(3, 0, 4, up=False)
        self.assertIsNone(segment)

    def test_diagonal_line_down_right_valid(self):
        line = self.board.get_diagonal_line_down(3, 0, 3, "right")
        self.assertTrue(line)

    def test_diagonal_line_down_right_empty(self):
        line = self.board.get_diagonal_line_down(3, 0, 4, "right")
        self.assertEqual(line, [])

    def test_diagonal_segment_down_left_valid(self):
        segment = self.board.get_diagonal_segment(3, 4, 3, up=False, right=False)
        self.assertEqual(segment, ['y', 'y', 'r'])

    def test_diagonal_segment_down_left_none(self):
        segment = self.board.get_diagonal_segment(3, 4, 4, up=False, right=False)
        self.assertIsNone(segment)

    def test_diagonal_line_down_left_valid(self):
        line = self.board.get_diagonal_line_down(3, 4, 3, "left")
        self.assertTrue(line)

    def test_diagonal_line_down_left_empty(self):
        line = self.board.get_diagonal_line_down(3, 4, 4, "left")
        self.assertEqual(line, [])

    def test_diagonal_segment_up_right_valid(self):
        segment = self.board.get_diagonal_segment(3, 0, 4)
        self.assertEqual(segment, ['r', 0, 0, 0])

    def test_diagonal_segment_up_right_none(self):
        segment = self.board.get_diagonal_segment(3, 0, 5)
        self.assertIsNone(segment)

    def test_diagonal_line_up_right_valid(self):
        line = self.board.get_diagonal_line_up(3, 0, 4, "right")
        self.assertTrue(line)

    def test_diagonal_line_up_right_empty(self):
        line = self.board.get_diagonal_line_up(3, 0, 5, "right")
        self.assertEqual(line, [])

    def test_diagonal_segment_up_left_valid(self):
        segment = self.board.get_diagonal_segment(3, 4, 4, up=True, right=False)
        self.assertEqual(segment, ['y', 0, 0, 0])

    def test_diagonal_segment_up_left_none(self):
        segment = self.board.get_diagonal_segment(3, 4, 5, up=True, right=False)
        self.assertIsNone(segment)

    def test_diagonal_line_up_left_valid(self):
        line = self.board.get_diagonal_line_up(3, 4, 4, "left")
        self.assertTrue(line)

    def test_diagonal_line_up_left_empty(self):
        line = self.board.get_diagonal_line_up(3, 4, 5, "left")
        self.assertEqual(line, [])

if __name__ == "__main__":
    unittest.main()
