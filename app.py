
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import db, GameResult
from tictactoe import Game, Player, Square, AIPlayer
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    results = GameResult.query.order_by(GameResult.wins.desc()).all()
    return render_template('index.html', results=results)

@app.route('/play', methods=['POST'])
def play():
    player_name = request.form.get('player_name')
    game_mode = request.form.get('game_mode')
    
    if not player_name:
        return redirect(url_for('home'))
        
    # Create or update player record
    player = GameResult.query.filter_by(player_name=player_name).first()
    if not player:
        player = GameResult(player_name=player_name)
        db.session.add(player)
        db.session.commit()
        
    return render_template('game.html', player_name=player_name, game_mode=game_mode)

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    player_name = data.get('player_name')
    result = data.get('result')
    
    player = GameResult.query.filter_by(player_name=player_name).first()
    
    if result == 'win':
        player.wins += 1
    elif result == 'loss':
        player.losses += 1
    else:
        player.draws += 1
        
    db.session.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
