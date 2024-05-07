import requests
from getUser import get_user
from getLeagues import get_leagues
# Function to get rostership based on a user and player data
def get_rostership(sleeper_username, player_data):
    user_id = get_user(sleeper_username)
    leagues_data = get_leagues(user_id)
    total_number_of_leagues = len(leagues_data)

    league_names = []
    player_object_list = {}

    # Iterate over each league to fetch rosters
    for league in leagues_data:
        league_id = league["league_id"]
        league_name = league["name"]

        league_names.append(league_name)

        rosters_url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
        rosters_response = requests.get(rosters_url)
        rosters_response.raise_for_status()
        rosters_data = rosters_response.json()

        # Process rosters to find player's ownership
        for current_roster in rosters_data:
            if current_roster["owner_id"] == user_id:
                players = current_roster.get("players", [])
                if players is None:
                    players = []
                for player_id in players:
                    player = player_data.get(player_id, None)

                    if player is not None:
                        player_name = player["full_name"]
                        if player_name in player_object_list:
                            player_object_list[player_name]["numberOfOccurances"] += 1
                            player_object_list[player_name]["leagues"] += f", {league_name}"
                        else:
                            team = player.get("team", "FA")
                            position = player["position"]
                            new_player = {
                                "position": position,
                                "team": team,
                                "numberOfOccurances": 1,
                                "numberOfLeagues": total_number_of_leagues,
                                "leagues": league_name,
                            }
                            player_object_list[player_name] = new_player

    return player_object_list