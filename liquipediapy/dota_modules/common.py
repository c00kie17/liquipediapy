import unicodedata


class DotaCommon:
    def __init__(self):
        self.image_base_url = "https://liquipedia.net"

    def __verify_wikitable(self, table):
        assert table.name == "table"
        assert "wikitable" in table["class"]
        # assert "wikitable-striped" not in table["class"]

    def __fetch_entry_settings(self, index, settings):
        for setting in settings:
            if setting["place"] == index:
                return setting
        return None

    def read_wikitable(self, table, settings):
        self.__verify_wikitable(table)

        wikitable_headers = []
        headers = table.find_all("th")
        for header in headers:
            wikitable_headers.append(unicodedata.normalize("NFKD", header.text.strip()))

        wikitable_data = []
        rows = table.find_all("tr")
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
                setting = self.__fetch_entry_settings(i, settings)
                if setting is not None:
                    if "key" in setting:
                        key = setting["key"]
                    if "func" in setting:
                        value = setting["func"](data_value)
                    if "skip" in setting and setting["skip"]:
                        increment_head = False
                parsed_data[key] = value
                if increment_head:
                    head_counter += 1
            wikitable_data.append(parsed_data)

        return wikitable_data
