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
        game.print_welcome_box()

        # Send initial output
        initial_output = output.getvalue()
        if initial_output:
            ws.send(initial_output)
        output.truncate(0)
        output.seek(0)

        # Handle input
        while True:
            try:
                user_input = ws.receive()
                if user_input:
                    # Redirect input to game
                    print(user_input, end='')
                    # Send any output back to client
                    new_output = output.getvalue()
                    if new_output:
                        ws.send(new_output)
                    output.truncate(0)
                    output.seek(0)
            except Exception as e:
                print(f"WebSocket error: {e}")
                break

    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)