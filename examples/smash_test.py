from liquipediapy import smash
import json
# smash_wiki = smash('appname', "F:\\Path\\To\\Folder\\")
smash_wiki = smash('appname')
players = smash_wiki.get_players()

teams = smash_wiki.get_teams()

Armada_details = smash_wiki.get_player_info('Armada', True)

T1_details = smash_wiki.get_team_info('T1')
