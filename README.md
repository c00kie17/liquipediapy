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

<a name="install"></a>
## Install 

```pip install liquidpy```

Please refer to [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for rate-limiting information. 

## Examples
The `examples` directory contains an example files on how to interact with the each object.

##Docs
- [liquidpy](#liquidpy)
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
  
<a name="liquidpy"></a>  
#### liquidpy(appname)
create a liquidpy object

| Param | Type | Description |
| --- | --- | --- |
| appname | <code>string</code> | The name for your app, you can refer to the [liquipedia's terms of use](https://liquipedia.net/api-terms-of-use) for more information |


```python
from liquidpy import liquidpy

liquipy_object = liquidpy('appname')
```
<a name="liquidpy_parse"></a>  
#### parse(page,page_format)
parses a given page

| Param | Type | Description |
| --- | --- | --- |
| page | <code>string</code> | name of the page you want to parse |

[example](https://liquipedia.net/dota2/api.php?action=parse&page=arteezy)

| Return | Type | Description |
| --- | --- | --- |
| soup | <code>bs4 Object</code> | a [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) object  |
| redirect_value | <code>string</code> | if the page has been redirected then returns page value it was redirected to, orderwise returns ```None``` |

```python
soup,url = liquipy_object.parse('arteezy')
```

<a name="liquidpy_search"></a>  
#### search(serach_value)
searchs liquipedia.net for a given term

| Param | Type | Description |
| --- | --- | --- |
| serach_value | <code>string</code> | search term |

[example](https://liquipedia.net/dota2/api.php?action=opensearch&format=json&search=mid)

| Return | Type | Description |
| --- | --- | --- |
| search_result | <code>json</code> | response |


```python
search_result = liquipy_object.search('mar')
```

