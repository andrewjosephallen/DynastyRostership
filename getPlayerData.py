import requests
import json


def get_player_data():
    # URL to fetch data from
    player_url = 'https://api.sleeper.app/v1/players/nfl'

    # Fetch the data from the URL
    response = requests.get(player_url)

    # Raise an exception if the request was not successful
    response.raise_for_status()

    # Parse the JSON data
    player_data = response.json()

    # Return the parsed player data
    return player_data
