import requests


# Function to fetch the leagues for a given user ID and year
def get_leagues(user_id, year="2024"):
    # Construct the URL for fetching leagues
    leagues_url = f'https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}'

    # Make the HTTP GET request
    response = requests.get(leagues_url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch leagues for user {user_id}. HTTP status code: {response.status_code}")

    # Parse the JSON response
    leagues_data = response.json()

    # Return the list of leagues
    return leagues_data