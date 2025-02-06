
from flask import Flask, render_template
from database import db, GameResult
from tictactoe import Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_results.db'
db.init_app(app)

@app.route('/')
def home():
    results = GameResult.query.all()
    return render_template('index.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=3000)
