from liquidpy import dota

dota_obj = dota("appname")

print(dota_obj.get_players())

print(dota_obj.get_player_info('Miracle-',True))

print(dota_obj.get_team_info('Team Liquid',True))

print(dota_obj.get_transfers())	

print(dota_obj.get_upcoming_and_ongoing_games())

print(dota_obj.get_heros())

print(dota_obj.get_items())

print(dota_obj.get_patches())

print(dota_obj.get_tournaments())

print(dota_obj.get_pro_circuit_details())