from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Game state
game_state = {
    'players': {},
    'current_player': 1,
    'current_letter': '',
    'word_history': []
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def handle_join(data):
    # Add player to the game
    player_id = data['player_id']
    player_name = data['player_name']

    if len(game_state['players']) < 3:  # Maximum 3 players
        game_state['players'][player_id] = player_name
        emit('update_players', game_state['players'], broadcast=True)

@socketio.on('start_game')
def handle_start_game():
    import random
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    game_state['current_letter'] = random.choice(letters)
    game_state['word_history'] = []
    game_state['current_player'] = 1

    emit('game_started', {
        'current_letter': game_state['current_letter'],
        'current_player': game_state['current_player'],
        'word_history': game_state['word_history']
    }, broadcast=True)

@socketio.on('submit_word')
def handle_submit_word(data):
    word = data['word']
    player_id = data['player_id']

    # Validate the word
    if not word.upper().startswith(game_state['current_letter']):
        emit('invalid_word', {'message': f'Word must start with "{game_state["current_letter"]}"'}, room=request.sid)
        return

    # Add word to history
    player_name = game_state['players'][player_id]
    game_state['word_history'].append(f'{player_name}: {word}')

    # Update the next turn
    game_state['current_player'] = (game_state['current_player'] % len(game_state['players'])) + 1
    game_state['current_letter'] = word[-1].upper()  # Next letter is the last letter of the submitted word

    # Broadcast updated game state
    emit('update_game', {
        'current_letter': game_state['current_letter'],
        'current_player': game_state['current_player'],
        'word_history': game_state['word_history']
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
