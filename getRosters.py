from getUser import get_user
from getLeagues import get_leagues
import requests
from getDraftPicks import get_draft_picks

# Function to fetch team rosters for a given Sleeper username and player data
def get_rosters(sleeper_username, player_data):
    # Get the user ID and leagues data
    user_id = get_user(sleeper_username)
    leagues_data = get_leagues(user_id)
    total_number_of_leagues = len(leagues_data)

    # List to store roster objects
    roster_object_list = []

    # Iterate over each league to gather information
    for league in leagues_data:
        league_id = league["league_id"]
        league_name = league["name"]
        total_teams = league["total_rosters"]
        ppr = league.get("scoring_settings", {}).get("rec", "N/A")
        tep = league.get("scoring_settings", {}).get("bonus_rec_te", "N/A")
        positions = league["roster_positions"]

        # Determine the number of starters and QB setup
        starters = sum(1 for pos in positions if pos != "BN")
        qb = None

        for pos in positions:
            if pos == "SUPER_FLEX":
                qb = "SF"
            elif pos == "QB":
                if qb is None:
                    qb = "1QB"
                elif qb == "1QB":
                    qb = "2QB"

        # Fetch rosters for the league
        rosters_url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
        rosters_response = requests.get(rosters_url)
        rosters_response.raise_for_status()
        rosters_data = rosters_response.json()

        # Iterate through rosters to find the user's roster
        for current_roster in rosters_data:
            if current_roster["owner_id"] == user_id:
                roster_id = current_roster["roster_id"]
                draft_picks = get_draft_picks(league_id, roster_id, league_name)

                # Get team record
                settings = current_roster.get("settings", {})
                wins = settings.get("wins", 0)
                losses = settings.get("losses", 0)
                ties = settings.get("ties", 0)
                record = f"{wins}-{losses}-{ties}"

                # Categorize players based on position
                quarterbacks = []
                runningbacks = []
                wide_receivers = []
                tight_ends = []
                players = current_roster.get("players", [])
                if players is None:
                    players = []
                for player_id in players:
                    player = player_data.get(player_id)
                    if player:
                        player_name = player["full_name"]
                        position = player["position"]
                        if position == "QB":
                            quarterbacks.append(player_name)
                        elif position == "RB":
                            runningbacks.append(player_name)
                        elif position == "WR":
                            wide_receivers.append(player_name)
                        else:
                            tight_ends.append(player_name)

                # Create a new roster object with the gathered data
                new_roster = {
                    "league_name": league_name,
                    "total_teams": total_teams,
                    "ppr": ppr,
                    "starters": starters,
                    "tep": tep,
                    "qb": qb,
                    "players": {
                        "quarterbacks": quarterbacks,
                        "runningbacks": runningbacks,
                        "widereceivers": wide_receivers,
                        "tightends": tight_ends,
                        "draftpicks": draft_picks,
                    },
                    "record": record,
                }

                # Add the new roster to the list of roster objects
                roster_object_list.append(new_roster)

    # Return the list of roster objects
    return roster_object_list