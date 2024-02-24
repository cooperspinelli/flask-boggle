from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    game_data = {"gameId": game_id,
                 "board": game.board}

    return jsonify(game_data)


@app.post('/api/score-word')
def handle_score_word():
    """handles score word endpoint, returns status of word"""

    request_data = request.get_json()
    game = games[request_data["gameId"]]
    word = request_data['word'].upper()

    word_response = {}

    # TODO: clean this up syntactically

    if not game.is_word_in_word_list(word):
        word_response['result'] = "not-word"
    elif not game.check_word_on_board(word):
        word_response['result'] = "not-on-board"
    else:
        game.play_and_score_word(word)
        word_response['result'] = "ok"

    return jsonify(word_response)


