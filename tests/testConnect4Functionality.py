import unittest
from games.games import ConnectFour

class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.game = ConnectFour()

    def test_invalid_column_index_1(self):
        """Test adding a piece to an out-of-bounds column"""
        self.assertFalse(self.game.make_move(7, "r"))  # Column index too high should return False

    def test_invalid_column_index_2(self):
        """Test adding a piece to an out-of-bounds column"""
        self.assertFalse(self.game.make_move(-1, "y"))  # Column index too high should return False
    
    def test_full_column(self):
        """Test adding a piece to a full column"""
        for _ in range(6):  # Fill the column
            self.game.make_move(0, "r")
        self.assertFalse(self.game.make_move(0, "y"))  # Column is full should return False
    
    def test_horizontal_win(self):
        """Test horizontal win condition"""
        self.game.make_move(0, "r")
        self.game.make_move(1, "r")
        self.game.make_move(2, "r")
        self.game.make_move(3, "r")
        self.assertTrue(self.game.check_winner())
    
    def test_vertical_win(self):
        """Test vertical win condition"""
        self.game.make_move(0, "y")
        self.game.make_move(0, "y")
        self.game.make_move(0, "y")
        self.game.make_move(0, "y")
        self.assertTrue(self.game.check_winner())
    
    def test_diagonal_win(self):
        """Test diagonal win condition"""
        self.game.make_move(0, "r")
        self.game.make_move(1, "y")
        self.game.make_move(1, "r")
        self.game.make_move(2, "y")
        self.game.make_move(2, "y")
        self.game.make_move(2, "r")
        self.game.make_move(3, "y")
        self.game.make_move(3, "y")
        self.game.make_move(3, "y")
        self.game.make_move(3, "r")
        self.assertTrue(self.game.check_winner())
    
    def test_no_winner(self):
        """Test that no winner is detected incorrectly"""
        self.game.make_move(0, "r")
        self.game.make_move(1, "y")
        self.game.make_move(2, "r")
        self.game.make_move(3, "y")
        self.assertFalse(self.game.check_winner())
    
    def test_full_board_no_winner(self):
        """Test a full board with no winner"""
        moves = [
            ["r", "y", "r", "r", "r", "y", "r"],
            ["y", "r", "y", "r", "y", "r", "y"],
            ["r", "y", "y", "r", "y", "y", "r"],
            ["y", "r", "r", "y", "r", "y", "y"],
            ["r", "y", "r", "y", "r", "y", "r"],
            ["y", "r", "y", "y", "y", "r", "y"]
        ]
        for row in moves:
            for col, piece in enumerate(row):
                self.game.make_move(col, piece)
        self.assertFalse(self.game.check_winner())
    
if __name__ == "__main__":
    unittest.main()
