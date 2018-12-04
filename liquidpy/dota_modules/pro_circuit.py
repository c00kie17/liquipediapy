




class dota_pro_circuit():

	def __init__(self):
		pass
		
	def get_rankings(self,soup):
		teams = []
		rows = soup.findAll('tr')
		rows = [row for row in rows if len(row)>5]
		indexes = rows[0]
		index_values = []
		for cell in indexes.find_all('th'):
			value = cell.get_text()
			if len(value) < 2:
				try:
					value = cell.find('a').get('title')
				except AttributeError:
					value = 'TBD'	
			index_values.append(value.rstrip())
		rows = rows[1:]
		for row in rows:
			team = {}
			cells = row.find_all('td')	
			for i in range(0,len(cells)):
				value = cells[i].find(text=True, recursive=False)
				if value is None:
					value = cells[i].get_text()
				if value == "99999":
					team[index_values[i]] = 0
				else:
					value = value.rstrip()
					if len(value) > 0:
						team[index_values[i]] = value
			teams.append(team)		

		return teams 

	def get_schedule(self,soup):
		events = []
		rows = soup.findAll('tr')
		indexes = rows[0]
		index_values = []
		for cell in indexes.find_all('th'):
			index_values.append(cell.get_text().rstrip())
		rows = rows[1:]
		for row in rows:
			if len(row) > 3:
				event={}
				cells = row.find_all('td')
				for i in range(0,len(cells)):	
					event[index_values[i]] = cells[i].get_text().rstrip()
				events.append(event)

		return events	




