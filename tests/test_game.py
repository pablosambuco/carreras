from game import Game
from deck import Deck

def test_game_initialization():
    game = Game(3,5,["Mock1","Mock2","Mock3"])
    assert isinstance(game.deck, Deck)
    assert game.players == 3
    assert len(game.players_names) == 3
    assert len(game.knights) == 3
    assert len(game.steps) == 5

def test_game_move_knights():
    game = Game(5)
    initial_rows = [knight["row"] for knight in game.knights.values()]
    game.move_knights("golds", 1)
    updated_rows = [knight["row"] for knight in game.knights.values()]
    assert updated_rows != initial_rows

def test_game_step():
    game = Game(5)
    ended = game.step()
    assert isinstance(ended, bool)

