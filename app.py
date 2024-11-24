from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# This will store the player data
players = []

@app.route('/')
def home():
    return render_template('index.html', players=players)

@app.route('/join_game', methods=['POST'])
def join_game():
    # Get the player's name and selected role
    player_name = request.json.get('name')
    if len(players) < 3:  # Limiting to 3 players
        players.append({'name': player_name, 'role': f'Player{len(players) + 1}'})
        return jsonify({"message": f"{player_name} joined as {f'Player{len(players)}'}"}), 200
    else:
        return jsonify({"message": "Game is full. Only 3 players allowed."}), 400

@app.route('/generate_letter', methods=['POST'])
def generate_letter():
    player_name = request.json.get('name')
    
    # Ensure that only Player 1 can generate a letter
    if len(players) > 0 and players[0]['name'] == player_name:
        random_letter = chr(random.randint(65, 90))  # Generates a random uppercase letter
        return jsonify({"letter": random_letter})
    else:
        return jsonify({"error": "Only Player 1 can generate the letter!"}), 403

if __name__ == '__main__':
    app.run(debug=True)
