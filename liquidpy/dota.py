import requests
import liquidpy.exceptions as ex
from liquidpy.liquidpy import liquidpy
from bs4 import BeautifulSoup
import re
from liquidpy.dota_modules.player import dota_player
from liquidpy.dota_modules.team import dota_team
from liquidpy.dota_modules.pro_circuit import dota_pro_circuit


class dota():

	def __init__(self,appname):
		self.appname = appname
		self.liquipedia = liquidpy(appname)
		self.__image_base_url = 'https://liquipedia.net'
		


	def get_players(self):
		soup,__ = self.liquipedia.parse('Players_(all)')
		rows = soup.findAll('tr')
		indexes = rows[0]
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(cell.get_text().rstrip())
		players = []
		for row in rows:
			if len(row) > 3:
				player={}
				cells = row.find_all('td')
				for i in range(0,len(cells)):
					key = index_values[i]
					if key == '':
						key = "country"
						value = cells[i].find('a').get('title')
					elif key == "Links":
						player_links = {}
						links = cells[i].find_all('a')
						for link in links:
							link_list = link.get('href').split('.')
							site_name = link_list[-2].replace('https://','').replace('http://','')
							player_links[site_name] = link.get('href')
						value = player_links	
					else:
						value = cells[i].get_text().rstrip()	
					player[key] = value
				if len(player) > 0:
					players.append(player)

		return players
	
	def get_player_info(self,playerName,results=False):
		player_object = dota_player()
		playerName = player_object.process_playerName(playerName)		
		soup,redirect_value = self.liquipedia.parse(playerName)
		if redirect_value is not None:
			playerName = redirect_value
		player = {}
		player['info'] = player_object.get_player_infobox(soup)
		player['links'] = player_object.get_player_links(soup)
		player['history'] = player_object.get_player_history(soup)
		player['achivements'] = player_object.get_player_achivements(soup)
		if results:
			parse_value = playerName + "/Results"
			try:
				soup,__ = self.liquipedia.parse(parse_value)
			except ex.RequestsException:
				player['results'] = []
			else:	
				player['results'] = player_object.get_player_achivements(soup)

		return player

	def get_team_info(self,teamName,results=False):
		team_object = dota_team()
		teamName = team_object.process_teamName(teamName)	
		soup,redirect_value = self.liquipedia.parse(teamName)
		if redirect_value is not None:
			teamName = redirect_value
		team = {}	
		team['info'] = team_object.get_team_infobox(soup)
		team['links'] = team_object.get_team_links(soup)
		team['cups'] = team_object.get_team_cups(soup)
		team['team_roster'] = team_object.get_team_roster(soup)
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
		indexes = soup.find('div',class_='divHeaderRow')
		index_values = []
		for cell in indexes.find_all('div'):
			index_values.append(cell.get_text())
		rows = soup.find_all('div',class_='divRow')
		for row in rows:
			transfer = {}
			cells = row.find_all('div',class_='divCell')
			for i in range(0,len(cells)):
				key = index_values[i]
				value = cells[i].get_text()
				if key == "Player":
					value = [val for val in value.split(' ') if len(val) > 0]
				if key == "Previous" or key == "Current":
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
		soup,__ = self.liquipedia.parse('Liquipedia:Upcoming_and_ongoing_matches')
		matches = soup.find_all('table',class_='infobox_matches_content')
		for match in matches:
			game = {}
			cells = match.find_all('td')
			try:
				game['team1'] = cells[0].find('span',class_='team-template-image').find('a').get('title')			
				game['format'] = cells[1].find('abbr').get_text()
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

	def get_heros(self):
		heros = []	
		soup,__ = self.liquipedia.parse('Portal:Heroes')
		list_elements = soup.find_all('li')
		for list_element in list_elements:
			hero = {}
			try:
				hero['image'] = self.__image_base_url + list_element.find('img').get('src')
				hero['name'] = list_element.find('span').get_text()
				heros.append(hero)
			except AttributeError:
				pass

		return	heros

	def get_items(self):
		items = []							
		soup,__ = self.liquipedia.parse('Portal:Items')
		item_divs = soup.find_all('div',class_='responsive')
		for item_div in item_divs:
			item = {}
			item['image'] = self.__image_base_url + item_div.find_all('img')[0].get('src')
			item['name'] = item_div.find_all('a')[1].get_text()
			try:
				item['price'] = item_div.find('b').get_text()
			except AttributeError:
				pass	
			items.append(item)	

		return items

	def get_patches(self):
		patches = []
		soup,__ = self.liquipedia.parse('Portal:Patches')
		tables = soup.find_all('table')	
		for table in tables:
			rows = table.find('tbody').find_all('tr')
			indexes = rows[0]
			index_values = []
			for cell in indexes.find_all('td'):
				index_values.append(cell.get_text().rstrip())
			rows = rows[1:]
			for row in rows:
				patch = {}
				cells = row.find_all('td')
				for i in range(0,len(cells)):
					key = index_values[i]
					value = cells[i].get_text().rstrip()
					if key == "Highlights":
						value = [val.replace('\xa0','') for val in cells[i].get_text().split('\n') if len(val) > 0]
					patch[key] = value
				patches.append(patch)

		return patches		
		
			
	def get_tournaments(self,tournamentType=None):
		tournaments = []
		if tournamentType is None:
			page_val = 'Portal:Tournaments'
		else:
			page_val = tournamentType.capitalize()+'_Tournaments'				
		soup,__ = self.liquipedia.parse(page_val)
		div_rows = soup.find_all('div',class_='divRow')
		for row in div_rows:
			tournament = {}

			values = row.find('div',class_="Tournament").get_text().split('\n')
			tournament['tier'] = re.sub('\W+',' ',values[0]).strip()
			tournament['name'] = values[1]

			try:
				tournament['icon'] = self.__image_base_url+row.find('div',class_="Tournament").find('img').get('src')
			except AttributeError:
				pass	

			tournament['dates'] = row.find('div',class_="Date").get_text()

			try:
				tournament['prize_pool'] = int(row.find('div',class_="Prize").get_text().rstrip().replace('$','').replace(',',''))
			except (AttributeError,ValueError):
				tournament['prize_pool'] = 0

			tournament['teams'] = re.sub('[A-Za-z]','',row.find('div',class_="PlayerNumber").get_text()).rstrip()	
			location_list= row.find('div',class_="Location").get_text().replace('\xa0','').rstrip().split(',')	
			tournament['host_location'] = location_list[0]

			try:
				tournament['event_location'] = location_list[1]
			except IndexError:
				pass	
		
			if len(row) < 15:
				links_a = row.find('div',class_="SecondPlace").find_all('a')
				tournament['links'] = []
				for link in links_a:
					link_list = link.get('href').split('.')
					site_name = link_list[-2].replace('https://','')
					tournament['links'].append({site_name:link.get('href')})
			else:
				tournament['winner'] = 	row.find('div',class_="FirstPlace").get_text().replace('\xa0','').rstrip()	
				tournament['runner_up'] = 	row.find('div',class_="SecondPlace").get_text().replace('\xa0','').rstrip()	

			tournaments.append(tournament)

		return tournaments	

	def get_pro_circuit_details(self):
		soup,__ = self.liquipedia.parse('Dota_Pro_Circuit/2018-19/Rankings/Full')
		pro_circuit = {}
		circuit_object = dota_pro_circuit()
		pro_circuit['rankings'] = circuit_object.get_rankings(soup)
		soup,__ = self.liquipedia.parse('Dota_Pro_Circuit/2018-19/Schedule')
		pro_circuit['schedule'] = circuit_object.get_schedule(soup)


		return pro_circuit
	


	