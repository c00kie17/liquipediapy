from liquipediapy import Dota

dota_obj = Dota("appname")

# players = dota_obj.get_players()

# player_details = dota_obj.get_player_info("Miracle-", False)

# teams = dota_obj.get_teams()

# teams_disbanded = dota_obj.get_teams(True)

team_details = dota_obj.get_team_info("Team Liquid", False)
print(team_details)

# transfers = dota_obj.get_transfers()

# games = dota_obj.get_upcoming_and_ongoing_games()

# heros = dota_obj.get_heros()
# print(heros)

# items = dota_obj.get_items()
# print(items)

# patches = dota_obj.get_patches()
# print(patches)

# tournaments = dota_obj.get_tournaments()

# pro_circuit_details = dota_obj.get_pro_circuit_details()
