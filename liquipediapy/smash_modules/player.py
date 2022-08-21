import re
from urllib.request import quote
import unicodedata


class smash_player():
	def __init__(self):
		self.__image_base_url = 'https://liquipedia.net'
		self.__player_exceptions = []

	def process_playerName(self, playerName):
		if playerName in self.__player_exceptions:
			playerName = playerName + "_(player)"
		if not playerName[0].isdigit():
			playerName = list(playerName)
			playerName[0] = playerName[0].upper()
			playerName = "".join(playerName)
		playerName = quote(playerName)
		return playerName

	def get_player_infobox(self, soup):
		player = {}
		try:
			image_url = soup.find('div', class_='infobox-image').find('img').get('src')
			if 'PlayerImagePlaceholder' not in image_url:
				player['image'] = self.__image_base_url + image_url
			else:
				player['image'] = ''
		except AttributeError:
			player['image'] = ''

		try:
			info_boxes = soup.find_all('div', class_='infobox-cell-2')
		except AttributeError:
			return player

		for i in range(0, len(info_boxes), 2):
			attribute = info_boxes[i].get_text().replace(':', '')
			if attribute == 'Country':
				player_countries = []
				countries = info_boxes[i + 1].find_all('a')
				for country in countries:
					player_countries.append(country.get_text())
				player_countries = [c for c in player_countries if len(c) > 0]
				player['countries'] = player_countries
			elif attribute == 'Birth':
				birth_details = info_boxes[i + 1].get_text()
				player['birth_details'] = unicodedata.normalize("NFKD", birth_details)
			elif attribute == 'Approx. Total Winnings':
				earnings = info_boxes[i + 1].get_text()
				earnings = earnings.replace('$', '').replace(',', '').replace('.', '')
				player['earnings'] = int(earnings)
			elif attribute == "Roles":
				player_roles = []
				roles = info_boxes[i + 1].find_all('a')
				for role in roles:
					text = role.get_text()
					if len(text) > 0:
						player_roles.append(text)
				player['roles'] = player_roles
			elif attribute == "Games":
				games = []
				game_values = info_boxes[i + 1].find_all('i')
				for game in game_values:
					games.append(game.get_text())
				player['games'] = games
			else:
				attribute = attribute.lower()
				attribute = attribute.replace('(', '').replace(')', '').replace(' ', '_')
				player[attribute] = info_boxes[i + 1].get_text().rstrip()
		return player

	def get_player_links(self, soup):
		player_links = {}
		try:
			links = soup.find('div', class_='infobox-icons').find_all('a')
		except AttributeError:
			return player_links
		for link in links:
			link_list = link.get('href').split('.')
			site_name = link_list[0].replace('https://', '').replace('http://', '')
			player_links[site_name] = link.get('href')

		return player_links

	def get_player_history(self, soup):
		player_history = []
		histories = soup.find_all('div', class_='infobox-center')
		try:
			histories = histories[-1].find_all('div', recursive=False)
		except (IndexError, AttributeError):
			return player_history

		for history in histories:
			teams_info = history.find_all('div')
			if len(teams_info) > 1:
				team = {}
				team['duration'] = teams_info[0].get_text()
				team['name'] = teams_info[1].get_text()
				player_history.append(team)

		return player_history

	def get_player_achivements(self, soup):
		header_ul = None
		b_multiGames = True
		achivements = []
		# First, get header div to retrieve game name
		try:
			header_ul = soup.find('div', class_='tabs-dynamic').find('ul')
		except AttributeError:
			b_multiGames = False

		# Get all games played
		games = []
		if b_multiGames:
			games = [game.get_text() for game in header_ul.find_all('li')[:-1]]

		# Assume that if only one game played, it's the latest one
		if not games:
			games = ["Ultimate"]

		# Multiple tables if multiple games played
		try:
			tables = soup.find_all('table', class_='wikitable-striped')
		except AttributeError:
			return achivements

		if len(tables) == 0:
			return achivements

		# Move along each game
		for j, (game, table) in enumerate(zip(games, tables)):
			try:
				rows = table.find_all('tr')
			except AttributeError:
				return achivements

			if len(rows) == 0:
				return achivements

			# Get headers
			if j == 0:
				indexes = rows[0]
				index_values = []
				for cell in indexes.find_all('th'):
					index_values.append(cell.get_text().rstrip())
				index_values.insert(0, 'Game')

			# We will handle results like this :
			# {
			#   'game': str,
			#   'date': str,
			#   'place': tuple[str],
			#   'event' : str,
			#   'result': {
			#       characters: list[str],
			#       scores: list[tuple[int]],
			#       opponent: str,
			#       opp_characters: list[str]
			#   },
			#   'prize': {
			#       'amount': float,
			#       'currency': str
			#   }
			# }

			rows = rows[1:]
			for row in rows:
				achivement = {}
				cells = row.find_all('td')
				# We sometimes have rows with date only
				if len(cells) <= 1:
					continue

				value = games[j]
				value = unicodedata.normalize("NFKD", value.rstrip())
				achivement['Game'] = value

				# 7 cells that we must split in order to get all the data
				for i in range(0, len(cells)):
					try:
						# Doing it by TDs index as we have multiple data by TDs
						if i == 0:
							achivement['Date'] = cells[i].get_text().rstrip()
						# Place
						elif i == 1:
							pool = cells[i].find('span').get_text().rstrip()
							place = cells[i].find('font').get_text().rstrip()
							achivement['Place'] = (pool, place)
						elif i == 2:
							achivement['Event'] = cells[i].get_text().rstrip()
						# Result
						elif i == 3:
							chars = [c.find('img').get('title') for c in cells[i].find_all('span')]
							achivement['Result'] = {}
							achivement['Result']['Characters'] = chars
						# Result
						elif i == 4:
							for br in cells[i].find_all('br'):
								br.replace_with('\n')
							str_scores = cells[i].get_text().split('\n')
							scores = []
							for str_score in str_scores:
								try:
									scores.append(tuple([int(i) for i in str_score.split(' : ')]))
								except ValueError:
									scores.append(str_score)
							achivement['Result']['Scores'] = scores
						# Result
						elif i == 5:
							spans = cells[i].find_all('span', class_='heads-padding-right')
							opp_characters = [c.find('img').get('title') for c in spans]
							achivement['Result']['Opp_characters'] = opp_characters

							opponent = cells[i].find('a').get_text().rstrip()
							achivement['Result']['Opponent'] = opponent
						# Prize
						elif i == 6:
							try:
								value = cells[i].get_text()
								prize = {
									'amount': float(value[1:].replace(',', '')),
									'currency': value[0]
								}
							except ValueError:
								value = cells[i].get_text()
								prize = {'amount': value, 'currency': value}
							achivement['Prize'] = prize
					except (AttributeError, IndexError):
						pass
				if len(achivement) > 0:
					achivements.append(achivement)
		return achivements
