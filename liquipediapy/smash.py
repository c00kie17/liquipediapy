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

	def get_team_info(self, teamName: str, results: bool = True) -> dict:
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

	def get_transfers(self) -> list:
		transfers = []
		soup, __ = self.liquipedia.parse('Player_Transfers')
		# Main transfer page doesn't work as expected
		# Iterate over all year to get all transfers

		# First line is "Latest", Second is "2013", empty
		years = soup.find('div', class_='tabs-static').find_all('li')[2:]

		for year in years:
			year = year.get_text()
			url = f"Player_Transfers/{year}"
			soup, _ = self.liquipedia.parse(url)

			indexes = soup.find('div', class_='divHeaderRow')
			index_values = []
			for cell in indexes.find_all('div'):
				text = cell.get_text().strip()
				if text != '':
					index_values.append(text)
			index_values.insert(3, 'Icon')
			index_values.append('Link')
			rows = soup.find_all('div', class_='divRow')
			for row in rows:
				transfer = {}
				cells = row.find_all('div', class_='divCell')
				for i in range(0, len(cells)):
					key = index_values[i]
					value = cells[i].get_text().strip()
					if key == "Player":
						# Player can have up to three direct child
						# Country, Main, Name
						children = [
							c for c in cells[i].findChildren(recursive=False) if c.name != 'br'
						]

						players = []
						player = {}
						for child in children:
							if child.name == 'span':
								if 'Country' in player.keys():
									players.append(player)
									player = {}
								player['Country'] = child.find('a').get('title').strip()
							elif child.name == 'img':
								if 'Main' in player.keys():
									players.append(player)
									player = {}
								player['Main'] = child.get('title').strip()
							elif child.name == 'a':
								if 'Name' in player.keys():
									players.append(player)
									player = {}
								player['Name'] = child.get_text().strip()
						players.append(player)
						value = players
					if key == "Old" or key == "New":
						try:
							value = cells[i].find('a').get('title')
						except AttributeError:
							value = "None"

					if key == 'Icon':
						continue
					if key == 'Link':
						try:
							value = cells[i].find('a').get('href')
						except AttributeError:
							value = "None"

					transfer[key] = value
				transfer = {k: v for k, v in transfer.items() if len(k) > 0}
				transfers.append(transfer)

		return transfers

	def get_tournaments(
		self,
		games: list = ['64'],
		extended_infos: bool = False
	) -> list:
		"""Get extended_infos
		Type (Major, Invitationnal, Double, etc.)
		Winner & Runner-up Characters (For Majors only)

		Up to 7 Additionnal Queries
			/Major_Tournaments/64
												/Melee
												/Brawl
												/Project_M
												/Wii_U
												/Ultimate
			/Misc_Tournaments (Which get all misc for all games)

		Get tournament Games ([64, Melee, Brawl, Project_M, Wii_U, Ultimate])
			From 1 To 9 Queries
			/Portal:Tournaments/All/64
															/Melee
																		/2018-2020
																		/Pre-2018
															/Brawl
															/Project_M
															/Wii_U
															/Ultimate
																				/Pre-2021
			-------------------------------------------
																	Queries: 2 - 16"""

		tournaments = []
		if extended_infos:
			page_val = f'Misc_Tournaments'
			misc_soup, __ = self.liquipedia.parse(page_val)

		for game in games:
			page_val = f'Portal:Tournaments/All/{game}'
			soups = []
			soup, __ = self.liquipedia.parse(page_val)
			soups.append(soup)

			if game == 'Melee':
				page_val = f'Portal:Tournaments/All/{game}/2018-2020'
				soup, __ = self.liquipedia.parse(page_val)
				soups.append(soup)
				page_val = f'Portal:Tournaments/All/{game}/Pre-2018'
				soup, __ = self.liquipedia.parse(page_val)
				soups.append(soup)
			elif game == 'Ultimate':
				page_val = f'Portal:Tournaments/All/{game}/Pre-2021'
				soup, __ = self.liquipedia.parse(page_val)
				soups.append(soup)

			if extended_infos:
				page_val = f'Major_Tournaments/{game}'
				major_soup, __ = self.liquipedia.parse(page_val)

			index_row = soup.find('div', class_='divHeaderRow')
			index_cells = index_row.find_all('div', class_='divCell')
			index_values = [c.get_text().replace('P#', 'Players') for c in index_cells]

			for soup in soups:
				div_rows = soup.find_all('div', class_="divRow")
				for row in div_rows:
					tournament = {}
					tournament['Game'] = game
					div_cells = row.find_all('div', class_="divCell")
					for i, cell in enumerate(div_cells):
						key = index_values[i]
						if key == 'Tournament':
							value = cell.find('b').get_text()
						elif key == 'Date':
							value = cell.get_text()
						elif key == 'Prize':
							try:
								value = cell.get_text()
								prize = {
									'amount': float(value[1:].replace(',', '')),
									'currency': value[0]
								}
							except ValueError:
								value = cell.get_text()
								prize = {'amount': value, 'currency': value}
							value = prize
						elif key == 'Players':
							try:
								value = cell.find('span').get_text()
							except AttributeError:
								value = ""
						elif key == 'Location':
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['City'] = cell.get_text().strip()
							except AttributeError:
								value['City'] = ""
						elif key == 'Winner':
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['Name'] = (
									cell.find('a').get_text().strip().replace('TBD', '')
								)
							except AttributeError:
								value['Name'] = ""
						elif key == 'Runner-up':
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['Name'] = (
									cell.find('a').get_text().strip().replace('TBD', '')
								)
							except AttributeError:
								value['Name'] = ""

						tournament[key] = value
					tournaments.append(tournament)
			if extended_infos:
				# game_header = ['64', 'Melee',...]
				# Misc Part
				counter = 0
				if game == '64':
					counter = 1
				elif game == 'Melee':
					counter = 2
				elif game == 'Brawl':
					counter = 3
				elif game == 'Project_M':
					counter = 4
				elif game == 'Wii_U':
					counter = 5
				elif game == 'Ultimate':
					counter = 6

				game_div = misc_soup.find('div', class_=f'content{counter}')
				year_divs = game_div.find_all('div', class_='divTable')
				for year_div in year_divs:
					rows = year_div.find_all('div', class_='divRow')
					for row in rows:
						tournament_type = row.find(
							'div', class_='Tier'
						).get_text().strip()

						tournament_name = row.find(
							'div', class_='Tournament'
						).get_text().strip()
						try:
							tournament = next(
								x for x in tournaments if x['Tournament'] == tournament_name
							)
							tournament['Type'] = tournament_type
						except StopIteration:
							# We got a special tournament,
							# We need to get all the info

							tournament = {}
							tournament['Game'] = game
							tournament['Tournament'] = tournament_name
							tournament['Type'] = tournament_type

							tournament['Date'] = row.find(
								'div', class_='EventDetails-Left-55'
							).get_text().strip()

							try:
								value = row.find(
									'div', class_='EventDetails-Right-45'
								).get_text().strip()
								prize = {
									'amount': float(value[1:].replace(',', '')),
									'currency': value[0]
								}
							except ValueError:
								value = row.find(
									'div', class_='EventDetails-Right-45'
								).get_text().strip()
								prize = {'amount': value, 'currency': value}
							tournament['Prize'] = prize

							tournament['Players'] = row.find(
								'div', class_='EventDetails-Left-40'
							).get_text().strip()

							cell = row.find(
								'div', class_='EventDetails-Right-60'
							)
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['City'] = cell.get_text().strip()
							except AttributeError:
								value['City'] = ""
							tournament['Location'] = value
							tournaments.append(tournament)

				# Major Part
				year_divs = major_soup.find_all('div', class_='divTable')
				for year_div in year_divs:
					rows = year_div.find_all('div', class_='divRow')
					for row in rows:
						tournament_name = row.find(
							'div', class_='Tournament'
						).get_text().strip()
						try:
							tournament = next(
								x for x in tournaments if x['Tournament'] == tournament_name
							)
							tournament['Type'] = 'Major'
							if 'tournament-card-premier' in row.attrs['class']:
								tournament['Type'] = 'SuperMajor'

							spans = row.find(
								'div', class_='FirstPlace'
							).find_all('span', class_='heads-padding-right')
							winner_characters = [span.find('img').get('title') for span in spans]
							tournament['Winner']['Characters'] = winner_characters

							spans = row.find(
								'div', class_='SecondPlace'
							).find_all('span', class_='heads-padding-right')
							runner_up_characters = [span.find('img').get('title') for span in spans]
							tournament['Runner-up']['Characters'] = runner_up_characters
						except StopIteration:
							# We got a special/upcoming tournament,
							# We need to get all the info
							tournament = {}
							tournament['Game'] = game
							tournament['Tournament'] = tournament_name
							tournament['Type'] = tournament_type
							if 'tournament-card-premier' in row.attrs['class']:
								tournament['Type'] = 'SuperMajor'

							tournament['Date'] = row.find(
								'div', class_='EventDetails-Left-55'
							).get_text().strip()

							try:
								value = row.find(
									'div', class_='EventDetails-Right-45'
								).get_text().strip()
								prize = {
									'amount': float(value[1:].replace(',', '')),
									'currency': value[0]
								}
							except ValueError:
								value = row.find(
									'div', class_='EventDetails-Right-45'
								).get_text().strip()
								prize = {'amount': value, 'currency': value}
							tournament['Prize'] = prize

							tournament['Players'] = row.find(
								'div', class_='EventDetails-Left-40'
							).get_text().strip()

							cell = row.find(
								'div', class_='EventDetails-Right-60'
							)
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['City'] = cell.get_text().strip()
							except AttributeError:
								value['City'] = ""
							tournament['Location'] = value

							# WINNER
							cell = row.find(
								'div', class_='FirstPlace'
							)
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['Name'] = (
									cell.find('a').get_text().strip().replace('TBD', '')
								)
							except AttributeError:
								value['Name'] = ""

							tournament['Winner'] = value

							spans = cell.find_all(
								'span', class_='heads-padding-right'
							)
							winner_characters = [span.find('img').get('title') for span in spans]
							tournament['Winner']['Characters'] = winner_characters

							# RUNNERUP
							cell = row.find(
								'div', class_='SecondPlace'
							)
							value = {}
							try:
								value['Country'] = (
									cell.find(
										'span', class_='flag'
									).find('img')
									.get('title')
								)
							except AttributeError:
								value['Country'] = ""
							try:
								value['Name'] = (
									cell.find('a').get_text().strip().replace('TBD', '')
								)
							except AttributeError:
								value['Name'] = ""

							tournament['Runner-up'] = value

							spans = cell.find_all(
								'span', class_='heads-padding-right'
							)
							runner_up_characters = [span.find('img').get('title') for span in spans]
							tournament['Runner-up']['Characters'] = runner_up_characters

							tournaments.append(tournament)
		return tournaments
