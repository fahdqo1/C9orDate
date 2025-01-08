from flask import Flask, jsonify, request, send_from_directory
import os
import json
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'gast102030',  # Replace with your MySQL root password
    'database': 'activation_keys_db'
}

# Define paths
DATA_FILES_PATH = os.path.join(os.getcwd(), "data")
GAME_DATA_FILE = "game_data.json"
NEW_GAMES_FILE = "game_newadded.json"  # New file for recently added games
ZIP_FILES_PATH = os.path.join(os.getcwd(), "games")

# Ensure directories exist
os.makedirs(ZIP_FILES_PATH, exist_ok=True)

def get_db_connection():
    """Establish a connection to the database."""
    return mysql.connector.connect(**DB_CONFIG)

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
            pc_name = data.get("pc_name")
            login_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            if not user_id or not pc_name:
                return jsonify({"status": "error", "message": "Missing required fields"}), 400

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Check if user ID exists and is active
            cursor.execute("SELECT * FROM activation_keys WHERE user_id = %s AND status = 'active'", (user_id,))
            key_data = cursor.fetchone()

            if key_data:
                # Log PC name and last login
                cursor.execute("""
                    UPDATE activation_keys
                    SET pc_name = %s, last_login = %s
                    WHERE user_id = %s
                """, (pc_name, login_date, user_id))
                conn.commit()
                conn.close()

                return jsonify({"status": "success", "message": "Login successful"})
            else:
                conn.close()
                return jsonify({"status": "error", "message": "Invalid or revoked key"}), 401
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/revoke-key", methods=["POST"])
def revoke_key():
    """Revoke or reactivate a user's key."""
    try:
        data = request.json
        user_id = data.get("user_id")
        action = data.get("action", "revoke")  # Default to revoke

        if not user_id:
            return jsonify({"status": "error", "message": "User ID is missing"}), 400

        new_status = 'revoked' if action == 'revoke' else 'active'

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE activation_keys SET status = %s WHERE user_id = %s", (new_status, user_id))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": f"Key {user_id} has been {new_status}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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
