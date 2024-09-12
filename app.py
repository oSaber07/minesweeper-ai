from flask import Flask, render_template, request, jsonify
from minesweeper_ai import MinesweeperAI

app = Flask(__name__)

game = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    global game
    data = request.json
    rows = data['rows']
    cols = data['cols']
    num_mines = data['mines']
    game = MinesweeperAI(rows, cols, num_mines)
    return jsonify({'message': 'New game created'})

@app.route('/make_move', methods=['POST'])
def make_move():
    global game
    data = request.json
    row = data['row']
    col = data['col']
    result = game.reveal(row, col)
    return jsonify({
        'result': result,
        'revealed': game.revealed,
        'flagged': game.flagged,
        'game_over': result == -1,
        'game_won': game.is_game_won()
    })

@app.route('/ai_move', methods=['POST'])
def ai_move():
    global game
    revealed, flagged = game.solve()
    return jsonify({
        'revealed': revealed,
        'flagged': flagged,
        'game_won': game.is_game_won()
    })

if __name__ == '__main__':
    app.run(debug=True)