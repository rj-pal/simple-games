import unittest
import Game

def play_game(Game, x_first, move_list):
    Game.reset_game_state()
    Game.go_first = x_first
    for i in range(Game.board_size): 
        if Game.go_first:
            player = Game.players[i % 2]
        else:
            player = Game.players[i % 2 - 1]
        
        while True:
            move = *move_list[i], player.marker
            if Game.make_move(*move):
                break
            else:
                i += 1

        if i >= 4 and Game.check_winner():
            break
    Game.update_winner_info()
    Game.update_players_stats()
    print(Game.print_stats())
    return Game.get_winner_info()

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        """Set up a new Tic Tac Toe game instance for each test."""
        self.Game = Game.TicTacToe()


    def test_x_wins_rows(self):
        """Test all row wins for 'x'."""
        moves = [
            ([(0, 0), (1, 0), (0, 1), (2, 0), (0, 2)], {'marker': 'x', 'type': 'row', 'row': 0, 'column': 0}),
            ([(1, 0), (0, 0), (1, 1), (2, 0), (1, 2)], {'marker': 'x', 'type': 'row', 'row': 1, 'column': 0}),
            ([(2, 0), (0, 0), (2, 1), (1, 0), (2, 2)], {'marker': 'x', 'type': 'row', 'row': 2, 'column': 0}),
        ]
        for move_list, expected in moves:
            with self.subTest(move_list=move_list):
                result = play_game(self.Game, True, move_list)
                self.assertEqual(result, expected)

    def test_x_wins_columns(self):
        """Test all column wins for 'x'."""
        moves = [
            ([(0, 0), (0, 1), (1, 0), (0, 2), (2, 0)], {'marker': 'x', 'type': 'column', 'row': 0, 'column': 0}),
            ([(0, 1), (0, 0), (1, 1), (0, 2), (2, 1)], {'marker': 'x', 'type': 'column', 'row': 0, 'column': 1}),
            ([(0, 2), (0, 0), (1, 2), (0, 1), (2, 2)], {'marker': 'x', 'type': 'column', 'row': 0, 'column': 2}),
        ]
        for move_list, expected in moves:
            with self.subTest(move_list=move_list):
                result = play_game(self.Game, True, move_list)
                self.assertEqual(result, expected)

    def test_x_wins_diagonals(self):
        """Test diagonal wins for 'x'."""
        moves = [
            ([(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)], {'marker': 'x', 'type': 'right_diagonal', 'row': 0, 'column': 0}),
            ([(0, 2), (0, 1), (1, 1), (0, 0), (2, 0)], {'marker': 'x', 'type': 'left_diagonal', 'row': 0, 'column': 2}),
        ]
        for move_list, expected in moves:
            with self.subTest(move_list=move_list):
                result = play_game(self.Game, True, move_list)
                self.assertEqual(result, expected)

    def test_o_wins_rows(self):
        """Test all row wins for 'o'."""
        moves = [
            ([(0, 0), (1, 0), (0, 1), (2, 0), (0, 2)], {'marker': 'o', 'type': 'row', 'row': 0, 'column': 0}),
            ([(1, 0), (0, 0), (1, 1), (2, 0), (1, 2)], {'marker': 'o', 'type': 'row', 'row': 1, 'column': 0}),
            ([(2, 0), (0, 0), (2, 1), (1, 0), (2, 2)], {'marker': 'o', 'type': 'row', 'row': 2, 'column': 0}),
        ]
        for move_list, expected in moves:
            with self.subTest(move_list=move_list):
                result = play_game(self.Game, False, move_list)
                self.assertEqual(result, expected)

    def test_o_wins_columns(self):
        """Test all column wins for 'o'."""
        moves = [
            ([(0, 0), (0, 1), (1, 0), (0, 2), (2, 0)], {'marker': 'o', 'type': 'column', 'row': 0, 'column': 0}),
            ([(0, 1), (0, 0), (1, 1), (0, 2), (2, 1)], {'marker': 'o', 'type': 'column', 'row': 0, 'column': 1}),
            ([(0, 2), (0, 0), (1, 2), (0, 1), (2, 2)], {'marker': 'o', 'type': 'column', 'row': 0, 'column': 2}),
        ]
        for move_list, expected in moves:
            with self.subTest(move_list=move_list):
                result = play_game(self.Game, False, move_list)
                self.assertEqual(result, expected)

    def test_o_wins_diagonals(self):
        """Test diagonal wins for 'o'."""
        moves = [
            ([(1, 0), (0, 0), (2, 1), (1, 1), (0, 1), (2, 2)], {'marker': 'o', 'type': 'right_diagonal', 'row': 0, 'column': 0}),
            ([(1, 0), (0, 2), (2, 1), (1, 1), (0, 0), (2, 0)], {'marker': 'o', 'type': 'left_diagonal', 'row': 0, 'column': 2}),
        ]
        for move_list, expected in moves:
            with self.subTest(move_list=move_list):
                result = play_game(self.Game, True, move_list)
                self.assertEqual(result, expected)

    def test_draw(self):
        """Test a game ending in a draw."""
        move_list = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)]
        expected = {'marker': None, 'type': None, 'row': None, 'column': None}
        result = play_game(self.Game, True, move_list)
        self.assertEqual(result, expected)

    def test_one_occupied_square_move(self):
        """Test trying to add a move to an already occupied square."""
        move_list = [(0, 0), (0, 1), (0, 0), (1, 1), (0, 2), (2, 2)]
        result = play_game(self.Game, True, move_list)
        # Expect the valid game outcome after ignoring the invalid move
        expected = {'marker': 'x', 'type': 'right_diagonal', 'row': 0, 'column': 0}
        self.assertEqual(result, expected)

    def test_invalid_moves(self):
        """Test trying to add a move to an already occupied square."""
        move_list = [(0, 0), (0, 1), (3, 3),(0, 0), (1, 1), (0, 2), (-3, -3), (2, 2)]
        result = play_game(self.Game, True, move_list)
        # Expect the valid game outcome after ignoring the invalid move
        expected = {'marker': 'x', 'type': 'right_diagonal', 'row': 0, 'column': 0}
        self.assertEqual(result, expected)

    # def test_x_statistics(self):
    #     result = self.Game.players[0].win_count
    #     expected = 9
    #     self.assertEqual(result,expected)

if __name__ == '__main__':
    unittest.main()
