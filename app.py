from flask import Flask, render_template
from flask_sock import Sock
import sys
from io import StringIO
from tictactoe import Game, Player, Square, AIPlayer, set_console_window_size

app = Flask(__name__)
sock = Sock(app)
game = None

@app.route('/')
def home():
    return render_template('terminal.html')

@sock.route('/terminal')
def terminal(ws):
    old_stdout = sys.stdout
    output = StringIO()
    sys.stdout = output

    try:
        set_console_window_size(85, 30)
        game = Game()
        game.print_welcome_box()
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
                    if game.game_board.square_is_occupied(row, col):
                        print("Invalid move. Try again.")
                    else:
                        game.take_turn(game.players[0], row, col)
                        if game.check_for_winner():
                            print(f"Winner: {game.players[0].name}")
                            break
                        if isinstance(game.players[1], AIPlayer):
                            ai_row, ai_col = game.players[1].move(game.game_board)
                            game.take_turn(game.players[1], ai_row, ai_col)
                            if game.check_for_winner():
                                print(f"Winner: {game.players[1].name}")
                                break

                except (ValueError, IndexError):
                    print("Invalid input format. Use row,col (e.g., 0,1)")
                sys.stdout.flush()
                new_output = output.getvalue()
                if new_output:
                    ws.send(new_output)
                output.truncate(0)
                output.seek(0)

    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)