from liquipediapy import liquipediapy

liquipediapy_object_dota = liquipediapy("appname", "dota2")

soup, url = liquipediapy_object_dota.parse("arteezy")

search_result = liquipediapy_object_dota.search("mar")

liquipediapy_object_cs = liquipediapy("appname", "counterstrike")

soup, url = liquipediapy_object_cs.parse("Nitr0")

search_result = liquipediapy_object_cs.search("liq")
