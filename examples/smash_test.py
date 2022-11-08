from liquipediapy import smash
import json

# To turn on Debugger mode
# smash_wiki = smash('appname', "F:\\Path\\To\\Folder\\")
smash_wiki = smash('appname')

players = smash_wiki.get_players()

teams = smash_wiki.get_teams()

Armada_details = smash_wiki.get_player_info('Armada', True)

T1_details = smash_wiki.get_team_info('T1')

transfers = smash_wiki.get_transfers()

# Smash 64 With no extended infos by default
tournaments = smash_wiki.get_tournaments()

# All smashes + extended infos
tournaments = smash_wiki.get_tournaments(games=['64', 'Melee', 'Brawl', 'Project_M', 'Wii_U', 'Ultimate'], extended_infos= True)
