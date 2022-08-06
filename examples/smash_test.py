from liquipediapy import smash

# smash_wiki = smash('appname', "F:\\Path\\To\\debug.ini")
smash_wiki = smash('appname')
players = smash_wiki.get_players()

teams = smash_wiki.get_teams()

MKLeo_details = smash_wiki.get_player_info('MKLeo', True)
