from flask import Flask, jsonify

app = Flask(__name__)

# Example API route
@app.route('/api/gameid/<game_id>', methods=['GET'])
def get_game(game_id):
    # Example response
    return jsonify({"game_id": game_id, "message": "Game found!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
