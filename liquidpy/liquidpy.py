import liquidpy.exceptions as ex
from bs4 import BeautifulSoup
import requests
from urllib.request import quote

class liquidpy():
	def __init__(self,appname):
		self.appname = appname
		self.__headers = {'User-Agent': appname,'Accept-Encoding': 'gzip'}
		self.__base_url = 'https://liquipedia.net/dota2/api.php?'

	def parse(self,page):
		url = self.__base_url+'action=parse&format=json&page='+page
		response = requests.get(url, headers=self.__headers)
		if response.status_code == 200:
			try:
				page_html = response.json()['parse']['text']['*']
			except KeyError:
				raise ex.RequestsException(response.json(),response.status_code)	
			soup = BeautifulSoup(page_html,features="lxml")
			redirect = soup.find('ul',class_="redirectText")
			if redirect is None:
				return soup,None
			else:
				redirect_value = soup.find('a').get_text()
				redirect_value = quote(redirect_value)
				soup,__ = self.parse(redirect_value)
				return soup,redirect_value
		else:
			raise ex.RequestsException(response.json(),response.status_code)	


	def search(self,serach_value):
		url = self.__base_url+'action=opensearch&format=json&search='+serach_value
		response = requests.get(url, headers=self.__headers)
		if response.status_code == 200:
			return  response.json()
		else:
			raise ex.RequestsException(response.json(),response.status_code)		