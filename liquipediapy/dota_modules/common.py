import unicodedata
from datetime import datetime


class DotaCommon:
    def __init__(self):
        self.image_base_url = "https://liquipedia.net"

    def get_span_class(self, spans, class_name):
        found_spans = []
        for span in spans:
            if span.has_attr("class"):
                if class_name in span["class"]:
                    found_spans.append(span)
        return found_spans

    def __verify_wikitable(self, table):
        assert table.name == "table"
        assert "wikitable" in table["class"]

    def __fetch_entry_settings(self, index, settings):
        index_settings = []
        for setting in settings:
            if setting["place"] == index:
                index_settings.append(setting)

        main_setting = [
            setting
            for setting in index_settings
            if "add" not in setting or not setting["add"]
        ]
        added_settings = [
            setting for setting in index_settings if "add" in setting and setting["add"]
        ]

        if len(main_setting) == 0:
            main_setting = None
        else:
            main_setting = main_setting[0]

        return main_setting, added_settings

    def handle_header_wikitable(self, table):
        headers = table.find_all("th")
        found_headers = []
        for header in headers:
            found_headers.append(unicodedata.normalize("NFKD", header.text.strip()))
        return found_headers

    def handle_row_wikitable(self, table):
        return table.find_all("tr")

    def read_wikitable(self, table, header_func, row_func, settings=[]):
        self.__verify_wikitable(table)

        wikitable_headers = header_func(table)
        wikitable_data = []
        rows = row_func(table)
        for row in rows:
            data = row.find_all("td")
            if len(data) == 0:
                continue
            parsed_data = {}
            head_counter = 0
            for i, data_value in enumerate(data):
                increment_head = True
                try:
                    key = wikitable_headers[head_counter]
                except IndexError:
                    key = ""

                value = data_value.text.strip()
                setting, added_settings = self.__fetch_entry_settings(i, settings)
                if setting is not None:
                    if "key" in setting:
                        key = setting["key"]
                    if "func" in setting:
                        value = setting["func"](data_value)
                    if "skip" in setting and setting["skip"]:
                        increment_head = False

                if key == "":
                    continue

                parsed_data[key] = value

                for added_setting in added_settings:
                    parsed_data[added_setting["key"]] = added_setting["func"](
                        data_value
                    )

                if increment_head:
                    head_counter += 1
            wikitable_data.append(parsed_data)

        return wikitable_data

    def handle_header_roster_card(self, table):
        header = table.find("tr", {"class", "HeaderRow"})
        headers = []
        for column in header.find_all("th"):
            headers.append(unicodedata.normalize("NFKD", column.text.strip()))
        return headers

    def handle_row_roster_card(self, table):
        return table.find("tr", {"class", "Player"})

    def __verify_div_table(self, table):
        assert table.name == "div"
        assert "divTable" in table["class"]

    def read_div_table(self, table, header_func, row_func, settings=[]):
        self.__verify_div_table(table)

        div_table_headers = header_func(table)
        div_table_data = []
        rows = row_func(table)
        for row in rows:
            data = row.find_all("div")
            if len(data) == 0:
                continue
            parsed_data = {}
            head_counter = 0
            for i, data_value in enumerate(data):
                increment_head = True
                try:
                    key = div_table_headers[head_counter]
                except IndexError:
                    key = ""

                value = data_value.text.strip()
                setting, added_settings = self.__fetch_entry_settings(i, settings)
                if setting is not None:
                    if "key" in setting:
                        key = setting["key"]
                    if "func" in setting:
                        value = setting["func"](data_value)
                    if "skip" in setting and setting["skip"]:
                        increment_head = False

                if key != "":
                    parsed_data[key] = value

                    for added_setting in added_settings:
                        parsed_data[added_setting["key"]] = added_setting["func"](
                            data_value
                        )

                if increment_head:
                    head_counter += 1

            div_table_data.append(parsed_data)

        return div_table_data

    def handle_header_div_table(self, table):
        header = table.find("div", {"class", "divHeaderRow"})
        headers = []
        for column in header.find_all("div", {"class": "divCell"}):
            headers.append(unicodedata.normalize("NFKD", column.text.strip()))
        return headers

    def handle_row_div_table(self, table):
        return table.find_all("div", {"class", "divRow"})

    def read_match_list(self, matches):
        found_matches = []
        for match in matches:
            match_details = {}
            teams = [
                match.find("td", {"class": "team-left"}).find("span").find("a"),
                match.find("td", {"class": "team-right"}).find("span").find("a"),
            ]
            for i, team in enumerate(teams):
                try:
                    match_details["team" + str(i + 1)] = team["title"]
                    match_details["team" + str(i + 1) + "_logo"] = (
                        self.image_base_url + team["href"]
                    )
                except TypeError:
                    match_details["team" + str(i + 1)] = "TBD"

            vs = match.find("td", {"class": "versus"})
            if "vs" in vs.text:
                match_details["format"] = vs.text.strip().replace("vs", "").strip("()")

            else:
                match_details["result"] = vs.text.strip()

            footer = match.find("td", {"class": "match-filler"})
            match_details["time"] = datetime.strptime(
                footer.find("span", {"class": "match-countdown"}).text.replace(
                    "UTC", ""
                ),
                "%B %d, %Y - %H:%M ",
            )
            tournament = footer.find("span", {"class": "league-icon-small-image"}).find(
                "a"
            )
            match_details["tournament"] = tournament["title"]
            match_details["tournament_icon"] = self.image_base_url + tournament["href"]
            found_matches.append(match_details)
        return found_matches