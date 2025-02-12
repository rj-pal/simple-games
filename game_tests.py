from Game import *

# Game Tests for Board Conditions

# Define the move patterns
move_patterns = [
    ("x wins in column", [(1, 1, 'x'), (0, 1, 'o'), (0, 0, 'x'), (2, 2, 'o'), (2, 0, 'x'), (2, 1, 'o'), (1, 0, 'x')]),
    ("o wins in second row", [(1, 0, 'o'), (0, 0, 'x'), (1, 1, 'o'), (0, 1, 'x'), (1, 2, 'o')]),
    ("x wins diagonally", [(0, 0, 'x'), (0, 1, 'o'), (1, 1, 'x'), (0, 2, 'o'), (2, 2, 'x')]),
    ("no winner", [(0, 0, 'x'), (0, 1, 'o'), (0, 2, 'x'), (1, 1, 'o'), (1, 0, 'x'), (1, 2, 'o'), (2, 1, 'x'), (2, 0, 'o'), (2, 2, 'x')])
]

# Initialize the game
Game = TicTacToe()
for pattern_name, moves in move_patterns:
    print(f"\nTesting pattern: {pattern_name}")    
    
    for i, move in enumerate(moves):
        Game.round_count += 1  
        player = Game.players[i % 2]
        name = player.get_player_name()
        print("NOW PLAYING", name)
        Game.make_move(*move)
        print(Game.board.__str__())
        
        if i >= 4 and Game.check_winner():
            print("WINNER FOUND")
            break
    else:
        print("TIE")
        # Game.reset_winner()
    # Final game updates
    Game.update_winner_info()
    Game.update_players_stats()
    
    Game.print_winner()
    print(Game.print_stats())
    Game.reset_game_state()

exit()


  

# print(board(3,3))
# exit()
# pair_list = []     
# for i in range(9):
#     pair_list.append(int_converter(i,3))
# print(pair_list)
# for pair in pair_list:
#     print(pair_converter(pair, 3))
exit()

# T = TicTacToe()
# T.update_player_name("Joe", "x")
# T.update_player_name("Mason", "O")

# T.winner = T.players[0]
# print(T.winner.name)
# T.update_players_stats()

# T.players[0].game_played()
# print(T.players)

# T.update_player("", "x")
# print(T.players)
# print(T.check_for_winner())
# T.print_winner()

# print(T.board)
# print(T.get_columns())
# print(T.get_rows())
# T.reset_board()
# print(T.board)
# T.update_square(2, 2, 'X')

# T.update_players()
# print(T.players)