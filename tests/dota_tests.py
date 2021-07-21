import unittest
from liquipediapy import dota
from liquipediapy.exceptions import RequestsException


class DotaTestsGetPlayers(unittest.TestCase):
    def setUp(self):
        self.dota = dota(
            "appname",
        )

    def test_get_players_pass(self):
        players = self.dota.get_players()
        self.assertGreater(len(players), 0)


class DotaTestsGetPlayer(unittest.TestCase):
    def setUp(self):
        self.dota = dota(
            "appname",
        )

    def test_get_player_pass(self):
        player = self.dota.get_player_info("Arteezy")
        self.assertIsNotNone(player)
        self.assertFalse("results" in player)

    def test_get_player_fail(self):
        with self.assertRaises(RequestsException) as context:
            self.dota.get_player_info("tch334")

    def test_get_player_with_achivements_pass(self):
        player = self.dota.get_player_info("Arteezy", True)
        self.assertIsNotNone(player)
        self.assertGreater(len(player["results"]), 0)


class DotaTestsGetTeams(unittest.TestCase):
    def setUp(self):
        self.dota = dota(
            "appname",
        )

    def test_get_teams_pass(self):
        teams = self.dota.get_teams(False)
        self.assertGreater(len(teams), 0)

    def test_get_teams_disbanded_pass(self):
        teams = self.dota.get_teams(True)
        self.assertGreater(len(teams), 0)


if __name__ == "__main__":
    unittest.main()