
from flask import Flask, render_template, request, jsonify
from tictactoe import Game, Player, Square, AIPlayer

app = Flask(__name__)
game = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    data = request.json
    game_type = data.get('gameType')
    player_name = data.get('playerName')
    difficulty = data.get('difficulty')
    
    game = Game()
    game.add_player(Player(player_name, Square.X))
    
    if game_type == 'single':
        if difficulty == 'easy':
            diff_setting = None
        elif difficulty == 'intermediate':
            diff_setting = False
        else:
            diff_setting = True
        game.add_player(AIPlayer(difficulty=diff_setting))
    else:
        game.add_player(Player(data.get('player2Name'), Square.O))
    
    return jsonify({'status': 'success'})

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    row = data.get('row')
    col = data.get('col')
    
    if game.game_board.square_is_occupied(row, col):
        return jsonify({'status': 'invalid'})
        
    game.take_turn(game.players[0])
    
    if game.check_for_winner():
        return jsonify({
            'status': 'winner',
            'board': [str(square) for row in game.game_board.get_rows() for square in row],
            'winner': game.players[0].name
        })
    
    if isinstance(game.players[1], AIPlayer):
        ai_row, ai_col = game.players[1].move(game.game_board)
        game.game_board.update_square(ai_row, ai_col, Square.O)
        
        if game.check_for_winner():
            return jsonify({
                'status': 'winner',
                'board': [str(square) for row in game.game_board.get_rows() for square in row],
                'winner': game.players[1].name
            })
    
    return jsonify({
        'status': 'continue',
        'board': [str(square) for row in game.game_board.get_rows() for square in row]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
