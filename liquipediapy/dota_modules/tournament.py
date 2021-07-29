from liquipediapy.dota_modules.common import DotaCommon
import unicodedata
import re


class DotaTournament(DotaCommon):
    def __init__(self):
        super().__init__()

    def get_tournament_infobox(self, soup):
        info = {}

        image = soup.find("div", {"class": "infobox-image"})
        info["image"] = self.image_base_url + image.find("img")["src"]

        info_cells = soup.find_all("div", {"class", "infobox-cell-2"})
        for i in range(0, len(info_cells), 2):
            header = info_cells[i].text.replace(":", "")
            value = unicodedata.normalize("NFKD", info_cells[i + 1].text.strip())
            if header == "Sponsor":
                value = value.split("•")

            info[header] = value

        links = soup.find("div", {"class": "infobox-icons"}).find_all("a")
        found_links = []
        for link in links:
            link_href = link.get("href")
            domain = re.search(
                "https?://(www.)?([A-Za-z_0-9.-]+).com/.*",
                link_href,
            )
            if domain:
                found_links.append({"domain": domain.group(2), "link": link_href})
        info["links"] = found_links

        return info

    def get_prizepool_table(self, soup):
        prizepool = []
        table = soup.find("table", {"class": "prizepooltable"})

        rows = table.find_all("tr")
        header = rows[0]
        rows = rows[1:]

        header_values = []
        for head in header.find_all("th"):
            header_values.append(head.text.strip())

        place = 1
        for row in rows:
            entry = {}
            data = row.find_all("td")
            for i, header in enumerate(header_values):
                if i == 0:
                    entry[header] = place
                else:
                    if len(data) < len(header_values):
                        if i == len(header_values) - 1:
                            entry[header] = data[0].text.strip()
                        else:
                            entry[header] = prizepool[-1][header]
                    else:
                        entry[header] = data[i].text.strip()

            place += 1
            prizepool.append(entry)
        return prizepool

    def get_tournament_participants(self, soup):
        teams = []
        team_cards = soup.find_all("div", {"class": "teamcard"})

        for team in team_cards:
            team_info = {}
            team_info["name"] = team.find("center").find("a").text
            members = team.find("table", {"class": "wikitable"}).find_all("tr")
            team_members = []
            for member in members:
                info = {}
                a = member.find("td").find("a", recursive=False)
                if a is not None:
                    info["name"] = a.text
                    info["url"] = self.image_base_url + a["href"]
                    try:
                        info["country"] = (
                            member.find("span", {"class": "flag"})
                            .find("a")
                            .get("title")
                        )
                    except AttributeError:
                        pass
                    team_members.append(info)
            team_info["members"] = team_members
            teams.append(team_info)
        return teams

    def get_tournament_bracket_matches(self, soup):
        all_matches = []
        matches = soup.find_all("div", {"class": "bracket-game"})

        for match in matches:
            match_data = {}
            time_popup = match.find("div", {"class": "bracket-popup-body-time"})
            if time_popup is None:
                continue

            match_data["time"] = time_popup.text
            match_data["teams"] = []
            match_data["team_score"] = []
            teams = match.find_all(
                "div",
                {"class": ["bracket-cell-r1", "bracket-cell-r2", "bracket-cell-r3"]},
            )
            for team in teams:
                name_template = team.find("span", {"class": "team-template-text"})
                if name_template is None:
                    continue
                match_data["teams"].append(name_template.text)
                match_data["team_score"].append(
                    team.find("div", {"class": "bracket-score"}).text
                )

            links = match.find("div", {"class": "plainlinks"})
            if links:
                links = links.find_all("a")
                found_links = []
                for link in links:
                    link_href = link.get("href")
                    domain = re.search(
                        "https?://(www.)?([A-Za-z_0-9.-]+).com/.*",
                        link_href,
                    )
                    if domain:
                        found_links.append(
                            {
                                "domain": domain.group(2),
                                "link": link_href,
                                "title": link.get("title"),
                            }
                        )
                match_data["links"] = found_links

            all_matches.append(match_data)
        return all_matches
