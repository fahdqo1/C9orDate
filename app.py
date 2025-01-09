from flask import Flask, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

# Define paths
DATA_FILES_PATH = os.path.join(os.getcwd(), "data")
GAME_DATA_FILE = "game_data.json"
NEW_GAMES_FILE = "game_newadded.json"
ZIP_FILES_PATH = os.path.join(os.getcwd(), "games")

# Ensure directories exist
os.makedirs(ZIP_FILES_PATH, exist_ok=True)

@app.route("/api/gameid/<game_id>.zip", methods=["GET"])
def get_game_zip(game_id):
    zip_file = f"{game_id}.zip"
    zip_file_path = os.path.join(ZIP_FILES_PATH, zip_file)

    if os.path.exists(zip_file_path):
        return send_from_directory(ZIP_FILES_PATH, zip_file, as_attachment=True)
    else:
        return jsonify({"error": "Game not found", "game_id": game_id}), 404

@app.route("/api/game-data", methods=["GET"])
def get_game_data():
    file_path = os.path.join(DATA_FILES_PATH, GAME_DATA_FILE)
    
    if os.path.exists(file_path):
        return send_from_directory(DATA_FILES_PATH, GAME_DATA_FILE, as_attachment=False)
    else:
        return jsonify({"error": "Game data not found"}), 404

@app.route("/api/new-games", methods=["GET"])
def get_new_games():
    file_path = os.path.join(DATA_FILES_PATH, NEW_GAMES_FILE)
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            new_games = json.load(file)
        return jsonify(new_games)
    else:
        return jsonify({"error": "New games data not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
