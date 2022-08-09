import liquipediapy.exceptions as ex
from bs4 import BeautifulSoup
import requests
from urllib.request import quote

# For debug purposes
from liquipediapy.devparser import DevParser

class liquipediapy():
	def __init__(self, appname: str, game: str, debug_folder: str= ""):
		self.appname = appname
		self.game = game
		self.__headers = {'User-Agent': appname, 'Accept-Encoding': 'gzip'}
		self.__base_url = 'https://liquipedia.net/'+game+'/api.php?'

		# If enabled, offer the possibility to
		# write the output of parse.page_html to a folder
		# and reading from it afterwards to avoid surcharing liquipedia api
		# If read mode and file requested not in folder, query will happen
		self.__debug = False
		if debug_folder != "":
			self.devparser = DevParser(debug_folder) 
			self.__debug = True

	def parse(self,page):
		success, soup = False, None

		# If page.html is readable from file
		if self.__debug and self.devparser.isPageAvailableLocally(page):
			success, soup = self.devparser.fromFile(page)
		else:
			url = self.__base_url+'action=parse&format=json&page='+page
			response = requests.get(url, headers=self.__headers)
			if response.status_code == 200:
				try:
					page_html = response.json()['parse']['text']['*']
				except KeyError:
					raise ex.RequestsException(response.json(),response.status_code)	
			else:
				raise ex.RequestsException(response.json(),response.status_code)

			soup = BeautifulSoup(page_html,features="lxml")

		# If page.html wasn't readable from file, write it for next time
		if (self.__debug and not self.devparser.isPageAvailableLocally(page)):
			self.devparser.toFile(soup, page)

		redirect = soup.find('ul',class_="redirectText")
		if redirect is None:
			return soup,None
		else:
			redirect_value = soup.find('a').get_text()
			redirect_value = quote(redirect_value)
			soup,__ = self.parse(redirect_value)
			return soup,redirect_value



	def dota2webapi(self,matchId):
		if self.game == 'dota2':
			url = self.__base_url+'action=dota2webapi&data=picks_bans|players|kills_deaths|duration|radiant_win|teams|start_time&format=json&matchid='+matchId
			response = requests.get(url, headers=self.__headers)
			if response.status_code == 200:
				res = response.json()
				if res['dota2webapi']['isresult'] >= 1:
					return res['dota2webapi']['result']
				else:
					return res['dota2webapi']['result']['error']
			else:
				raise ex.RequestsException(response.json(),response.status_code)
		else:
			raise ex.RequestsException('set game as dota2 to access this api',0)			



	def search(self,serachValue):
		url = self.__base_url+'action=opensearch&format=json&search='+serachValue
		response = requests.get(url, headers=self.__headers)
		if response.status_code == 200:
			return  response.json()
		else:
			raise ex.RequestsException(response.json(),response.status_code)		