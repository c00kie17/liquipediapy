import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
import re
import unicodedata
from liquipediapy.counterstrike_modules.player import cs_player
from liquipediapy.counterstrike_modules.team import cs_team
import itertools
from urllib.request import quote


class counterstrike():

	def __init__(self,appname):
		self.appname = appname
		self.liquipedia = liquipediapy(appname,'counterstrike')
		self.__image_base_url = 'https://liquipedia.net'

	def get_players(self):
		regions = ['Europe','CIS','Americas','Oceania','Eastern_&_Southern_Asia','Africa_&_Middle_East']
		players = []
		for region in regions:			
			soup,__ = self.liquipedia.parse('Portal:Players/'+quote(region))		
			rows = soup.find_all('td')
			for row in rows:
				player = {}
				name_list = row.get_text().split('-')
				player['id'] = name_list[0].replace(' ','')
				player['name'] = name_list[1].replace(' ','')
				player['country'] = row.find('a').get('title')
				try:
					team = row.find('span',class_='team-template-image').find('a').get('title')
				except AttributeError:
					team = ''
				player['team'] = team
				players.append(player)	

		return players

	def get_teams(self,region):
		if 'cis' in region:
			region = region.upper()
		else:
			region = region.capitalize()	
		soup,__ = self.liquipedia.parse('Portal:Teams/'+region)
		teams = []
		tables = soup.find_all('table',class_='collapsible')
		for table in tables:
			team = {}
			soup.find('tr',class_='mw-empty-elt').decompose()
			rows = table.find_all('tr')
			header = rows[0]
			team['name'] = header.find('span',class_='team-template-text').get_text()
			team['logo'] = self.__image_base_url+header.find('span',class_='team-template-image').find('img').get('src')
			team['playes'] = []
			rows = rows[2:]
			for row in rows:		
				player = {}
				data = row.find_all('td')
				links = data[0].find_all('a')
				player['country'] = links[0].get('title')
				try:
					player_id = links[1].get_text()
				except IndexError:
					player_id = data[0].get_text()
				player['id'] = unicodedata.normalize("NFKD",player_id)		
				player['name'] = data[1].get_text()
				team['playes'].append(player)
			teams.append(team)	

		return teams

	def get_player_info(self,playerName,results=False):
		player_object = cs_player()
		playerName = player_object.process_playerName(playerName)		
		soup,redirect_value = self.liquipedia.parse(playerName)
		if redirect_value is not None:
			playerName = redirect_value
		player = {}
		player['info'] = player_object.get_player_infobox(soup)
		player['links'] = player_object.get_player_links(soup)
		player['history'] = player_object.get_player_history(soup)
		player['achivements'] = player_object.get_player_achivements(soup)
		player['gear_settings'] = player_object.get_player_hardware(soup)
		if results:
			parse_value = playerName + "/Results"
			try:
				soup,__ = self.liquipedia.parse(parse_value)
			except ex.RequestsException:
				player['results'] = []
			else:	
				player['results'] = player_object.get_player_achivements(soup)

		return player

	def get_team_info(self,teamName,results=True):
		team_object = cs_team()
		teamName = team_object.process_teamName(teamName)	
		soup,redirect_value = self.liquipedia.parse(teamName)
		if redirect_value is not None:
			teamName = redirect_value
		team = {}
		team['info'] = team_object.get_team_infobox(soup)	
		team['links'] = team_object.get_team_links(soup)
		team['team_roster'] = team_object.get_team_roster(soup)
		team['achivements'] = team_object.get_team_achivements(soup)
		if results:
			parse_value = teamName + "/Results"
			try:
				soup,__ = self.liquipedia.parse(parse_value)
			except ex.RequestsException:
				team['results'] = []
			else:	
				team['results'] = team_object.get_team_achivements(soup)
		return team

	def get_transfers(self):
		transfers = []
		soup,__ = self.liquipedia.parse('Portal:Transfers')
		index_values = []
		header_row = soup.find('div',class_='divHeaderRow')
		cells = header_row.find_all('div',class_='divCell')
		for cell in cells:
			index_values.append(cell.get_text().strip())
		rows = soup.find_all('div',class_='divRow')	
		for row in rows:
			transfer = {}
			cells = row.find_all('div',class_='divCell')
			for i in range(0,len(cells)):
				key = index_values[i]
				value = cells[i].get_text()
				if key == "Player":
					value = [val for val in value.split(' ') if len(val) > 0]
				if key == "Old" or key == "New":
					try:
						value = cells[i].find('a').get('title')	
					except	AttributeError:
						value = "None"
				transfer[key] = value
			transfer = {k: v for k, v in transfer.items() if len(k) > 0}	
			transfers.append(transfer)	

		return transfers

	def get_upcoming_and_ongoing_games(self):
		games = []
		soup,__ = self.liquipedia.parse('Liquipedia:Matches')
		matches = soup.find_all('table',class_='infobox_matches_content')
		for match in matches:
			game = {}
			cells = match.find_all('td')
			try:
				game['team1'] = cells[0].find('span',class_='team-template-image').find('a').get('title')			
				game['team2'] = cells[2].find('span',class_='team-template-image').find('a').get('title')
				game['start_time'] = cells[3].find('span',class_="timer-object").get_text()
				game['tournament'] = cells[3].find('div').get_text().rstrip()
				try:
					game['twitch_channel'] = cells[3].find('span',class_="timer-object").get('data-stream-twitch')
				except AttributeError:
					pass
				games.append(game)	
			except AttributeError:
				continue		
					
		return games

	def get_tournaments(self,tournamentType=None):
		tournaments = []
		if tournamentType is None:
			page_val = 'Portal:Leagues'
		else:
			page_val = tournamentType.capitalize()+'_Tournaments'				
		soup,__ = self.liquipedia.parse(page_val)
		tables = soup.find_all('div',class_='divTable')
		for table in tables:
			rows = table.find_all('div',class_='divRow')
			for row in rows:
				tournament = {}
				tournament_cell = row.find('div',class_='Tournament')
				tournament['tier'] = tournament_cell.find('a').get_text()
				tournament['tournament'] = tournament_cell.find('b').get_text()
				tournament['date'] = row.find('div',class_='Date').get_text()
				tournament['prize'] = unicodedata.normalize("NFKD",row.find('div',class_='Prize').get_text().rstrip())
				team_no = unicodedata.normalize("NFKD",row.find('div',class_='PlayerNumber').get_text().rstrip()).split()
				tournament['teams_no'] = team_no[0]
				location = unicodedata.normalize("NFKD",row.find('div',class_='Location').get_text().rstrip()).split(',')
				try:
					tournament['host_locaion'] = location[1]
				except IndexError:	
					tournament['host_locaion'] = ''	
				tournament['event_locaion'] = location[0]

				placement = row.find_all('div',class_='Placement')
				if len(placement) > 1:
					try:
						tournament['first_place'] = row.find('div',class_='FirstPlace').find('span',class_='team-template-text').get_text()		
					except AttributeError:	
						tournament['first_place'] = 'TBD'

					try:
						tournament['second_place'] = row.find('div',class_='SecondPlace').find('span',class_='team-template-text').get_text()		
					except AttributeError:	
						tournament['second_place'] = 'TBD'
				else:
					teams = row.find('div',class_='Placement').find_all('span',class_='Player')
					qual_teams = []
					for team in teams:
						qual_teams.append(team.find('span',class_='team-template-text').get_text())
					
					tournament['qualified'] = qual_teams
						
				tournaments.append(tournament)

		return tournaments

	def get_weapons(self):
		soup,__ = self.liquipedia.parse('Portal:Weapons')
		weapons = []
		page_list = soup.find_all('li')
		for item in page_list:
			weapon = {}
			try:
				weapon['image'] = self.__image_base_url + item.find('img').get('src')
			except AttributeError:
				continue	
			weapon['name'] = item.get_text()
			weapons.append(weapon)
		return weapons	

	def get_weapon_info(self,weaponName):
		weapon = {}
		weaponName = weaponName.replace(' ','_')
		soup,__ = self.liquipedia.parse(weaponName)	
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')		
			if 'PlayerImagePlaceholder' not in image_url:
				weapon['image'] = self.__image_base_url+image_url
			else:
				weapon['image'] = ''	
		except AttributeError:
			weapon['image'] = ''		
		info_boxes = soup.find_all('div', class_='infobox-cell-2')
		for i in range(0,len(info_boxes),2):
			attribute = info_boxes[i].get_text().replace(':','')
			if attribute == "Side":
				weapon['side'] =  info_boxes[i+1].get_text().rstrip().split(',')
			else:	
				attribute = attribute.lower().replace('(', '').replace(')', '').replace(' ','_')
				weapon[attribute] = info_boxes[i+1].get_text().rstrip()

		return weapon

	def get_statistics(self):
		teams = []
		soup,__ = self.liquipedia.parse('Statistics/Total')				
		tables = soup.find_all('table',class_='wikitable')	
		for table in tables:
			index = []
			rows = table.find_all('tr')
			rows = rows[1:]
			for row in rows:
				team = {}
				data = row.find_all('td')
				team['name'] = data[0].get_text().rstrip()
				team['earnings'] = data[1].get_text().rstrip()
				medals = row.find_all('th')
				team['golds'] = medals[0].get_text().rstrip()
				team['silver'] = medals[1].get_text().rstrip()
				team['bronze'] = medals[2].get_text().rstrip()
				teams.append(team)

		return  teams 

	def get_patches(self):
		patches = []
		soup,__ = self.liquipedia.parse('Patches')	
		tables = soup.find_all('table',class_='wikitable')
		for table in tables:
			indexes=[]
			for header in table.find_all('th'):
				indexes.append(header.get_text().rstrip())
			rows = table.find_all('tr')
			rows = rows[1:]
			for row in rows:
				patch = {}
				cells = row.find_all('td')
				for i in range(0,len(cells)):
					key = indexes[i]
					if key == "Release Highlights":
						value = []
						release_list = cells[i].find_all('li')
						for release in release_list:
							value.append(release.get_text())	 
					else:	
						value = unicodedata.normalize("NFKD",cells[i].get_text().rstrip())
					patch[key] = value
				patches.append(patch)
		return patches			



						


	