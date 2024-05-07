import requests


# Function to get the user ID given a Sleeper username
def get_user(sleeper_username):
    # URL for fetching user information
    user_url = f'https://api.sleeper.app/v1/user/{sleeper_username}'

    # Make the HTTP GET request to the Sleeper API
    response = requests.get(user_url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch user data for {sleeper_username}. HTTP status code: {response.status_code}")

    # Parse the response JSON data
    user_data = response.json()

    # Return the user ID
    return user_data.get("user_id")