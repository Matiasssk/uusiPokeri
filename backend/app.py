# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  
from make_move import make_move

app = Flask(__name__)
CORS(app)

@app.route('/api/make_move', methods=['POST'])
def get_move():
    data = request.get_json()
    hand = data['hand']
    board = data['board']
    pot_size = data['pot_size']
    player_chips = data['player_chips']
    game_stage = data['game_stage']
    
    move, bet_amount = make_move(hand, board, pot_size, player_chips, game_stage)
    
    return jsonify({"move": move, "bet_amount": bet_amount})

if __name__ == "__main__":
    app.run(debug=True)
