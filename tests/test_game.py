"""Tests for the Game class."""

from carreras.game import Game
from carreras.deck import Deck

def test_game_initialization():
    """Test Game initialization and attributes."""
    game = Game(3,5,["Mock1","Mock2","Mock3"])
    assert isinstance(game.deck, Deck)
    assert game.players == 3
    assert len(game.players_names) == 3
    assert len(game.knights) == 3
    assert len(game.steps) == 5

def test_game_move_knights():
    """Test moving knights by suit and step."""
    game = Game(5)
    initial_rows = [knight["row"] for knight in game.knights.values()]
    game.move_knights("coins", 1)
    updated_rows = [knight["row"] for knight in game.knights.values()]
    assert updated_rows != initial_rows

def test_game_step():
    """Test a single step in the Game."""
    game = Game(5)
    ended = game.step()
    assert isinstance(ended, bool)

