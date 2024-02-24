from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle</title>', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            # make a post request to /api/new-game
            response = client.post('/api/new-game')
            # get the response body as json using .get_json()
            response_data = response.get_json()

            # test that the game_id is a string
            self.assertIsInstance(response_data["gameId"], str)
            # test that the board is a list
            self.assertIsInstance(response_data["board"], list)
            # test that the game_id is in the dictionary of games (imported from app.py above)
            # TODO:test response data more specifically
            self.assertIn(response_data["gameId"], games)


    def test_score_word(self):
        """Test if word is valid"""

        # with self.client as client:
        with app.test_client() as client:
            # make a post request to /api/new-game
            response = client.post("/api/new-game")
            # get the response body as json using .get_json()
            response_data = response.get_json()
            # find that game in the dictionary of games (imported from app.py above)
            game_id = response_data["gameId"]
            game = games[game_id]
            # manually change the game board's rows so they are not random
            game.board = [
                ['C', 'A', 'T', 'E', 'E'],
                ['E', 'E', 'E', 'E', 'E'],
                ['E', 'E', 'E', 'E', 'E'],
                ['E', 'E', 'E', 'E', 'E'],
                ['E', 'E', 'E', 'E', 'E']
            ]

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            json_data = {"gameId": game_id, "word": "CAT"}
            response = client.post("api/score-word", json=json_data)
            response_data = response.get_json()

            self.assertEqual(response_data["result"], "ok")

            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            json_data = {"gameId": game_id, "word": "DOG"}
            response = client.post("api/score-word", json=json_data)
            response_data = response.get_json()

            self.assertEqual(response_data["result"], "not-on-board")

            # test to see that an invalid word returns {'result': 'not-word'}
            json_data = {"gameId": game_id, "word": "ghpft"}
            response = client.post("api/score-word", json=json_data)
            response_data = response.get_json()

            self.assertEqual(response_data["result"], "not-word")
