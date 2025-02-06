
from flask import Flask, render_template
from flask_sock import Sock
import sys
from io import StringIO
from tictactoe import Game, Player, Square, AIPlayer

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def home():
    return render_template('terminal.html')

@sock.route('/terminal')
def terminal(ws):
    game = Game()
    output = StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    try:
        game.print_welcome_box()
        game.print_intro()
        game.add_player(Player("Player 1", Square.X))
        game.add_player(AIPlayer())
        game.print_board()
        
        initial_output = output.getvalue()
        if initial_output:
            ws.send(initial_output)
            output.truncate(0)
            output.seek(0)

        while True:
            user_input = ws.receive()
            if user_input:
                try:
                    row, col = map(int, user_input.split(','))
                    if 1 <= row <= 3 and 1 <= col <= 3:
                        row -= 1
                        col -= 1
                        if not game.game_board.square_is_occupied(row, col):
                            game.take_turn(game.players[0], row, col)
                            game.print_board()
                            
                            if game.check_for_winner():
                                print(f"\nWinner: {game.players[0].name}!")
                                break
                                
                            # AI's turn
                            ai_row, ai_col = game.players[1].move(game.game_board)
                            game.take_turn(game.players[1], ai_row, ai_col)
                            game.print_board()
                            
                            if game.check_for_winner():
                                print(f"\nWinner: {game.players[1].name}!")
                                break
                        else:
                            print("\nThat square is already occupied! Try again.\n")
                    else:
                        print("\nInvalid move! Row and column must be between 1 and 3.\n")
                except (ValueError, IndexError):
                    print("\nInvalid input format. Use row,col (e.g., 1,2)\n")
                
                new_output = output.getvalue()
                if new_output:
                    ws.send(new_output)
                    output.truncate(0)
                    output.seek(0)
    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
