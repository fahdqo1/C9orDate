from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Game Library!"

@app.route('/api/game/<game_id>')
def get_game(game_id):
    try:
        # Serve the game zip file
        return send_from_directory('games', f'{game_id}.zip', as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 404

if __name__ == "__main__":
    app.run(debug=True)
