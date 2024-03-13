from liquipediapy import dota


def test_get_players():
    app = dota("test")
    players = app.get_players()
    assert len(players) > 0
    first_player = players[0]
    assert first_player["Name"] == "Visar Zymberi"
