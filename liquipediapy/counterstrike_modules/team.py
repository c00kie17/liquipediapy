from urllib.request import quote
import re
import itertools
import unicodedata

class cs_team():


	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'

	def process_teamName(self,teamName):
		teamName = teamName.replace(" ","_")
		teamName = quote(teamName)

		return teamName

	def get_team_infobox(self,soup):
		team = {}
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')	
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
			elif attribute == "Games":
				games = []
				game_values = info_boxes[i+1].find_all('i')	
				for game in game_values:
					games.append(game.get_text())
				team['games'] = games				
			else:
				team[attribute.lower()] = unicodedata.normalize("NFKD",info_boxes[i+1].get_text())


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


	def get_team_roster(self,soup):
		roster = soup.find(
			"table",class_="wikitable wikitable-striped sortable"
		).find("tbody")
		rows = roster.find_all("tr")
		players = []
		for tag in rows:
			player = {}
			try:
				player["Country"] = tag.find("span", class_="flag").a["title"]
				player["ID"] = (
					tag.find(
						"span", attrs={"style": "white-space: pre"}
					).a["title"]
				)
				player["Name"] = (
					tag.find(
						"td", attrs={"style": "text-indent:4px"}
					).get_text()
					.strip()
				)
				player["Join Date"] = (
					tag.find(
						"td", attrs={"align": "center", "style": "font-style:italic"}
					).get_text()
					.split()[0]
				)
				players.append(player)
			except AttributeError:
				pass

		return players


	def get_team_achivements(self,soup):
		achivements = []
		rows = soup.find_all("tr")
		for row in rows:
			try:
				if len(row)>8:
					match = {}
					attrs = {"style": "text-align:left"}
					icon = "results-team-icon"

					match["Date"] = row.find("td").get_text()
					place = row.find(
						"b", attrs={"style": "white-space:nowrap"}
					).get_text()
					match["Placement"] = re.sub("[A-Za-z]", "", place) 
					match["Tier"] = row.find("a").get_text()
					match["Type"] = row.find_all("td")[3].get_text()
					match["game"] = row.find_all("a")[1]["title"]
					try:
						match["Tournament"] = row.find("td", attrs).get_text()
					except AttributeError:
						match["Tournament"] = row.find(
							"td", attrs={"style": "text-align:left;"}
						).get_text()
					match["Results"] = row.find(
						"td", class_="results-score"
					).get_text()
					try:
						match["opponent"] = row.find(
							"td", class_=icon
						).find("a")["title"] 
					except TypeError:
						try:
							match["opponent"] = row.find(
								"td", class_=icon
							).find("abbr")["title"]
						except:
							match["opponent"] = ""
					match["Prize"] = row.find_all("td")[-1].get_text()

					for key, value in match.items():
						match[key] = unicodedata.normalize("NFKD", value).rstrip()

					match["Placement"] = match["Placement"].replace(" ", "")
					match["Results"] = match["Results"].replace(" ", "")

					achivements.append(match)
			except AttributeError:
				pass

		return achivements

