from getPlayerData import get_player_data
from setRostership import set_rostership
from setTeamRosters import set_team_rosters
import openpyxl

import datetime

# Prompt the user for their name
sleeper_username = input("Please enter your sleeper username: ")
# sleeper_username = "ajallen12"

current_date = datetime.date.today()  # Returns the current date in 'YYYY-MM-DD' format
formatted_date = current_date.strftime("%Y_%m_%d")  # Convert to 'YYYY_MM_DD' format
excel_name = f"{formatted_date}_sleeper_sync.xlsx"  # Use f-string for concatenation
workbook = openpyxl.Workbook()
print("Generating filename:", excel_name)  # For demonstration purposes

# Display a message using the input
player_data = get_player_data()
set_rostership(workbook, excel_name, sleeper_username, player_data)
set_team_rosters(workbook, excel_name, sleeper_username, player_data)

if "Sheet" in workbook.sheetnames:
    del workbook["Sheet"]
    workbook.save(excel_name)
print("Excel file created successfully.")


# function main() {
#   var masterSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Master");
#   var sleeperUsername = masterSheet.getRange('D4').getValue();
#   var playerData = getPlayerData();
#   setRostership(sleeperUsername, playerData);
#   setTeamRosters(sleeperUsername, playerData);
#   setCurrentDraftPicks(sleeperUsername);
# }
