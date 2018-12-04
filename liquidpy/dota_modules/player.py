import re
from urllib.request import quote



class dota_player():

	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'
		self.__player_exceptions = ['Fade','ghost','Ice','Lance','Ms','Net','Panda','shadow','Sky']


	def get_player_infobox(self,soup):
		player = {}
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')		
			if 'PlayerImagePlaceholder' not in image_url:
				player['image'] = self.__image_base_url+image_url
		except AttributeError:
			player['image'] = ''		

		info_boxes = soup.find_all('div', class_='infobox-cell-2')
		for i in range(0,len(info_boxes),2):
			attribute = info_boxes[i].get_text().replace(':','')
			if attribute == 'Country':
				player['country'] = info_boxes[i+1].get_text().split()
			elif attribute == 'Alternate IDs':	
				player['ids'] = info_boxes[i+1].get_text().split(',')
			elif attribute == 'Birth':
				player['birth_details'] = info_boxes[i+1].get_text().replace('\xa0','')
			elif attribute == 'Approx. Total Earnings':
				player['earnings'] = int(info_boxes[i+1].get_text().replace('$','').replace(',',''))
			elif attribute == "Pro Circuit Rank":
				ranking = {}
				ranking_list = info_boxes[i+1].get_text().replace('\xa0',' ').split()	
				ranking['rank'] = ranking_list[0].replace('#','')
				ranking['points'] = int(ranking_list[1].replace('(', '').replace(')', '').split(',')[0])
				player['ranking'] = ranking
			elif attribute == "Signature Hero":
				player_heros = []
				heros = info_boxes[i+1].find_all('a')
				for hero in heros:
					player_heros.append(hero.get('title'))
				player['signature_heros'] = player_heros	
			elif attribute == "Role(s)":
				player_roles = []
				roles = info_boxes[i+1].find_all('a')
				for role in roles:
					text = role.get_text()
					if len(text) > 0:
						player_roles.append(text)
				player['roles'] = player_roles
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

	#not perfectly found	
	def get_player_history(self,soup):
		player_history = []
		histories = soup.find_all('div', class_='infobox-center')
		try:
			histories = histories[-1].find_all('div', recursive=False)
		except IndexError:	
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
		rows = soup.find_all('tr')
		rows = [row for row in rows if len(row)>10]
		if len(rows) == 0:
			return achivements
		indexes = rows[0]	
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(cell.get_text().rstrip())
		rows = rows[1:]
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
					elif key == "LP Tier":	
						value = cells[i].find('a').get_text().rstrip()
					elif value == '':
						value = cells[i].find('a').get('title')
					elif key == "Results":
						value = cells[i].get_text()
				except (AttributeError,IndexError):
					pass	
				else:
					value = value.replace('\xa0','').rstrip()			
					achivement[key] = value
			if len(achivement) > 0:		
				achivements.append(achivement)

		return achivements	

	def process_playerName(self,playerName):
		if playerName in self.__player_exceptions:
			playerName = playerName+"_(player)"
		if not playerName[0].isdigit():
			playerName = list(playerName)
			playerName[0] = playerName[0].upper()
			playerName = "".join(playerName)	
		playerName = quote(playerName)

		return playerName		
				