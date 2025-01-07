import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Define folders for games and other tools
GAME_FOLDER = os.path.join(os.getcwd(), 'uploads', 'games')
TOOLS_FOLDER = os.path.join(os.getcwd(), 'uploads', 'tools')
os.makedirs(GAME_FOLDER, exist_ok=True)
os.makedirs(TOOLS_FOLDER, exist_ok=True)

# Route to upload files to a specific category
@app.route('/api/upload/<category>', methods=['POST'])
def upload_file(category):
    if category not in ['gameid', 'other']:
        return jsonify({"message": "Invalid category. Use 'gameid' or 'other'"}), 400
    
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    if category == 'gameid':
        save_folder = GAME_FOLDER
    else:
        save_folder = TOOLS_FOLDER

    file_path = os.path.join(save_folder, file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully", "filename": file.filename, "category": category}), 200

# Route to download game files
@app.route('/api/gameid/<filename>', methods=['GET'])
def download_game_file(filename):
    try:
        return send_from_directory(GAME_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"message": "Game file not found"}), 404

# Route to download other tools
@app.route('/api/other/<filename>', methods=['GET'])
def download_other_file(filename):
    try:
        return send_from_directory(TOOLS_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"message": "Tool file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
