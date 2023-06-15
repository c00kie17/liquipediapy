import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
import re
import unicodedata
from liquipediapy.valorant_modules.player import valorant_player
from liquipediapy.valorant_modules.team import valorant_team
import itertools
from urllib.request import quote


class valorant():

  def __init__(self, appname):
    self.appname = appname
    self.liquipedia = liquipediapy(appname, 'valorant')
    self.__image_base_url = 'https://liquipedia.net'

  def get_transfers(self):
    transfers = []
    soup, __ = self.liquipedia.parse('Portal:Transfers')
    index_values = []
    header_row = soup.find('div', class_='divHeaderRow')
    cells = header_row.find_all('div', class_='divCell')
    for cell in cells:
      index_values.append(cell.get_text().strip())
    rows = soup.find_all('div', class_='divRow')
    for row in rows:
      transfer = {}
      cells = row.find_all('div', class_='divCell')
      for i in range(0, len(cells)):
        key = index_values[i]
        value = cells[i].get_text()
        if key == "Player":
          value = [val for val in value.split(' ') if len(val) > 0]
        if key == "Old" or key == "New":
          try:
            value = cells[i].find('a').get('title')
          except AttributeError:
            value = "None"
        if key == "Ref":
          try:
            value = cells[i].find('a').get('href')
          except AttributeError:
            value = "None"
        transfer[key] = value
      transfer = {k: v for k, v in transfer.items() if len(k) > 0}
      transfers.append(transfer)

    return transfers

  def get_upcoming_and_ongoing_games(self):
    games = []
    soup, __ = self.liquipedia.parse('Liquipedia:Matches')
    matches = soup.find_all('table', class_='infobox_matches_content')
    for match in matches:
      game = {}
      cells = match.find_all('td')
      try:
        game['team1'] = cells[0].find(
          'span', class_='team-template-text').find('a').get('title')
        game['team2'] = cells[2].find(
          'span', class_='team-template-text').find('a').get('title')
        game['start_time'] = cells[3].find('span',
                                           class_="timer-object").get_text()
        game['tournament'] = cells[3].find('div').get_text().rstrip()
        try:
          game['twitch_channel'] = cells[3].find(
            'span', class_="timer-object").get('data-stream-twitch')
        except AttributeError:
          pass
        games.append(game)
      except AttributeError:
        continue

    return games

  def get_weapons(self):
    soup, __ = self.liquipedia.parse('Portal:Weapons')
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

  def get_weapon_info(self, weaponName):
    weapon = {}
    weaponName = weaponName.replace(' ', '_')
    soup, __ = self.liquipedia.parse(weaponName)
    try:
      image_url = soup.find('div',
                            class_='infobox-image').find('img').get('src')
      if 'PlayerImagePlaceholder' not in image_url:
        weapon['image'] = self.__image_base_url + image_url
      else:
        weapon['image'] = ''
    except AttributeError:
      weapon['image'] = ''
    info_boxes = soup.find_all('div', class_='infobox-cell-2')
    for i in range(0, len(info_boxes), 2):
      attribute = info_boxes[i].get_text().replace(':', '')
      if attribute == "Side":
        weapon['side'] = info_boxes[i + 1].get_text().rstrip().split(',')
      else:
        attribute = attribute.lower().replace('(', '').replace(')',
                                                               '').replace(
                                                                 ' ', '_')
        weapon[attribute] = info_boxes[i + 1].get_text().rstrip()

    return weapon

 
  def get_patches(self):
    patches = []
    soup, __ = self.liquipedia.parse('Patches')
    tables = soup.find_all('table', class_='wikitable')
    for table in tables:
      indexes = []
      for header in table.find_all('th'):
        indexes.append(header.get_text().rstrip())
      rows = table.find_all('tr')
      rows = rows[1:]
      for row in rows:
        patch = {}
        cells = row.find_all('td')
        for i in range(0, len(cells)):
          key = indexes[i]
          if key == "Release Highlights":
            value = []
            release_list = cells[i].find_all('li')
            for release in release_list:
              value.append(release.get_text())
          else:
            value = unicodedata.normalize("NFKD", cells[i].get_text().rstrip())
          patch[key] = value
        patches.append(patch)
    print(patches)
    return patches
