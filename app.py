from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Store players, game state, and word history
players = []
current_letter = None
word_history = []
current_player_index = 0
current_word = None

@app.route('/')
def home():
    return render_template('index.html', players=players, word_history=word_history, current_letter=current_letter)

@app.route('/join_game', methods=['POST'])
def join_game():
    player_name = request.json.get('name')
    if len(players) < 3:  # Limiting to 3 players
        players.append({'name': player_name, 'role': f'Player{len(players) + 1}'})
        return jsonify({"message": f"{player_name} joined as {f'Player{len(players)}'}"}), 200
    else:
        return jsonify({"message": "Game is full. Only 3 players allowed."}), 400

@app.route('/generate_letter', methods=['POST'])
def generate_letter():
    global current_letter
    player_name = request.json.get('name')
    
    # Ensure that only Player 1 can generate a letter
    if len(players) > 1 and players[0]['name'] == player_name:
        current_letter = chr(random.randint(65, 90))  # Generates a random uppercase letter
        return jsonify({"letter": current_letter})
    else:
        return jsonify({"error": "Only Player 1 can generate the letter!"}), 403

@app.route('/submit_word', methods=['POST'])
def submit_word():
    global current_player_index, current_word
    player_name = request.json.get('name')
    word = request.json.get('word')

    # Ensure the current player is submitting a word
    if player_name != players[current_player_index]['name']:
        return jsonify({"error": "It's not your turn!"}), 403

    # Validate the word starts with the current letter or the previous word's last letter
    if current_word and word[0].upper() != current_word[-1].upper():
        return jsonify({"error": f"Word must start with {current_word[-1].upper()}"}), 400

    # Add the word to the history
    word_history.append(word)
    current_word = word

    # Move to the next player
    current_player_index = (current_player_index + 1) % len(players)
    return jsonify({"message": "Word submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
