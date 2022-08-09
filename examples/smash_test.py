from liquipediapy import smash

# smash_wiki = smash('appname', "F:\\Path\\To\\Folder\\")
# smash_wiki = smash('appname')
smash_wiki = smash('appname', debug_folder="F:\\Projets\\SBTV\\HTMLOutput\\")
# players = smash_wiki.get_players()

teams = smash_wiki.get_teams()

Armada_details = smash_wiki.get_player_info('Armada', True)
