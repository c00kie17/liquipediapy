from urllib.request import quote
import re
import itertools
import unicodedata
from liquipediapy.dota_modules.common import DotaCommon


class DotaTeam(DotaCommon):
    def __init__(self):
        super().__init__()

    def process_teamName(self, teamName):
        teamName = teamName.replace(" ", "_")
        teamName = quote(teamName)

        return teamName

    def get_team_infobox(self, soup):
        team = {}
        try:
            image_url = (
                soup.find("div", {"class": "img-responsive"}).find("img").get("src")
            )
            team["image"] = self.image_base_url + image_url
        except AttributeError:
            team["image"] = ""
        info_boxes = soup.find_all("div", class_="infobox-cell-2")
        for i in range(0, len(info_boxes), 2):
            attribute = info_boxes[i].get_text().replace(":", "")
            if attribute == "Sponsor" or attribute == "Location":
                value_list = []
                values = info_boxes[i + 1].find_all("a")
                for value in values:
                    text = value.get_text()
                    if len(text) > 0:
                        value_list.append(text)
                team[attribute.lower()] = value_list
            elif attribute == "Total Earnings":
                team["earnings"] = int(
                    info_boxes[i + 1].get_text().replace("$", "").replace(",", "")
                )
            else:
                team[attribute.lower()] = unicodedata.normalize(
                    "NFKD", info_boxes[i + 1].get_text().strip()
                )

        return team

    def get_team_links(self, soup):
        team_links = {}
        try:
            links = soup.find("div", class_="infobox-icons").find_all("a")
        except AttributeError:
            return team_links
        for link in links:
            link_list = link.get("href").split(".")
            site_name = link_list[-2].replace("https://", "")
            team_links[site_name] = link.get("href")

        return team_links

    def get_team_cups(self, soup):
        team_cups = []
        info_boxes = soup.find_all("div", class_="infobox-center")
        cups = []
        for boxes in info_boxes:
            cups.append(boxes.find_all("span", class_="league-icon-small-image"))
        cups = list(itertools.chain.from_iterable(cups))
        for cup in cups:
            try:
                league = cup.find("a").get("title")
                team_cups.append(league)
            except AttributeError:
                pass

        return team_cups

    def __get_roster_card_by_title(self, soup, title):
        roster_cards = soup.find_all("table", class_="roster-card")
        filtered_cards = []
        for card in roster_cards:
            title_row = card.find("tr").find("th")
            a = title_row.text.strip()
            if title_row.text.strip() == title:
                filtered_cards.append(card)
        return filtered_cards

    def get_team_roster(self, soup):
        card = self.__get_roster_card_by_title(soup, "Active Squad")[0]

        def handle_country(data):
            return data.find("span", {"class": "flag"}).find("a").get("title")

        def handle_join_date(data):
            return data.find("div", {"class": "Date"}).find(text=True, recursive=False)

        return self.read_wikitable(
            card,
            self.handle_header_roster_card,
            self.handle_row_wikitable,
            [
                {"place": 0, "add": True, "key": "Country", "func": handle_country},
                {"place": 3, "func": handle_join_date},
            ],
        )

    def get_team_org(self, soup):
        card = self.__get_roster_card_by_title(soup, "Organization")[0]

        def handle_country(data):
            return data.find("span", {"class": "flag"}).find("a").get("title")

        def handle_join_date(data):
            return data.find("div", {"class": "Date"}).find(text=True, recursive=False)

        return self.read_wikitable(
            card,
            self.handle_header_roster_card,
            self.handle_row_wikitable,
            [
                {"place": 0, "add": True, "key": "Country", "func": handle_country},
                {"place": 3, "func": handle_join_date},
            ],
        )

    def get_former_team(self, soup):
        card = self.__get_roster_card_by_title(soup, "Former Organization")[0]

        def handle_country(data):
            return data.find("span", {"class": "flag"}).find("a").get("title")

        def handle_join_leave_date(data):
            return data.find("div", {"class": "Date"}).find(text=True, recursive=False)

        return self.read_wikitable(
            card,
            self.handle_header_roster_card,
            self.handle_row_wikitable,
            [
                {"place": 0, "add": True, "key": "Country", "func": handle_country},
                {"place": 3, "func": handle_join_leave_date},
                {"place": 4, "func": handle_join_leave_date},
            ],
        )

    def get_team_achivements(self, table):
        def handle_place(data):
            return unicodedata.normalize(
                "NFKD", data.text.replace(data.findChild("span").text, "")
            )

        def handle_tier(data):
            return data.find("a").text

        def handle_tournament_icon(data):
            spans = data.findChildren("span")
            span = self.get_span_class(spans, "league-icon-small-image")
            if len(span) == 0:
                return ""

            span = span[0]
            try:
                return self.image_base_url + span.find("a").find("img")["src"]
            except AttributeError:
                return ""

        def handle_result(data):
            return unicodedata.normalize("NFKD", data.text.rstrip())

        def handle_opponent(data):
            try:
                return data.find("a")["title"].rstrip()
            except TypeError:
                return data.text

        return self.read_wikitable(
            table,
            self.handle_header_wikitable,
            self.handle_row_wikitable,
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
                    "place": 5,
                    "func": handle_result,
                },
                {
                    "place": 6,
                    "skip": True,
                    "key": "opponent",
                    "func": handle_opponent,
                },
            ],
        )

    def get_team_matches(self, table):
        def handle_tier(data):
            return data.find("a").text

        def handle_tournament_icon(data):
            spans = data.findChildren("span")
            span = self.get_span_class(spans, "league-icon-small-image")
            if len(span) == 0:
                return ""

            span = span[0]
            try:
                return self.image_base_url + span.find("a").find("img")["src"]
            except AttributeError:
                return ""

        def handle_result(data):
            return unicodedata.normalize("NFKD", data.text.rstrip())

        def handle_vod(data):
            vods = []
            links = data.find_all("span", {"class": "vodlink"})

            for link in links:
                vod = {}
                a = link.find("a")
                vod["title"] = a["title"].replace("Watch", "")
                vod["url"] = a["href"]
                vods.append(vod)
            return vods

        return self.read_wikitable(
            table,
            self.handle_header_wikitable,
            self.handle_row_wikitable,
            [
                {"place": 2, "func": handle_tier},
                {
                    "place": 4,
                    "func": handle_tournament_icon,
                    "skip": True,
                    "key": "tournament_icon",
                },
                {
                    "place": 6,
                    "func": handle_result,
                },
                {
                    "place": 8,
                    "func": handle_vod,
                },
            ],
        )
