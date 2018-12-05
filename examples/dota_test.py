from liquidpy import dota

dota_obj = dota("appname")

players = dota_obj.get_players()

player_details = dota_obj.get_player_info('Miracle-',True)

team_details = dota_obj.get_team_info('Team Liquid',True)

transfers = dota_obj.get_transfers()

games = dota_obj.get_upcoming_and_ongoing_games()

heros = dota_obj.get_heros()

items = dota_obj.get_items()

patches = dota_obj.get_patches()

tournaments = dota_obj.get_tournaments()

pro_circuit_details = dota_obj.get_pro_circuit_details()