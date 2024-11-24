from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

# Store game state
game_state = {
    "letter": "",  # Current letter
    "history": []  # History of words
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

@socketio.on("generate_letter")
def generate_letter():
    letter = random.choice(string.ascii_lowercase)
    game_state["letter"] = letter
    game_state["history"] = []  # Clear history for a new round
    emit("new_letter", {"letter": letter, "history": []}, broadcast=True)

@socketio.on("submit_word")
def submit_word(data):
    word = data.get("word", "").strip().lower()
    if word and word[0] == game_state["letter"]:
        game_state["history"].append(word)
        game_state["letter"] = word[-1]  # Update the letter for the next turn
        emit("update_game", {"letter": game_state["letter"], "history": game_state["history"]}, broadcast=True)
    else:
        emit("invalid_word", {"message": f"Word must start with '{game_state['letter']}'"})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
