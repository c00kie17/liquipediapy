from liquidpy import liquidpy


liquidpy_object = liquidpy('appname')

soup,url = liquidpy_object.parse('arteezy')

match_details = liquidpy_object.dota2webapi('4225454337')

search_result = liquidpy_object.search('mar')
