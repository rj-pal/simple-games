from flask import Flask, render_template
from flask_sock import Sock
from tictactoe import Game, set_console_window_size
import sys
from io import StringIO

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def home():
    return render_template('terminal.html')

@sock.route('/terminal')
def terminal(ws):
    # Redirect stdout to capture console output
    old_stdout = sys.stdout
    sys.stdout = output = StringIO()

    try:
        # Initialize game
        set_console_window_size(85, 30)
        game = Game()
        game.start_game()

        # Send initial output
        ws.send(output.getvalue())
        output.truncate(0)
        output.seek(0)

        # Handle input
        while True:
            user_input = ws.receive()
            if user_input:
                # Process input and capture output
                print(user_input, end='')
                ws.send(output.getvalue())
                output.truncate(0)
                output.seek(0)

    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)