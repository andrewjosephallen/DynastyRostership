import requests


# Function to get draft picks for a given league, roster, and league name
def get_draft_picks(league_id, roster_id, league_name):
    # List of original picks (3 years out, only 1st and 2nd rounders)
    original_picks = [
        "Round 1 2024",
        "Round 2 2024",
        "Round 1 2025",
        "Round 2 2025",
        "Round 1 2026",
        "Round 2 2026",
    ]

    # URL to fetch traded picks for the given league
    draft_picks_url = f"https://api.sleeper.app/v1/league/{league_id}/traded_picks"
    response = requests.get(draft_picks_url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the JSON data
    draft_picks_data = response.json() if response.content else []

    # Process each draft pick in the data
    for draft_pick in draft_picks_data:
        # Skip picks beyond the 2nd round
        if draft_pick["round"] > 2:
            continue

        draft_pick_string = f"Round {draft_pick['round']} {draft_pick['season']}"

        if draft_pick["roster_id"] != draft_pick["owner_id"]:
            if draft_pick["roster_id"] == roster_id:
                # Traded away this pick
                if draft_pick_string in original_picks:
                    original_picks.remove(draft_pick_string)
            elif draft_pick["owner_id"] == roster_id:
                # Traded for this pick
                if draft_pick_string not in original_picks:
                    original_picks.append(draft_pick_string)

    # Sort the list of picks
    original_picks.sort()

    # Return the sorted list of draft picks
    return original_picks