from flask import Flask, send_from_directory, abort

app = Flask(__name__)

# Folder where game files are stored
GAME_FOLDER = "./games"

@app.route('/api/gameid/<game_id>.zip', methods=['GET'])
def download_game(game_id):
    try:
        # Ensure the requested file exists
        file_path = f"{game_id}.zip"
        return send_from_directory(GAME_FOLDER, file_path, as_attachment=True)
    except Exception as e:
        abort(404, description="Game not found")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
