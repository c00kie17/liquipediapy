from urllib.request import quote
import re
import itertools
import unicodedata

class dota_team():


	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'

	def process_teamName(self,teamName):
		teamName = teamName.replace(" ","_")
		teamName = quote(teamName)

		return teamName

	def get_team_infobox(self,soup):
		team = {}
		try:
			image_url = soup.find('div', class_='img-responsive').find('img').get('src')	
			team['image'] = self.__image_base_url+image_url
		except AttributeError:
			team['image'] = ''			
		info_boxes = soup.find_all('div', class_='infobox-cell-2')
		for i in range(0,len(info_boxes),2):
			attribute = info_boxes[i].get_text().replace(':','')
			if attribute == "Sponsor" or attribute == "Location":
				value_list = []
				values = info_boxes[i+1].find_all('a')
				for value in values:
					text = value.get_text()
					if len(text) > 0:
						value_list.append(text)
				team[attribute.lower()] = value_list
			elif attribute == "Total Earnings":
				team['earnings'] = int(info_boxes[i+1].get_text().replace('$','').replace(',',''))
			# not available now
			#elif attribute == "Pro Circuit Rank":
			#	ranking = {}
			#	ranking_list = unicodedata.normalize("NFKD",info_boxes[i+1].get_text()).split()
			#	ranking['rank'] = ranking_list[0].replace('#','')
			#	ranking['points'] = int(ranking_list[1].replace('(', '').replace(')', '').split(',')[0])
			#	team['ranking'] = ranking			
			else:
				team[attribute.lower()] = unicodedata.normalize("NFKD",info_boxes[i+1].get_text().strip())


		return team

	def get_team_links(self,soup):
		team_links = {}
		try:		
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return team_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[-2].replace('https://','')
			team_links[site_name] = link.get('href')

		return team_links

	def get_team_cups(self,soup):
		team_cups = []
		info_boxes = soup.find_all('div',class_='infobox-center')
		cups = []
		for boxes in info_boxes:
			cups.append(boxes.find_all('span',class_='league-icon-small-image'))
		cups = list(itertools.chain.from_iterable(cups))
		for cup in cups:
			try:
				league = cup.find('a').get('title')
				team_cups.append(league)
			except AttributeError:
				pass	

		return team_cups

	def get_team_roster(self,soup):
		roster_cards = soup.find_all('table',class_='roster-card')
		team_roster = roster_cards[0]
		rows = team_roster.find_all('tr')
		indexes = rows[1]
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(unicodedata.normalize("NFKD",cell.get_text().rstrip()))	
		rows = rows[2:]
		players = []
		for row in rows:
			player={}
			cells = row.find_all('td')
			for i in range(0,len(cells)):
				key = index_values[i]
				value = cells[i].get_text().strip()
				if key == "Name":
					value = value.replace('(','').replace(')','')
				elif key == "Join Date":
					value = cells[i].find('div',class_="Date").find(text=True)	
				elif key == "Position":
					value = value.split()[-1]
				value = unicodedata.normalize("NFKD",value.rstrip())	
				if len(key) > 0:
					player[key] = value
			players.append(player)	
		return players
	
	def get_team_achivements(self,soup):
		achivements = []
		rows = soup.find_all('tr')
		rows = [row for row in rows if len(row)>10]
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
				key = index_values[i]
				value = cells[i].get_text().rstrip()
				try:	
					if key == "Placement":
						value = re.sub('[A-Za-z]','',cells[i].get_text())
					elif key == "LP Tier":
						value = cells[i].find('a').get_text().rstrip()
					elif value == '':
						try:
							value = cells[i].find('a').get('title')
						except AttributeError:
							pass	
					elif key == "Results":
						value = cells[i].get_text()
				except AttributeError:
					pass		
				value = unicodedata.normalize("NFKD",value.rstrip())	
				achivement[key] = value
			achivements.append(achivement)

		return achivements

		



					

