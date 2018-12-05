# liquipediapy
> api for liquipedia.net 

## Contents
- [Installation](#install)
- [Examples](#examples)
- [API](#api)
- [Contributing](#cb)
- [Author](#author)
- [License](#ls)

<a name="install"></a>
## Install 

```pip install liquipediapy```

Please refer to [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for rate-limiting information. 

<a name="examples"></a>
## Examples
The [examples](https://github.com/c00kie17/liquipediapy/tree/master/examples) directory contains an example files on how to interact with the each class.

<a name="api"></a>
## API
- [liquipediapy](#liquipediapy_obj)
  - [parse](#liquipediapy_parse)
  - [dota2webapi](#liquipediapy_dota2webapi)
  - [search](#liquipediapy_search)
- [dota](#dota)
  - [get_players](#dota_get_players)
  - [get_player_info](#dota_get_player_info)
  - [get_team_info](#dota_get_team_info)
  - [get_transfers](#get_transfers)
  - [get_upcoming_and_ongoing_games](#dota_get_upcoming_and_ongoing_games)
  - [get_heros](#dota_get_heros)
  - [get_items](#dota_get_items)
  - [get_patches](#dota_get_patches)
  - [get_tournaments](#dota_get_tournaments)
  - [get_pro_circuit_details](#dota_get_pro_circuit_details)
  
<a name="liquipediapy_obj"></a>  
#### liquipediapy(appname)
create a liquipediapy object

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| appname | <code>string</code> | The name for your app, you can refer to the [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for more information |

##### example
```python
from liquipediapy import liquipediapy

liquipy_object = liquipediapy('appname')
```
***
<a name="liquipediapy_parse"></a>  
#### parse(page)
parses a given page
[example](https://liquipedia.net/dota2/api.php?action=parse&page=arteezy)
##### parameters
| Param | Type | Description |
| --- | --- | --- |
| page | <code>string</code> | name of the page you want to parse |


##### response
| Return | Type | Description |
| --- | --- | --- |
| soup | <code>bs4 Object</code> | a [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) object  |
| redirect_value | <code>string</code> | if the page has been redirected then returns page value it was redirected to, orderwise returns ```None``` |

##### example
```python
soup,url = liquipediapy_object.parse('arteezy')
```
***

<a name="liquipediapy_dota2webapi"></a>  
#### dota2webapi(matchId)
returns match details for a given match 
[example](https://liquipedia.net/dota2/api.php?action=dota2webapi&matchid=4225454337&data=picks_bans%7Cplayers%7Ckills_deaths|duration|radiant_win|teams|start_time&format=json)

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| matchId | <code>string</code> | ID of the match you want details for  |


##### response
| Return | Type | Description |
| --- | --- | --- |
| match_details | <code>json</code> | match_details if valid matchID otherwise an error in json  |


##### example
```python
match_details = liquipediapy_object.dota2webapi('4225454337')
```
***


<a name="liquipediapy_search"></a>  
#### search(serach_value)
searchs liquipedia.net for a given term
[example](https://liquipedia.net/dota2/api.php?action=opensearch&format=json&search=mid)

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| serach_value | <code>string</code> | search term |


##### response
| Return | Type | Description |
| --- | --- | --- |
| search_result | <code>json</code> | response |

##### example
```python
search_result = liquipediapy_object.search('mar')
```
***
<a name="dota"></a>  
#### dota(appname)
create a dota object

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| appname | <code>string</code> | The name for your app, you can refer to the [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for more information |

##### example
```python
from liquipediapy import dota

dota_obj = dota("appname")
```
***


<a name="dota_get_players"></a>  
#### get_players()
returns all dota players from [Portal:Players](https://liquipedia.net/dota2/Portal:Players)

##### response
````python
[{'country': 'Russia', 'ID': '.Ark', 'Name': 'Egor Zhabotinskii', 'Team': '', 'Links': {'twitter': 'https://twitter.com/just_Ark', 'vk': 'http://vk.com/wtfkaelownage'}},...,{'country': 'China', 'ID': '小郭嘉', 'Name': 'Zhan Yaoyang', 'Team': '', 'Links': {}}, {'country': 'China', 'ID': '闷油瓶', 'Name': 'Wang Liang', 'Team': '', 'Links': {}}]
````
##### example
```python
players = dota_obj.get_players()
```
***


<a name="dota_get_player_info"></a>  
#### get_player_info(playerName,results)
gets information for a specified player

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| playerName | <code>string</code> | name of player |
| results | <code>bool</code> | if you want to parse the results page for the player, defauls to ```False``` |


##### response
````python
{'info': {'image': 'https://liquipedia.net/commons/images/thumb/f/f2/Miracle_SL_i-League.jpg/600px-Miracle_SL_i-League.jpg', 'name': 'عامر البرقاوي', 'romanized_name': 'Amer Al-Barkawi', 'birth_details': 'June 20, 1997 (1997-06-20) (age21)', 'country': ['Jordan', 'Poland'], 'status': 'Active', 'team': 'Team Liquid', 'roles': ['Solo Middle', 'Carry'], 'signature_heros': ['Invoker', 'Anti Mage', 'Shadow Fiend'], 'earnings': 3668824, 'ranking': {'rank': '10', 'points': 3120}}, 'links': {'dotabuff': 'https://www.dotabuff.com/esports/players/105248644',...,'steamcommunity': 'https://steamcommunity.com/profiles/76561198065514372'}, 'history': [{'duration': '2015-01-01 — 2015-04-02', 'name': 'Balkan Bears'},...{'duration': '2016-09-16 — Present', 'name': 'Team Liquid'}], 'achivements': [{'Date': '2018-08-24', 'Placement': '44', 'LP Tier': 'Premier', 'Tournament': 'The International 2018', 'Team': 'Team Liquid', 'Results': '0:2', 'opponent': 'Evil Geniuses', 'Prize': '$1,787,252'},...{'Date': '2015-11-21', 'Placement': '11', 'LP Tier': 'Premier', 'Tournament': 'The Frankfurt Major 2015', 'Team': 'OG', 'Results': '3:1', 'opponent': 'Team Secret', 'Prize': '$1,110,000'}], 'results': [{'Date': '2018-11-30', 'Placement': '22', 'LP Tier': 'Qualifier', 'Tournament': 'The Chongqing Major Europe Qualifier', 'Team': 'Team Liquid', 'Results': '2:1', 'opponent': 'Alliance', 'Prize': '$0'},...{'Date': '2015-01-21', 'Placement': '55 - 8', 'LP Tier': 'Minor', 'Tournament': 'Esportal Dota 2 League Open Tournament 2', 'Team': 'Balkan Bears', 'Results': '1:2', 'opponent': 'MYinsanity', 'Prize': '$0'}]}
````
##### example
```python
player_details = dota_obj.get_player_info('Miracle-',True)
```
***


<a name="dota_get_team_info"></a>  
#### get_team_info(teamName,results)
gets information for a specified team

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| teamName | <code>string</code> | name of the team |
| results | <code>bool</code> | if you want to parse the results page for the team, defauls to ```False``` |


##### response
````python
{'info': {'image': 'https://liquipedia.net/commons/images/thumb/b/b6/Team_Liquid_2017_Vertical_Type.png/600px-Team_Liquid_2017_Vertical_Type.png', 'location': ['Netherlands', 'Europe'], 'region': 'Europe', 'director': 'NazgulSteve Arhancet', 'manager': 'Mohamed Morad', 'team captain': 'KuroKy', 'sponsor': ['Monster',..., 'Ballistix'], 'earnings': 17312752, 'ranking': {'rank': '2', 'points': 9459}, 'created': '2012-12-06'}, 'links': {'teamliquidpro': 'https://www.teamliquidpro.com/',..., 'datdota': 'https://www.datdota.com/teams/2163'}, 'cups': ['RaidCall Dota 2 League Season 2', ... ,'China Dota2 Supermajor'], 'team_roster': [{'ID': 'MATUMBAMAN', 'Name': 'Lasse Urpalainen', 'Position': '1/2', 'Join Date': '2015-10-09'}, ...,{'ID': 'KuroKy', 'Name': 'Kuro Salehi Takhasomi', 'Position': '5', 'Join Date': '2015-10-09'}], 'results': [{'Date': '2018-11-30', 'Placement': '22', 'LP Tier': 'Qualifier', 'Tournament': 'The Chongqing Major Europe Qualifier', 'Results': '2:1', 'opponent': 'Alliance', 'Prize': '$0'},...,{'Date': '2013-02-10', 'Placement': '11', 'LP Tier': 'Minor', 'Tournament': 'BeyondTheSummit Weekend Cup', 'Results': '2:1', 'opponent': 'Fnatic', 'Prize': '$500'}]}

````
##### example
```python
team_details = dota_obj.get_team_info('Team Liquid',True)
```
***


<a name="get_transfers"></a>  
#### get_transfers()
gets all transfers from [Portal:Transfers](https://liquipedia.net/dota2/Portal:Transfers)



##### response
````python
[{'Date': '2018-12-03', 'Player': ['Moogy', 'Inflame'], 'Previous': 'Newbee', 'Current': 'Newbee'},...{'Date': '2018-09-10', 'Player': ['Fenrir'], 'Previous': 'Vici Gaming', 'Current': 'Team Aster'}]
````
##### example
```python
transfers = dota_obj.get_transfers()
```
***

<a name="dota_get_upcoming_and_ongoing_games"></a>  
#### get_upcoming_and_ongoing_games()
gets all matches from [Liquipedia:Upcoming_and_ongoing_matches](https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches)



##### response
````python
[{'team1': 'WP Gaming', 'format': 'Bo3', 'team2': 'Playmakers Esports', 'start_time': 'December 5, 2018 - 2:00 UTC', 'tournament': 'The Bucharest Minor SA Qual', 'twitch_channel': None},...,{'team1': 'Doge (Singaporean team)', 'format': 'Bo1', 'team2': 'Casuals', 'start_time': 'December 15, 2018 - 9:00 UTC', 'tournament': 'SEL Season 2', 'twitch_channel': 'sgpesports'}]
````
##### example
```python
games = dota_obj.get_upcoming_and_ongoing_games()
```
***

<a name="dota_get_heros"></a>  
#### get_heros()
gets all heros from [Portal:Heroes](https://liquipedia.net/dota2/Portal:Heroes)



##### response
````python
[{'image': 'https://liquipedia.net/commons/images/thumb/f/fa/Abaddon_Large.png/125px-Abaddon_Large.png', 'name': 'Abaddon'},...,{'image': 'https://liquipedia.net/commons/images/thumb/9/91/Zeus_Large.png/125px-Zeus_Large.png', 'name': 'Zeus'}]
````
##### example
```python
heros = dota_obj.get_heros()
```
***

<a name="dota_get_items"></a>  
#### get_items()
gets all items from [Portal:Items](https://liquipedia.net/dota2/Portal:Items)



##### response
````python
[{'image': 'https://liquipedia.net/commons/images/thumb/c/cd/Animal_Courier.png/60px-Animal_Courier.png', 'name': 'Animal Courier', 'price': '50'},...,{'image': 'https://liquipedia.net/commons/images/thumb/e/  e8/Ring_of_Aquila.png/60px-Ring_of_Aquila.png', 'name': 'Ring of Aquila', 'price': '985'}]
````
##### example
```python
items = dota_obj.get_items()
```
***

<a name="dota_get_patches"></a>  
#### get_patches()
gets all patches from [Portal:Patches](https://liquipedia.net/dota2/Portal:Patches)



##### response
````python
[{'Version': '7.20c', 'Release Date': '2018-11-24', 'Highlights': ['Balance Changes']},...,{'Version': '0.60', 'Highlights': ['Ported the following heroes:', ' Chen', ' Crystal Maiden', ' Death Prophet', ' Doom', ' Drow Ranger', ' Faceless Void', ' Lich', ' Lina', ' Lion', ' Magnus', " Nature's Prophet", ' Nyx Assassin', ' Pugna', ' Queen of Pain', ' Razor', ' Riki', ' Shadow Shaman', ' Silencer', ' Slardar', ' Sven', ' Vengeful Spirit', ' Venomancer', ' Viper', ' Visage', ' Wraith King']}]
````
##### example
```python
patches = dota_obj.get_patches()
```
***


<a name="dota_get_tournaments"></a>  
#### get_tournaments()
gets all tournaments from [Portal:Tournaments](https://liquipedia.net/dota2/Portal:Tournaments)



##### response
````python
[{'tier': 'Major', 'name': ' The Bucharest Minor', 'icon': 'https://liquipedia.net/commons/images/e/ed/The_Bucharest_Mihttps://github.com/c00kie17/liquipediapy/blob/master/CONTRIBUTING.mdnor_icon.png', 'dates': 'Jan 9 - 13, 2019', 'prize_pool': 300000, 'teams': '8', 'host_location': 'Romania', 'event_location': 'Bucharest', 'links': [{'pglesports': 'http://dota2.pglesports.com/'},...,{'twitter': 'https://twitter.com/pglesports'}]},...,{'tier': 'Qualifier', 'name': ' The Bucharest Minor Southeast Asia Open Qualifier', 'icon': 'https://liquipedia.net/commons/images/e/ed/The_Bucharest_Minor_icon.png', 'dates': 'Dec 1 - 3, 2018', 'prize_pool': 0, 'teams': '82', 'host_location': 'Southeast Asia', 'event_location': 'Online', 'winner': ' CG', 'runner_up': ' WG.U'}]
````
##### example
```python
tournaments = dota_obj.get_tournaments()
```
***



<a name="dota_get_pro_circuit_details"></a>  
#### get_pro_circuit_details()
returns pro circuit [rankings](https://liquipedia.net/dota2/Dota_Pro_Circuit/2018-19/Rankings) and [schedule](https://liquipedia.net/dota2/Dota_Pro_Circuit/2018-19/Schedule)



##### response
````python
{'rankings': [{'#': '1.', 'ID': ' Virtus.pro', 'Points': ' 4950', 'DreamLeague Season 10': 0, 'The Kuala Lumpur Major': ' 4950', 'The Bucharest Minor': 0, 'The Chongqing Major': 0, 'TBD': 0, 'DreamLeague Season 11': 0, 'AMD SAPPHIRE Dota PIT Minor': 0},...{'#': '23.', 'ID': ' ROOONS', 'Points': ' 8.192 5', 'DreamLeague Season 10': ' 20', 'The Kuala Lumpur Major': 0, 'The Bucharest Minor': 0, 'The Chongqing Major': 0, 'TBD': 0, 'DreamLeague Season 11': 0, 'AMD SAPPHIRE Dota PIT Minor': 0}], 'schedule': [{'Date': 'Sep 16-21, 2018', 'Title': ' The Kuala Lumpur Major Qualifier', 'DPC Points': '0'},...,{'Date': 'June 20-30, 2019', 'Title': 'Major Main Event', 'DPC Points': '15000'}]}
````
##### example
```python
pro_circuit_details = dota_obj.get_pro_circuit_details()
```
***
<a name="cb"></a> 
## Contributing

Contributions are welcome. Please submit all pull requests the against master branch. Please check the [Contributing Guidelines](https://github.com/c00kie17/liquipediapy/blob/master/CONTRIBUTING.md) for more details. If you want to contribute but have no idea what to work towards please check the [TODO](https://github.com/c00kie17/liquipediapy/blob/master/TODO.md) file or [Issues](https://github.com/c00kie17/liquipediapy/issues) there should always be something there you can work towards. Thanks! 

***
<a name="author"></a> 
## Author
[c00kie17](https://github.com/c00kie17)

***
<a name="ls"></a> 
## License
This project conforms to the [CC-BY-SA 3.0 license](https://creativecommons.org/licenses/by-sa/3.0/us/) as that is the License that all the text data on Liquipedia adhears to, for more information you can check out the [Liquipedia Copyrights Page](https://liquipedia.net/commons/Liquipedia:Copyrights). 

A lot of images you can download with this API have been provided to Liquipedia under separate licensing terms that may be incompatible with [CC-BY-SA 3.0 license](https://creativecommons.org/licenses/by-sa/3.0/us/).
 


