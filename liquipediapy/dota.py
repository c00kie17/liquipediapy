import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
import re
from liquipediapy.dota_modules.player import DotaPlayer
from liquipediapy.dota_modules.team import DotaTeam
from liquipediapy.dota_modules.tournament import DotaTournament
from liquipediapy.dota_modules.pro_circuit import DotaProCircuit
from liquipediapy.dota_modules.common import DotaCommon
from datetime import datetime
import unicodedata


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
            self.handle_header_wikitable,
            self.handle_row_wikitable,
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

    def get_team_info(self, teamName, results=False, matches=False):
        team_object = DotaTeam()
        teamName = team_object.process_teamName(teamName)
        soup, redirect_value = self.liquipedia.parse(teamName)
        if redirect_value is not None:
            teamName = redirect_value
        team = {}
        team["info"] = team_object.get_team_infobox(soup)
        team["links"] = team_object.get_team_links(soup)
        team["cups"] = team_object.get_team_cups(soup)
        team["team_roster"] = team_object.get_team_roster(soup)
        team["organization"] = team_object.get_team_org(soup)
        team["former_team"] = team_object.get_former_team(soup)

        achievements_table = (
            soup.find_all("div", {"class": "tabs-dynamic"})[-1]
            .find("div", {"class": "content1"})
            .find("table", {"class": "wikitable-striped"})
        )
        team["achievements"] = team_object.get_team_achivements(achievements_table)

        results_table = (
            soup.find_all("div", {"class": "tabs-dynamic"})[-1]
            .find("div", {"class": "content2"})
            .find("table", {"class": "wikitable-striped"})
        )
        team["matches"] = team_object.get_team_matches(results_table)

        if results:
            parse_value = teamName + "/Results"
            try:
                soup, __ = self.liquipedia.parse(parse_value)
            except ex.RequestsException:
                team["results"] = []
            else:
                table = soup.find("table", {"class": "wikitable-striped"})
                team["results"] = team_object.get_team_achivements(table)

        if matches:
            parse_value = teamName + "/Played_Matches"
            try:
                soup, __ = self.liquipedia.parse(parse_value)
            except ex.RequestsException:
                team["detailed_matches"] = []
            else:
                matches = []
                tables = soup.find_all("table", {"class": "wikitable-striped"})
                for table in tables:
                    matches += team_object.get_team_matches(table)
                team["detailed_matches"] = matches

        return team

    def __get_transfer_page(self, year):
        now = datetime.now()
        if year < 2012:
            year = "Pre_2012"

        assert year <= now.year

        return "Transfers/" + str(year)

    def get_transfers(self, year=None):

        if year is None:
            page = "Portal:Transfers"
        else:
            page = self.__get_transfer_page(year)

        soup, __ = self.liquipedia.parse(page)
        tables = soup.find_all("div", {"class": "divTable"})
        data = []

        def handle_players(data):
            found_players = []
            player_countries = data.find_all("span", {"class": "flag"})
            player_names = data.find_all("a", recursive=False)
            for i in range(0, len(player_names)):
                player_data = {}
                player_data["country"] = player_countries[i].find("a").get("title")
                player_data["name"] = player_names[i].text
                found_players.append(player_data)
            return found_players

        def handle_old_new_team(data):
            team = data.find("a")
            print(team)
            if team is not None:
                return team["title"]
            else:
                return data.text

        def handle_ref(data):
            return data.find("a").get("href")

        for table in tables:
            data += self.read_div_table(
                table,
                self.handle_header_div_table,
                self.handle_row_div_table,
                [
                    {"place": 1, "func": handle_players},
                    {"place": 2, "func": handle_old_new_team},
                    {"place": 4, "func": handle_old_new_team},
                    {"place": 5, "func": handle_ref, "key": "Ref"},
                ],
            )
        return data

    def get_upcoming_and_ongoing_games(self):
        games = {}
        soup, __ = self.liquipedia.parse("Liquipedia:Upcoming_and_ongoing_matches")
        contents = (
            soup.find("div", {"class": "matches-list"})
            .find("div", {"style": ""})
            .find_all("div", recursive=False)
        )
        headers = ["all_upcoming", "featured_matches", "recently_completed"]
        for i, content in enumerate(contents):
            header = headers[i]
            match_list = content.find_all("table", recursive=False)
            games[header] = self.read_match_list(match_list)
        return games

    def get_heros(self):
        all_heros = []
        attributes = ["strength", "agility", "intelligence"]
        soup, __ = self.liquipedia.parse("Portal:Heroes")
        hero_groups = soup.find_all("ul", {"class": "halfbox"})
        for i, group in enumerate(hero_groups):
            heros = group.find_all("li")
            for hero in heros:
                hero_data = {}
                hero_data["name"] = hero.find("a")["title"]
                hero_data["image"] = self.image_base_url + hero.find("img")["src"]
                hero_data["attribute"] = attributes[i]
                all_heros.append(hero_data)

        return all_heros

    def get_items(self):
        items = []
        soup, __ = self.liquipedia.parse("Portal:Items")
        item_divs = soup.find_all("div", class_="responsive")
        for item_div in item_divs:
            item = {}
            item["image"] = self.image_base_url + item_div.find_all("img")[0].get("src")
            item["name"] = item_div.find_all("a")[1].get_text()
            try:
                item["price"] = item_div.find("b").get_text()
            except AttributeError:
                pass
            items.append(item)

        return items

    def get_patches(self):
        patches = []
        soup, __ = self.liquipedia.parse("Portal:Patches")
        patch_tables = soup.find_all("table", {"class": "wikitable"})
        for table in patch_tables:
            rows = table.find_all("tr")
            header = rows[0]
            rows = rows[1:]

            header_keys = []
            header_data = header.find_all("td")
            for data in header_data:
                header_keys.append(data.text.strip())

            if len(header_keys) == 0:
                continue

            for row in rows:
                patch = {}
                row_data = row.find_all("td")
                for i, data in enumerate(row_data):
                    if header_keys[i] == "Highlights":
                        update_data = []
                        try:
                            updates = data.find("ul").find_all("li", recursive=False)
                        except AttributeError:
                            continue
                        for update in updates:
                            update_data.append(
                                unicodedata.normalize(
                                    "NFKD", update.text.strip().replace("\n", "")
                                )
                            )
                        patch[header_keys[i]] = update_data
                    else:
                        patch[header_keys[i]] = data.text.strip()
                patches.append(patch)
        return patches

    def get_tournaments(self, tier=None, year_string=""):
        tournaments = []
        if tier is None:
            tier = "Recent_Tournament_Results"
        else:
            tier = "Tier_" + str(tier) + "_Tournaments"

        page = tier + "/" + year_string
        soup, __ = self.liquipedia.parse(page)

        def handle_tournament_icon(data):
            return self.image_base_url + data.find("img")["src"]

        def handle_teams(data):
            return data.find(text=True, recursive=False)

        def handle_team_icon(data):
            span = data.find(
                "span",
                {"class": ["team-template-image-icon", "team-template-image-legacy"]},
            )
            if span is None:
                return ""
            else:
                return self.image_base_url + span.find("img")["src"]

        def handle_tournament_url(data):
            a = data.find_all("a")[-1]
            return self.image_base_url + a["href"]

        tables = soup.find_all("div", {"class": "divTable"})
        for table in tables:

            data = self.read_div_table(
                table,
                self.handle_header_div_table,
                self.handle_row_div_table,
                [
                    {
                        "place": 0,
                        "key": "tournament_icon",
                        "func": handle_tournament_icon,
                        "add": True,
                    },
                    {
                        "place": 0,
                        "key": "Tournament",
                    },
                    {
                        "place": 0,
                        "key": "tournament_url",
                        "func": handle_tournament_url,
                        "add": True,
                    },
                    {"place": 3, "key": "teams", "func": handle_teams},
                    {
                        "place": 5,
                        "key": "winner_icon",
                        "func": handle_team_icon,
                        "add": True,
                    },
                    {
                        "place": 6,
                        "key": "runner_up_icon",
                        "func": handle_team_icon,
                        "add": True,
                    },
                ],
            )

            tournaments += data
        return tournaments

    def get_tournament_info(self, tournament_url):
        tournament = {}
        tournament_obj = DotaTournament()
        soup, __ = self.liquipedia.parse(tournament_url)

        tournament["info"] = tournament_obj.get_tournament_infobox(soup)
        tournament["prizepool"] = tournament_obj.get_prizepool_table(soup)
        tournament["participants"] = tournament_obj.get_tournament_participants(soup)
        tournament["matches"] = tournament_obj.get_tournament_bracket_matches(soup)

        return tournament

    # def get_pro_circuit_details(self):
    #     soup, __ = self.liquipedia.parse("Dota_Pro_Circuit/2018-19/Rankings/Full")
    #     pro_circuit = {}
    #     circuit_object = dota_pro_circuit()
    #     pro_circuit["rankings"] = circuit_object.get_rankings(soup)
    #     soup, __ = self.liquipedia.parse("Dota_Pro_Circuit/2018-19/Schedule")
    #     pro_circuit["schedule"] = circuit_object.get_schedule(soup)

    #     return pro_circuit
