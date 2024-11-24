from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Game state
game_data = {
    'player1': '',
    'player2': '',
    'player3': ''
}
current_player = 1
current_letter = ''
word_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_letter', methods=['POST'])
def generate_letter():
    global current_letter
    from random import choice
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    current_letter = choice(letters)
    return jsonify({'letter': current_letter})

@app.route('/submit_word', methods=['POST'])
def submit_word():
    global current_player, word_history
    word = request.json.get('word')
    
    if word and word[0].upper() == current_letter:
        word_history.append(f'Player {current_player}: {word}')
        current_player = (current_player % 3) + 1  # Switch between players
        return jsonify({'message': f'Player {current_player} played: {word}. Now it\'s Player {current_player}\'s turn.'})
    else:
        return jsonify({'message': f'Please enter a word starting with {current_letter}.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
