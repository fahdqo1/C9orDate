from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

# Define the path where your ZIP files are stored
ZIP_FILES_PATH = os.path.join(os.getcwd(), "games")

# Ensure the directory exists
os.makedirs(ZIP_FILES_PATH, exist_ok=True)

@app.route("/api/gameid/<game_id>.zip", methods=["GET"])
def get_game_zip(game_id):
    zip_file = f"{game_id}.zip"
    zip_file_path = os.path.join(ZIP_FILES_PATH, zip_file)

    if os.path.exists(zip_file_path):
        return send_from_directory(ZIP_FILES_PATH, zip_file, as_attachment=True)
    else:
        return jsonify({"error": "Game not found", "game_id": game_id}), 404

if __name__ == "__main__":
    app.run(debug=True)
