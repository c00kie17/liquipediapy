from urllib.request import quote
import re
import itertools
import unicodedata


class smash_team():
	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'

	def process_teamName(self, teamName):
		teamName = teamName.replace(" ", "_")
		teamName = quote(teamName)
		return teamName

	def get_team_infobox(self, soup):
		team = {}
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')
			team['image'] = self.__image_base_url + image_url
		except AttributeError:
			team['image'] = ''
		info_boxes = soup.find_all('div', class_='infobox-cell-2')
		for i in range(0, len(info_boxes), 2):

			attribute = info_boxes[i].get_text().replace(':', '')
			if attribute == "Sponsor" or attribute == "Location":
				value_list = []
				values = info_boxes[i + 1].find_all('a')
				for value in values:
					text = value.get_text()
					if len(text) > 0:
						value_list.append(text)
				team[attribute.lower()] = value_list
			elif attribute == "Total Earnings":
				team['earnings'] = (
					int(info_boxes[i + 1].get_text().replace('$', '').replace(',', ''))
				)
			elif attribute == "Games":
				games = []
				game_values = info_boxes[i + 1].find_all('i')
				for game in game_values:
					games.append(game.get_text())
				team['games'] = games
			else:
				team[attribute.lower()] = (
					unicodedata.normalize("NFKD", info_boxes[i + 1].get_text())
				)
		return team

	def get_team_links(self, soup):
		team_links = {}
		try:
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return team_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[0].replace('https://', '').replace('http://', '')
			team_links[site_name] = link.get('href')

		return team_links

	def get_team_roster(self, soup):
		rosters = soup.find_all(
			"table", class_="wikitable-striped"
		)
		rosters = [c for c in rosters if 'roster-card' not in c.attrs['class']]

		players = []
		for roster in rosters:
			body = roster.find('tbody')
			rows = body.find_all("tr")
			rows = rows[2:]  # Skip headers
			assert len(rows) > 0, "We should always have at least one row"
			for i, row in enumerate(rows):
				player = {}
				try:
					player["Country"] = row.find("span", class_="flag").a["title"]
				except AttributeError:
					pass
				try:
					player["ID"] = (
						row.find(
							"span", attrs={"style": "white-space: pre"}
						).a.get_text()
					)
				except AttributeError:
					pass
				try:
					player["Name"] = (
						row.find(
							"i"
						).get_text()
						.strip()
					)
				except AttributeError:
					pass
				try:
					player["Main"] = (
						[i["title"] for i in row.find_all("img") if "title" in i.attrs.keys()]
					)
				except AttributeError:
					pass
				try:
					player["Join Date"] = (
						row.find_all(
							"i", text=re.compile(r'^[0-9]{4}-{1}[0-9]{2}-{1}[0-9]{2}$')
						)[-1].get_text()
					)
				except AttributeError:
					pass
				try:
					player["Leave Date"] = (
						row.find(
							"td", attrs={"align": "center", "style": "font-style:italic"}
						).get_text()
					)
				except AttributeError:
					pass
				players.append(player)

		return players

	def get_team_org(self, soup):
		rosters = soup.find_all(
			"table", class_="wikitable-striped"
		)
		rosters = [c for c in rosters if 'roster-card' in c.attrs['class']]

		orgs = []
		for roster in rosters:
			body = roster.find('tbody')
			rows = body.find_all("tr")
			rows = rows[2:]  # Skip headers
			assert len(rows) > 0, "We should always have at least one row"

			for i, row in enumerate(rows):
				org = {}
				try:
					org["Country"] = row.find("span", class_="flag").a["title"]
				except AttributeError:
					pass
				try:
					org["ID"] = (
						row.find(
							"td", class_="ID"
						).find_all('a')[-1].get_text()
					)
				except AttributeError:
					pass
				try:
					org["Name"] = (
						row.find(
							"td", class_="Name"
						).get_text()
						.strip()
						.replace('(', '')
						.replace(')', '')
					)
				except AttributeError:
					pass
				try:
					org["Join Date"] = (
						row.find(
							"div", class_='Date'
						).get_text()
					)
				except AttributeError:
					pass
				try:
					org["Leave Date"] = (
						row.find(
							"td", attrs={"align": "center", "style": "font-style:italic"}
						).get_text()
					)
				except AttributeError:
					pass

				try:
					org["Position"] = (
						row.find(
							"td", class_="PositionWoTeam2").get_text()
					)
				except AttributeError:
					pass
				orgs.append(org)

		return orgs
