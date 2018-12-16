import re
from urllib.request import quote
import unicodedata


class cs_player():

	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'
		self.__player_exceptions = []

	def process_playerName(self,playerName):
		if playerName in self.__player_exceptions:
			playerName = playerName+"_(player)"
		if not playerName[0].isdigit():
			playerName = list(playerName)
			playerName[0] = playerName[0].upper()
			playerName = "".join(playerName)	
		playerName = quote(playerName)

		return playerName		
	
	def get_player_infobox(self,soup):
		player = {}
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')		
			if 'PlayerImagePlaceholder' not in image_url:
				player['image'] = self.__image_base_url+image_url
			else:
				player['image'] = ''	
		except AttributeError:
			player['image'] = ''		

		try:	
			info_boxes = soup.find_all('div', class_='infobox-cell-2')
		except AttributeError:
			return player	
		for i in range(0,len(info_boxes),2):
			attribute = info_boxes[i].get_text().replace(':','')
			if attribute == 'Country':
				player_countries = []
				countries = info_boxes[i+1].find_all('a')
				for country in countries:
					player_countries.append(country.get_text())
				player_countries = [country for country in player_countries if len(country)>0]	
				player['countries'] = player_countries
			elif attribute == 'Birth':
				player['birth_details'] = unicodedata.normalize("NFKD",info_boxes[i+1].get_text())
			elif attribute == 'Approx. Total Winnings':
				player['earnings'] = int(info_boxes[i+1].get_text().replace('$','').replace(',','').replace('.',''))
			elif attribute == "Roles":
				player_roles = []
				roles = info_boxes[i+1].find_all('a')
				for role in roles:
					text = role.get_text()
					if len(text) > 0:
						player_roles.append(text)
				player['roles'] = player_roles
			elif attribute == "Games":
				games = []
				game_values = info_boxes[i+1].find_all('i')	
				for game in game_values:
					games.append(game.get_text())
				player['games'] = games	
			else:
				attribute = attribute.lower().replace('(', '').replace(')', '').replace(' ','_')
				player[attribute] = info_boxes[i+1].get_text().rstrip()
	
		return player

	def get_player_links(self,soup):
		player_links = {}
		try:		
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return player_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[-2].replace('https://','').replace('http://','')
			player_links[site_name] = link.get('href')

		return player_links	

	def get_player_history(self,soup):
		player_history = []
		histories = soup.find_all('div', class_='infobox-center')
		try:
			histories = histories[-1].find_all('div', recursive=False)
		except (IndexError,AttributeError):	
			return player_history
		for history in histories:
			teams_info = history.find_all('div')
			if len(teams_info) > 1:
				team = {}
				team['duration'] = teams_info[0].get_text()
				team['name'] = teams_info[1].get_text()
				player_history.append(team)

		return player_history
		
	def get_player_achivements(self,soup):
		achivements = []
		try:
			rows = soup.find('table',class_='table-striped').find_all('tr')
		except AttributeError:
			return achivements
		rows = [row for row in rows if len(row)>10]
		if len(rows) == 0:
			return achivements
		indexes = rows[0]	
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(cell.get_text().rstrip())
		rows = rows[1:]
		index_values.insert(3,'game')
		index_values.insert(-1,'opponent')
		for row in rows:
			achivement={}
			cells = row.find_all('td')
			for i in range(0,len(cells)):
				try:
					key = index_values[i]
					value = cells[i].get_text().rstrip()
					if key == "Date":
						value = cells[i].find(text=True)
					elif key == "Placement":
						value = re.sub('[A-Za-z]','',cells[i].get_text())
					elif key == "Tier":	
						value = cells[i].find('a').find(text=True).rstrip()
					elif value == '':
						value = cells[i].find('a').get('title')
					elif key == "Results":
						value = cells[i].get_text()
				except (AttributeError,IndexError):
					pass	
				else:
					value = unicodedata.normalize("NFKD",value.rstrip())					
					achivement[key] = value
			if len(achivement) > 0:		
				achivements.append(achivement)

		return achivements	

	def get_player_hardware(self,soup):
		hardware = {}
		try:
			soup.find('table',class_='mw-collapsible').decompose()
		except AttributeError:
			return hardware
		tables = soup.find_all('table',class_='wikitable')
		tables = [table for table in tables if len(table.find_all('tr')) > 1 ]
		hardware['hardware'] = {}
		for table in tables:
			rows = table.find_all('tr')
			if len(rows) > 3:
				header = unicodedata.normalize("NFKD",rows[0].get_text().split()[0])
				indexes = []
				header_datas = rows[1].find_all('th')
				for data in header_datas:
					indexes.append(unicodedata.normalize("NFKD",data.get_text().rstrip()))	
				info_datas = rows[2].find_all('td')
				table_data = {}
				for i in range(0,len(info_datas)):
					try:
						table_data[indexes[i]] = unicodedata.normalize("NFKD",info_datas[i].get_text().rstrip())
					except IndexError:
						continue	
				hardware[header] = table_data
			elif len(rows) <= 3:
				header_datas = rows[0].find_all('th')
				indexes = []
				for data in header_datas:
					indexes.append(unicodedata.normalize("NFKD",data.get_text().rstrip()))	
				info_datas = rows[1].find_all('td')
				j = 0
				for i in range(0,len(info_datas)):
					if len(info_datas[i].get_text().rstrip()) == 0:
						i = i + 1
						continue
					hardware['hardware'][indexes[j]] = unicodedata.normalize("NFKD",info_datas[i].get_text().rstrip())
					j = j + 1
		
		return hardware		

						

