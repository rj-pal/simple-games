from Game import *
from Board import *
from Player import *

def play_game(game_instance) -> None:
    """
    Simulates a single game by alternating turns between players.

    Parameters:
        game_instance (Game): The game instance to play.

    Behavior:
        - Alternates moves between players.
        - Makes moves based on player type (blind human/AI Player Mode).
        - Stops if a winner is found.
        - Updates game state and player stats post-game.
    """
    for round_count in range(game_instance.board_size):
        # Determine which player goes next based on turn order and position in game-instance tuple for X and O
        if game_instance.go_first:
            player = game_instance.players[round_count % 2]
        else:
            player = game_instance.players[(round_count % 2) - 1]

        # Handle moves based on player type
        if isinstance(player, TicTacToe.TicTacToePlayer): 
            while True:
                # Simulates blind human play (the same as AI easy mode)
                move = randint(0, 2), randint(0, 2), player.marker
                if game_instance.make_move(*move):
                    break
        elif isinstance(player, TicTacToe.AIPlayer):
            row, col = player.move(game_instance.board)
            game_instance.make_move(row, col, player.marker)

        # Check for a winner after a minimum number of moves
        if round_count >= 4 and game_instance.check_winner():
            break

    # Post-game updates and display of stats
    game_instance.update_winner_info()
    game_instance.update_players_stats()
    game_instance.reset_game_state()
    return


def test_games(number_of_games: int, ai_levels: dict, test_modes: dict) -> None:
    """
    Runs test games between a human player and AI at varying difficulty levels and modes.

    Parameters:
        number_of_games (int): The number of games to simulate per configuration.
        ai_levels (dict): A dictionary mapping AI difficulty names to internal difficulty values.
        test_modes (dict): A dictionary mapping test modes (offensive/defensive) to boolean values.

    Behavior:
        - Iterates through AI difficulty levels and test modes.
        - Creates an AI player for each configuration and simulates games versus a blind human.
        - Prints statistics after each configuration.
    """
    for difficulty_level, difficulty_bool_value in ai_levels.items():
        print(f"Blind mode tests for Player 1 versus AI Player ({difficulty_level} Mode).")
        for mode_name, go_first in test_modes.items():
            Game.create_ai_player(name=f"Computer ({difficulty_level} Mode - {mode_name})", difficulty=difficulty_bool_value)
            print(f"Player 1 moves first: {go_first}. Running {number_of_games} games.")
            
            for _ in range(number_of_games):
                Game.go_first = go_first
                play_game(Game)

            print(Game.print_stats())


def test_ai_games(number_of_games: int, ai_level1: any, ai_level2: any) -> None:
    """
    Simulates AI-versus-AI games at specified difficulty levels.

    Parameters:
        number_of_games (int): The number of games to simulate per configuration.
        ai_level1 (any): Difficulty level for the first AI player.
        ai_level2 (any): Difficulty level for the second AI player.

    Behavior:
        - Runs simulations with AI players of varying difficulty levels competing against each other.
        - Enforces rule that AI Hard mode cannot play X or be the first AI player in player tuple to keep AI logic
        - Alternates which AI goes first.
        - Prints statistics after each configuration.
    """
    ai_level_map = {None: "Easy", False: "Intermediate", True: "Hard"}

    if ai_level1:
        print("Testing Hard mode as X is not allowed unless both players are on Hard mode.")
        raise TypeError("Invalid AI difficulty configuration.")

    print(f"AI ({ai_level_map[ai_level1]} Mode) versus AI ({ai_level_map[ai_level2]} Mode).")
    for first_player in range(2):
        if first_player == 0:
            print(f"AI ({ai_level_map[ai_level2]}) moves first.")
        else:
            print(f"AI ({ai_level_map[ai_level1]}) moves first.")

        Game.add_ai_players_for_testing(ai_level1, ai_level2)

        for _ in range(number_of_games):
            Game.go_first = bool(first_player)
            play_game(Game)

        print(Game.print_stats())


# Configuration dictionaries
AI_LEVELS = {"Easy": None, "Intermediate": False, "Hard": True}
TEST_MODES = {"Offense": False, "Defense": True}

# Instantiate Game Object for Testing
Game = TicTacToe()

# Run human vs AI tests
test_games(1000, AI_LEVELS, TEST_MODES)

# Run AI vs AI tests
test_ai_games(1000, None, True)
test_ai_games(1000, False, True)
test_ai_games(1000, None, None)
test_ai_games(1000, False, False)

# Additional hard-mode-only AI vs AI tests
Game.add_two_hard_move_ai_players_for_testing()
print(f"AI (Hard Mode) versus AI (Hard Mode). Running {1000} games.")

for _ in range(1000):
    play_game(Game)

print(Game.print_stats())

# Exit script
exit()