import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
import re
from liquipediapy.smash_modules.player import smash_player
from liquipediapy.smash_modules.team import smash_team
import unicodedata
from urllib.request import quote


class smash():
	def __init__(self, appname: str, debug_folder: str = ""):
		self.appname = appname
		self.liquipedia = liquipediapy(appname, 'smash', debug_folder)
		self.__image_base_url = 'https://liquipedia.net'

	def get_players(self) -> list:
		regions = ['Americas', 'Europe', 'Asia/Oceania']
		games = ['64', 'Melee', 'Project_M', 'Brawl_WiiU_Ultimate']
		players = []

		asia_soup = None  # Asia/Oceania not handled the same way
		asia_pages = []
		for region in regions:
			# Asia/Oceania got all the games on the same page
			if region == 'Asia/Oceania':
				query = 'Players_' + '(' + quote(region) + ')'
				asia_soup, _ = self.liquipedia.parse(query)

				m_div = asia_soup.find('div', class_='tabs-content')
				asia_pages = m_div.find_all('div', class_=re.compile(r"^content[0-9]+$"))
				assert len(asia_pages) == len(games), \
					"get_players: numbers of game pages doesn't reflect number of games"

			for k, game in enumerate(games):
				if region != 'Asia/Oceania':
					query = 'Players_' + '(' + quote(region) + ')' + '/' + quote(game)
					soup, _ = self.liquipedia.parse(query)
				else:
					soup = asia_pages[k]

				cleared_game = game.replace('_', ' ')
				rows = soup.findAll('tr')
				indexes = rows[0]
				index_values = []
				for cell in indexes.find_all('th'):
					index_values.append(cell.get_text().strip())

				rows = rows[1:]
				for j, row in enumerate(rows):
					if len(row) >= 5:
						player = {}
						cells = row.find_all('td')
						for i in range(len(cells)):
							key = index_values[i]
							value = cells[i].get_text().strip()
							if key == 'ID':
								player['Country'] = cells[i].find('a').get('title')
							elif key == 'Main':
								value = [c.get('title') for c in cells[i].find_all('img')]
							elif key == 'Links':
								player_links = {}
								links = cells[i].find_all('a')
								for link in links:
									href = link.get('href')
									site = href.split('.')[-2]
									site = site.replace('https://', '').replace('http://', '')
									player_links[site] = href
								value = player_links
							player[key] = value

						player['Game'] = cleared_game
						players.append(player)
		return players

	def get_player_info(self, playerName: str, results: bool = False) -> dict:
		player_object = smash_player()
		playerName = player_object.process_playerName(playerName)
		soup, redirect_value = self.liquipedia.parse(playerName)

		if redirect_value is not None:
			playerName = redirect_value

		player = {}
		player['info'] = player_object.get_player_infobox(soup)
		player['links'] = player_object.get_player_links(soup)
		player['history'] = player_object.get_player_history(soup)

		if results:
			parse_value = playerName + "/Results"
			try:
				soup, __ = self.liquipedia.parse(parse_value)
			except ex.RequestsException:
				player['results'] = []
			else:
				player['results'] = player_object.get_player_achivements(soup)

		return player

	def get_teams(self) -> list:
		soup, __ = self.liquipedia.parse('Portal:Teams')
		teams = []
		templates = soup.find_all('span', class_="team-template-team-standard")
		for team in templates:
			teams.append(team.a['title'])
		return teams

	def get_team_info(self, teamName, results=True):
		team_object = smash_team()
		teamName = team_object.process_teamName(teamName)
		soup, redirect_value = self.liquipedia.parse(teamName)
		if redirect_value is not None:
			teamName = redirect_value
		team = {}
		team['info'] = team_object.get_team_infobox(soup)
		team['links'] = team_object.get_team_links(soup)
		team['team_roster'] = team_object.get_team_roster(soup)
		team['org_roster'] = team_object.get_team_org(soup)
		return team
