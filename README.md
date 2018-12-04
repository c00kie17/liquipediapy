# liquidpy
> api for liquipedia.net 

## Contents
- [Installation](#install)
- [Examples](#examples)
- [Docs](#docs)
- [Running](#run)
- [Contributing](#cb)
- [Author](#author)
- [License](#ls)
- [Issue](#issue)

<a name="install"></a>
## Install 

```pip install liquidpy```

Please refer to [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for rate-limiting information. 

## Examples
The `examples` directory contains an example files on how to interact with the each object.

## Docs
- [liquidpy](#liquidpy_obj)
  - [parse](#liquidpy_parse)
  - [search](#liquidpy_search)
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
  
<a name="liquidpy_obj"></a>  
#### liquidpy(appname)
create a liquidpy object

##### parameters
| Param | Type | Description |
| --- | --- | --- |
| appname | <code>string</code> | The name for your app, you can refer to the [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for more information |

##### example
```python
from liquidpy import liquidpy

liquipy_object = liquidpy('appname')
```
***
<a name="liquidpy_parse"></a>  
#### parse(page,page_format)
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
soup,url = liquipy_object.parse('arteezy')
```
***
<a name="liquidpy_search"></a>  
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
search_result = liquipy_object.search('mar')
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
from liquidpy import dota

dota_obj = dota("appname")
```
***


<a name="dota_get_players"></a>  
#### get_players()
returns all dota players on this [page](https://liquipedia.net/dota2/Portal:Players)

##### response
````python
[{'country': 'Russia', 'ID': '.Ark', 'Name': 'Egor Zhabotinskii', 'Team': '', 'Links': {'twitter': 'https://twitter.com/just_Ark', 'vk': 'http://vk.com/wtfkaelownage'}},...,{'country': 'China', 'ID': '小郭嘉', 'Name': 'Zhan Yaoyang', 'Team': '', 'Links': {}}, {'country': 'China', 'ID': '闷油瓶', 'Name': 'Wang Liang', 'Team': '', 'Links': {}}]
````
##### example
```python
dota_obj.get_players()
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
dota_obj.get_player_info('Miracle-',True)
```
***
