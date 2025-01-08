from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__)

# Define paths
DATA_FILES_PATH = os.path.join(os.getcwd(), "data")
GAME_DATA_FILE = "game_data.json"
LOGIN_FILE_PATH = os.path.join(os.getcwd(), "code", "login.json")
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
        
@app.route("/api/validate-login", methods=["GET", "POST"])
def validate_login():
    if request.method == "GET":
        return jsonify({"message": "Use POST to validate login"})
    
    if request.method == "POST":
        try:
            data = request.json
            user_id = data.get("user_id")
            if not user_id:
                return jsonify({"status": "error", "message": "User ID is missing"}), 400

            # Read login.json
            if os.path.exists(LOGIN_FILE_PATH):
                with open(LOGIN_FILE_PATH, "r") as file:
                    valid_ids = json.load(file)  # Parse JSON

                for entry in valid_ids:
                    if entry.get("user_id") == user_id:
                        return jsonify({"status": "success", "message": "1"})

                return jsonify({"status": "error", "message": "Invalid User ID"}), 401
            else:
                return jsonify({"status": "error", "message": "Login file not found"}), 500
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/game-data", methods=["GET"])
def get_game_data():
    file_path = os.path.join(DATA_FILES_PATH, GAME_DATA_FILE)
    
    if os.path.exists(file_path):
        return send_from_directory(DATA_FILES_PATH, GAME_DATA_FILE, as_attachment=False)
    else:
        return jsonify({"error": "Game data not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)
