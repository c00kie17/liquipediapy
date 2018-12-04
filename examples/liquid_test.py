from liquidpy import liquidpy


liquipy_object = liquidpy('appname')

soup,url = liquipy_object.parse('arteezy')
print(soup)
print(url)

print(liquipy_object.search('mar'))
