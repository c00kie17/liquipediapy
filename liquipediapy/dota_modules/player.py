import re
from urllib.request import quote
import unicodedata
from liquipediapy.dota_modules.common import DotaCommon


class DotaPlayer(DotaCommon):
    def __init__(self):
        super().__init__()
        self.__player_exceptions = [
            "Fade",
            "ghost",
            "Ice",
            "Lance",
            "Ms",
            "Net",
            "Panda",
            "shadow",
            "Sky",
        ]

    def get_player_infobox(self, soup):
        player = {}
        try:
            image_url = soup.find("div", class_="infobox-image").find("img").get("src")
            if "PlayerImagePlaceholder" not in image_url:
                player["image"] = self.image_base_url + str(image_url)
            else:
                player["image"] = ""
        except AttributeError:
            player["image"] = ""

        info_boxes = soup.find_all("div", class_="infobox-cell-2")
        for i in range(0, len(info_boxes), 2):
            attribute = info_boxes[i].get_text().replace(":", "")
            if attribute == "Country":
                player["country"] = info_boxes[i + 1].get_text().split()
            elif attribute == "Alternate IDs":
                player["ids"] = info_boxes[i + 1].get_text().split(",")
            elif attribute == "Birth":
                player["birth_details"] = unicodedata.normalize(
                    "NFKD", info_boxes[i + 1].get_text()
                )
            elif attribute == "Approx. Total Earnings":
                player["earnings"] = int(
                    info_boxes[i + 1]
                    .get_text()
                    .replace("$", "")
                    .replace(",", "")
                    .replace(".", "")
                )
            elif attribute == "Pro Circuit Rank":
                ranking = {}
                ranking_list = unicodedata.normalize(
                    "NFKD", info_boxes[i + 1].get_text()
                ).split()
                ranking["rank"] = ranking_list[0].replace("#", "")
                ranking["points"] = int(
                    ranking_list[1].replace("(", "").replace(")", "").split(",")[0]
                )
                player["ranking"] = ranking
            elif attribute == "Signature Hero":
                player_heros = []
                heros = info_boxes[i + 1].find_all("a")
                for hero in heros:
                    player_heros.append(hero.get("title"))
                player["signature_heros"] = player_heros
            elif attribute == "Role(s)":
                player_roles = []
                roles = info_boxes[i + 1].find_all("a")
                for role in roles:
                    text = role.get_text()
                    if len(text) > 0:
                        player_roles.append(text)
                player["roles"] = player_roles
            else:
                attribute = (
                    attribute.lower()
                    .replace("(", "")
                    .replace(")", "")
                    .replace(" ", "_")
                )
                player[attribute] = info_boxes[i + 1].get_text().rstrip()

        return player

    def get_player_links(self, soup):
        player_links = {}
        try:
            links = soup.find("div", class_="infobox-icons").find_all("a")
        except AttributeError:
            return player_links
        for link in links:
            link_list = link.get("href").split(".")
            site_name = link_list[-2].replace("https://", "").replace("http://", "")
            player_links[site_name] = link.get("href")

        return player_links

    # not perfectly found
    def get_player_history(self, soup):
        player_history = []
        histories = soup.find_all("div", class_="infobox-center")
        try:
            histories = histories[-1].find_all("div", recursive=False)
        except IndexError:
            return player_history
        for history in histories:
            teams_info = history.find_all("div")
            if len(teams_info) > 1:
                team = {}
                team["duration"] = teams_info[0].get_text()
                team["name"] = teams_info[1].get_text()
                player_history.append(team)

        return player_history

    def get_player_statistics(self, soup):
        table = soup.find("table", {"class": "wikitable"})
        stats = self.read_wikitable(table, [])
        return stats

    def __get_span_class(self, spans, class_name):
        found_spans = []
        for span in spans:
            if span.has_attr("class"):
                if class_name in span["class"]:
                    found_spans.append(span)
        return found_spans

    def get_player_achievements(self, soup):
        table = soup.find("table", {"class": "wikitable-striped"})

        def handle_place(data):
            return data.text.replace(data.findChild("span").text, "")

        def handle_tier(data):
            return data.find("a").text

        def handle_tournament_icon(data):
            spans = data.findChildren("span")
            span = self.__get_span_class(spans, "league-icon-small-image")[0]
            try:
                return self.image_base_url + span.find("a").find("img")["src"]
            except AttributeError:
                return ""

        def handle_result(data):
            return unicodedata.normalize("NFKD", data.text.rstrip())

        def handle_opponent(data):
            return data.find("a")["title"].rstrip()

        return self.read_wikitable(
            table,
            [
                {"place": 1, "func": handle_place},
                {"place": 2, "func": handle_tier},
                {
                    "place": 3,
                    "func": handle_tournament_icon,
                    "skip": True,
                    "key": "tournament_icon",
                },
                {
                    "place": 6,
                    "func": handle_result,
                },
                {
                    "place": 7,
                    "func": handle_opponent,
                    "skip": True,
                    "key": "opponent",
                },
            ],
        )

    def process_playerName(self, playerName):
        if playerName in self.__player_exceptions:
            playerName = playerName + "_(player)"
        if not playerName[0].isdigit():
            playerName = list(playerName)
            playerName[0] = playerName[0].upper()
            playerName = "".join(playerName)
        playerName = quote(playerName)

        return playerName
