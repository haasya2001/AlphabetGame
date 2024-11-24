from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select_player', methods=['POST'])
def select_player():
    player = request.json.get('player')
    if player == "Player1":
        return jsonify({"message": f"{player} selected. Ready to generate a letter."})
    else:
        return jsonify({"message": f"{player} selected. Cannot generate a letter."})

@app.route('/generate_letter', methods=['POST'])
def generate_letter():
    player = request.json.get('player')
    if player == "Player1":
        random_letter = chr(random.randint(65, 90))  # Generates a random uppercase letter
        return jsonify({"letter": random_letter})
    else:
        return jsonify({"error": "Only Player1 can generate the letter!"}), 403

if __name__ == '__main__':
    app.run(debug=True)
