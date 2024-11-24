from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game state
game_state = {
    "current_letter": "",
    "last_letter": "",
    "turn": 1,
    "players": ["Player 1", "Player 2", "Player 3"],
    "num_players": 2,  # Adjust for 2 or 3 players
    "history": []
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-letter", methods=["POST"])
def generate_letter():
    letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    game_state["current_letter"] = letter
    game_state["last_letter"] = ""
    return jsonify({"letter": letter})

@app.route("/submit-word", methods=["POST"])
def submit_word():
    word = request.json.get("word").strip()
    if not word:
        return jsonify({"error": "Please enter a word!"}), 400

    current_player = game_state["players"][game_state["turn"] - 1]
    if game_state["last_letter"] and not word.startswith(game_state["last_letter"]):
        return jsonify({"error": f"Word must start with '{game_state['last_letter']}'!"}), 400

    if not game_state["last_letter"] and not word.startswith(game_state["current_letter"]):
        return jsonify({"error": f"Word must start with the letter '{game_state['current_letter']}'!"}), 400

    game_state["history"].append({"player": current_player, "word": word})
    game_state["last_letter"] = word[-1].upper()
    game_state["turn"] = (game_state["turn"] % game_state["num_players"]) + 1

    return jsonify({
        "next_player": game_state["players"][game_state["turn"] - 1],
        "history": game_state["history"]
    })

if __name__ == "__main__":
    app.run(debug=True)
