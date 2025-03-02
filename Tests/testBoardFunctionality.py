import unittest
from core.board import Board, WinChecker


class TestBoardFunctionality(unittest.TestCase):
    
    def setUp(self):
        """Initialize boards for testing."""
        self.board_3x3 = Board(3, 3)
        self.board_6x7 = Board(6, 7)

    def test_board_basic_operations(self):
        """Test basic board operations like adding to squares and retrieving structures."""
        self.board_3x3.add_to_square(0, 0, "o")
        self.board_3x3.add_to_square(1, 2, "x")
        self.board_3x3.add_to_square(2, 0, "o")
        
        self.assertEqual(self.board_3x3.get_rows(), [['o', 0, 0], [0, 0, 'x'], ['o', 0, 0]])
        self.assertEqual(self.board_3x3.get_columns(), [['o', 0, 'o'], [0, 0, 0], [0, 'x', 0]])
        self.assertEqual(self.board_3x3.get_rows()[2][0], "o")
        self.assertEqual(self.board_3x3.get_columns()[2][1], "x")
        
    def test_diagonal_extraction(self):
        """Ensure diagonal extraction functions work correctly."""
        self.board_3x3.add_to_square(0, 0, "o")
        self.board_3x3.add_to_square(1, 2, "x")
        self.board_3x3.add_to_square(2, 0, "o")
        
        self.assertEqual(self.board_3x3.get_diagonals(3, "right"), [['o', 0, 0]])
        self.assertEqual(self.board_3x3.get_diagonals(3, "left"), [[0, 0, 'o']])
        self.assertEqual(self.board_3x3.get_diagonals(2, "right"), [['o', 0], [0, 'x'], [0, 0], [0, 0]])
        self.assertEqual(self.board_3x3.get_diagonals(1, "left"), [[0], [0], ['o'], ['x'], [0], [0], [0], [0], ['o']])

    def test_horizontal_win_connect_4_of_7(self):
        """Test if horizontal win condition is detected."""
        for col in range(7):  # Connect 4 win condition met with multiple wins in one move
            self.board_6x7.update_square(5, col, "b")
        win_checker = WinChecker(self.board_6x7, 4)
        self.assertTrue(win_checker.check_for_winner())

    def test_diagonal_win_right(self):
        """Test if right diagonal win condition is detected."""
        for i in range(4):
            self.board_6x7.update_square(i, i, "b")
        self.board_6x7.update_square(5, 6, "r")
        win_checker = WinChecker(self.board_6x7, 4)
        self.assertTrue(win_checker.check_for_winner())

    def test_diagonal_win_right_connect_2_of_4(self):
        """Test if right diagonal win condition is detected."""
        for i in range(4):
            self.board_6x7.update_square(i, i, "b")
        self.board_6x7.update_square(5, 6, "r")
        win_checker = WinChecker(self.board_6x7, 2)
        self.assertTrue(win_checker.check_for_winner())

    def test_diagonal_win_left(self):
        """Test if left diagonal win condition is detected."""
        self.board_6x7.update_square(2, 4, "r")
        self.board_6x7.update_square(3, 3, "r")
        self.board_6x7.update_square(4, 2, "r")
        self.board_6x7.update_square(5, 1, "r")
        win_checker = WinChecker(self.board_6x7, 4)
        self.assertTrue(win_checker.check_for_winner())

    def test_no_false_positives(self):
        """Ensure no false winners are detected when no win condition is met."""
        win_checker = WinChecker(self.board_6x7, 4)
        self.assertFalse(win_checker.check_for_winner())

    def test_invalid_win_condition(self):
        """Ensure ValueError is raised for win conditions greater than 7."""
        win_checker = WinChecker(self.board_6x7, 8)
        with self.assertRaises(ValueError):
            win_checker.check_for_winner()

if __name__ == "__main__":    
    unittest.main()
