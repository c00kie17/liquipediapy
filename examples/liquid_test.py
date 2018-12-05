from liquipediapy import liquipediapy

liquipediapy_object = liquipediapy('appname')

soup,url = liquipediapy_object.parse('arteezy')

match_details = liquipediapy_object.dota2webapi('4225454337')

search_result = liquipediapy_object.search('mar')
