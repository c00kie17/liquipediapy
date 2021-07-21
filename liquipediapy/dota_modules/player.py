import re
from urllib.request import quote
import unicodedata


class dota_player:
    def __init__(self):
        self.__image_base_url = "https://liquipedia.net"
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
                player["image"] = self.__image_base_url + image_url
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
        stats = []
        table = soup.find("table", {"class": "wikitable"})
        if table == None or "wikitable-striped" in table["class"]:
            return []

        headers = table.findChildren("th", recursive=True)
        stat_headers = []
        for head in headers:
            stat_headers.append(unicodedata.normalize("NFKD", head.text.strip()))

        rows = table.findChildren("tr")
        for row in rows:
            data = row.findChildren("td", recursive=False)
            if len(data) == 0:
                continue
            stat = {}
            for i, header in enumerate(stat_headers):
                stat[header] = data[i].text.strip()
            stats.append(stat)

        return stats

    def get_player_achievements(self, soup):

        size = 7
        achievements = []
        table = soup.find("table", {"class": "wikitable-striped"})

        headers = table.findChildren("th", recursive=True)
        achievements_headers = []
        for head in headers:
            achievements_headers.append(head.text)

        achivements_headers = achievements_headers[:size]

        rows = table.findChildren("tr")
        achievement_rows = []
        for row in rows:
            if row.find("td", {"class": "results-score"}):
                achievement_rows.append(row)

        if len(achievement_rows) == 0:
            return achievements

        for row in achievement_rows:
            data = row.findChildren("td", recursive=False)
            achievement = {}
            counter = 0
            for header in achivements_headers:
                image_counters = [3, 5, 7]
                if counter in image_counters:
                    spans = data[counter].findChildren("span")
                    key = ""
                    if counter == 3:
                        key = "tournament_icon"
                        counter += 1
                        span_class = "league-icon-small-image"
                    elif counter == 5 or counter == 7:
                        if counter == 5:
                            key = "team_icon"
                        elif counter == 7:
                            key = "opponent_team_icon"
                            counter += 1
                        span_class = "team-template-team-icon"
                    for span in spans:
                        if span.has_attr("class"):
                            if span_class in span["class"]:
                                try:
                                    achievement[key] = (
                                        self.__image_base_url
                                        + span.find("a").find("img")["src"]
                                    )
                                except AttributeError:
                                    pass

                if header == "Place":
                    value = data[counter].text.replace(
                        data[counter].findChild("span").text, ""
                    )
                elif header == "Tier":
                    value = data[counter].find("a").text
                else:
                    value = data[counter].text

                achievement[header] = unicodedata.normalize("NFKD", value.rstrip())
                counter += 1

            achievements.append(achievement)

        return achievements

    def process_playerName(self, playerName):
        if playerName in self.__player_exceptions:
            playerName = playerName + "_(player)"
        if not playerName[0].isdigit():
            playerName = list(playerName)
            playerName[0] = playerName[0].upper()
            playerName = "".join(playerName)
        playerName = quote(playerName)

        return playerName
