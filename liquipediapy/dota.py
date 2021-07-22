import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
import re
from liquipediapy.dota_modules.player import DotaPlayer
from liquipediapy.dota_modules.team import DotaTeam
from liquipediapy.dota_modules.pro_circuit import dota_pro_circuit
from liquipediapy.dota_modules.common import DotaCommon


class Dota(DotaCommon):
    def __init__(self, appname):
        super().__init__()
        self.appname = appname
        self.liquipedia = liquipediapy(appname, "dota2")

    def get_players(self):
        soup, __ = self.liquipedia.parse("Players_(all)")

        def get_player_country(data):
            return data.find("a").get("title")

        def get_player_team(data):
            team = data.find("a")
            if team is not None:
                return team.get("title")
            return ""

        def get_player_links(data):
            socials = []
            links = data.find_all("a")
            for link in links:
                link_href = link.get("href")
                domain = re.search(
                    "https?://([A-Za-z_0-9.-]+).com/.*",
                    link_href,
                )
                if domain:
                    socials.append({"domain": domain.group(1), "link": link_href})
            return socials

        table = soup.find(
            "table",
            {"class": "wikitable"},
        )
        return self.read_wikitable(
            table,
            [
                {"place": 0, "key": "Country", "func": get_player_country},
                {"place": 3, "func": get_player_team},
                {"place": 4, "func": get_player_links},
            ],
        )

    def get_player_info(self, playerName, results=False):
        player_object = DotaPlayer()
        playerName = player_object.process_playerName(playerName)
        soup, redirect_value = self.liquipedia.parse(playerName)
        if redirect_value is not None:
            playerName = redirect_value
        player = {}
        player["info"] = player_object.get_player_infobox(soup)
        player["links"] = player_object.get_player_links(soup)
        player["history"] = player_object.get_player_history(soup)
        player["achievements"] = player_object.get_player_achievements(soup)
        player["statistics"] = player_object.get_player_statistics(soup)
        if results:
            parse_value = playerName + "/Results"
            try:
                soup, __ = self.liquipedia.parse(parse_value)
            except ex.RequestsException:
                player["results"] = []
            else:
                player["results"] = player_object.get_player_achievements(soup)

        return player

    def get_teams(self, disbanded=False):
        soup = ""
        if disbanded:
            soup, _ = self.liquipedia.parse("Portal:Teams/Inactive")
        else:
            soup, __ = self.liquipedia.parse("Portal:Teams")
        teams = []

        templates = soup.find_all("span", class_="team-template-team-standard")
        for team in templates:
            team_details = {}
            team_spans = team.find_all("span")
            for span in team_spans:
                if span.has_attr("class"):
                    if (
                        "team-template-image-legacy" in span["class"]
                        or "team-template-image-icon" in span["class"]
                    ):
                        team_details["icon"] = (
                            self.image_base_url + span.find("img")["src"]
                        )
                    elif "team-template-text" in span["class"]:
                        team_details["name"] = span.text
            teams.append(team_details)
        return teams

    def get_team_info(self, teamName, results=False):
        # image not working
        team_object = DotaTeam()
        teamName = team_object.process_teamName(teamName)
        soup, redirect_value = self.liquipedia.parse(teamName)
        if redirect_value is not None:
            teamName = redirect_value
        team = {}
        team["info"] = team_object.get_team_infobox(soup)
        team["links"] = team_object.get_team_links(soup)
        team["cups"] = team_object.get_team_cups(soup)
        # TO-DO roster,org,former roster,results,matches
        # team["team_roster"] = team_object.get_team_roster(soup)
        # if results:
        #     parse_value = teamName + "/Results"
        #     try:
        #         soup, __ = self.liquipedia.parse(parse_value)
        #     except ex.RequestsException:
        #         team["results"] = []
        #     else:
        #         team["results"] = team_object.get_team_achivements(soup)

        return team

    # def get_transfers(self):
    #     transfers = []
    #     soup, __ = self.liquipedia.parse("Portal:Transfers")
    #     indexes = soup.find("div", class_="divHeaderRow")
    #     index_values = []
    #     for cell in indexes.find_all("div"):
    #         index_values.append(cell.get_text())
    #     rows = soup.find_all("div", class_="divRow")
    #     for row in rows:
    #         transfer = {}
    #         cells = row.find_all("div", class_="divCell")
    #         for i in range(0, len(cells)):
    #             key = index_values[i]
    #             value = cells[i].get_text()
    #             if key == "Player":
    #                 value = [val for val in value.split(" ") if len(val) > 0]
    #             if key == "Previous" or key == "Current":
    #                 try:
    #                     value = cells[i].find("a").get("title")
    #                 except AttributeError:
    #                     value = "None"
    #             transfer[key] = value
    #         transfer = {k: v for k, v in transfer.items() if len(k) > 0}
    #         transfers.append(transfer)

    #     return transfers

    # def get_upcoming_and_ongoing_games(self):
    #     games = []
    #     soup, __ = self.liquipedia.parse("Liquipedia:Upcoming_and_ongoing_matches")
    #     matches = soup.find_all("table", class_="infobox_matches_content")
    #     for match in matches:
    #         game = {}
    #         cells = match.find_all("td")
    #         try:
    #             game["team1"] = (
    #                 cells[0]
    #                 .find("span", class_="team-template-image")
    #                 .find("a")
    #                 .get("title")
    #             )
    #             game["format"] = cells[1].find("abbr").get_text()
    #             game["team2"] = (
    #                 cells[2]
    #                 .find("span", class_="team-template-image")
    #                 .find("a")
    #                 .get("title")
    #             )
    #             game["start_time"] = (
    #                 cells[3].find("span", class_="timer-object").get_text()
    #             )
    #             game["tournament"] = cells[3].find("div").a["title"]
    #             game["tournament_short_name"] = cells[3].find("div").get_text().rstrip()
    #             try:
    #                 game["twitch_channel"] = (
    #                     cells[3]
    #                     .find("span", class_="timer-object")
    #                     .get("data-stream-twitch")
    #                 )
    #             except AttributeError:
    #                 pass
    #             games.append(game)
    #         except AttributeError:
    #             continue

    #     return games

    # def get_heros(self):
    #     heros = []
    #     soup, __ = self.liquipedia.parse("Portal:Heroes")
    #     list_elements = soup.find_all("li")
    #     for list_element in list_elements:
    #         hero = {}
    #         try:
    #             hero["image"] = self.__image_base_url + list_element.find("img").get(
    #                 "src"
    #             )
    #             hero["name"] = list_element.find("span").get_text()
    #             heros.append(hero)
    #         except AttributeError:
    #             pass

    #     return heros

    # def get_items(self):
    #     items = []
    #     soup, __ = self.liquipedia.parse("Portal:Items")
    #     item_divs = soup.find_all("div", class_="responsive")
    #     for item_div in item_divs:
    #         item = {}
    #         item["image"] = self.__image_base_url + item_div.find_all("img")[0].get(
    #             "src"
    #         )
    #         item["name"] = item_div.find_all("a")[1].get_text()
    #         try:
    #             item["price"] = item_div.find("b").get_text()
    #         except AttributeError:
    #             pass
    #         items.append(item)

    #     return items

    # def get_patches(self):
    #     patches = []
    #     soup, __ = self.liquipedia.parse("Portal:Patches")
    #     tables = soup.find_all("table")
    #     for table in tables:
    #         rows = table.find("tbody").find_all("tr")
    #         indexes = rows[0]
    #         index_values = []
    #         for cell in indexes.find_all("td"):
    #             index_values.append(cell.get_text().rstrip())
    #         rows = rows[1:]
    #         for row in rows:
    #             patch = {}
    #             cells = row.find_all("td")
    #             for i in range(0, len(cells)):
    #                 key = index_values[i]
    #                 value = cells[i].get_text().rstrip()
    #                 if key == "Highlights":
    #                     value = [
    #                         unicodedata.normalize("NFKD", val)
    #                         for val in cells[i].get_text().split("\n")
    #                         if len(val) > 0
    #                     ]
    #                 patch[key] = value
    #             patches.append(patch)

    #     return patches

    # def get_tournaments(self, tournamentType=None):
    #     tournaments = []
    #     if tournamentType is None:
    #         page_val = "Portal:Tournaments"
    #     elif tournamentType == "Show Matches":
    #         page_val = "Show_Matches"
    #     else:
    #         page_val = tournamentType.capitalize() + "_Tournaments"
    #     soup, __ = self.liquipedia.parse(page_val)
    #     div_rows = soup.find_all("div", class_="divRow")
    #     for row in div_rows:
    #         tournament = {}

    #         values = row.find("div", class_="divCell Tournament Header")
    #         if tournamentType is None:
    #             tournament["tier"] = values.a.get_text()
    #             tournament["name"] = values.b.get_text()
    #         else:
    #             tournament["tier"] = tournamentType

    #         try:
    #             tournament["icon"] = self.__image_base_url + row.find(
    #                 "div", class_="divCell Tournament Header"
    #             ).find("img").get("src")
    #         except AttributeError:
    #             pass

    #         try:
    #             tournament["page"] = self.__image_base_url + values.b.a["href"]
    #         except AttributeError:
    #             pass

    #         tournament["dates"] = (
    #             row.find("div", class_="divCell EventDetails Date Header")
    #             .get_text()
    #             .strip()
    #         )

    #         try:
    #             tournament["prize_pool"] = int(
    #                 row.find("div", class_="divCell EventDetails Prize Header")
    #                 .get_text()
    #                 .rstrip()
    #                 .replace("$", "")
    #                 .replace(",", "")
    #             )
    #         except (AttributeError, ValueError):
    #             tournament["prize_pool"] = 0

    #         tournament["teams"] = re.sub(
    #             "[A-Za-z]",
    #             "",
    #             row.find(
    #                 "div", class_="divCell EventDetails PlayerNumber Header"
    #             ).get_text(),
    #         ).rstrip()
    #         location_list = unicodedata.normalize(
    #             "NFKD",
    #             row.find("div", class_="divCell EventDetails Location Header")
    #             .get_text()
    #             .strip(),
    #         ).split(",")
    #         tournament["host_location"] = location_list[0]

    #         winner = row.find("div", class_="divCell Placement FirstPlace")
    #         if winner:
    #             tournament["winner"] = winner.get_text().strip()
    #             tournament["runner_up"] = (
    #                 row.find("div", class_="divCell Placement SecondPlace")
    #                 .get_text()
    #                 .strip()
    #             )
    #         else:
    #             tournament["winner"] = "TBD"
    #             tournament["runner_up"] = "TBD"

    #         tournaments.append(tournament)

    #     return tournaments

    # def get_tournament_baner(self, tournament_page):
    #     try:
    #         page, __ = self.liquipedia.parse(
    #             tournament_page.replace("https://liquipedia.net/dota2/", "")
    #         )

    #         return f"https://liquipedia.net{page.find('div',class_='infobox-image').div.div.a.img['src']}"

    #     except AttributeError:
    #         pass

    # def get_pro_circuit_details(self):
    #     soup, __ = self.liquipedia.parse("Dota_Pro_Circuit/2018-19/Rankings/Full")
    #     pro_circuit = {}
    #     circuit_object = dota_pro_circuit()
    #     pro_circuit["rankings"] = circuit_object.get_rankings(soup)
    #     soup, __ = self.liquipedia.parse("Dota_Pro_Circuit/2018-19/Schedule")
    #     pro_circuit["schedule"] = circuit_object.get_schedule(soup)

    #     return pro_circuit
