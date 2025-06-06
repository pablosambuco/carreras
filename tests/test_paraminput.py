import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from paraminput import ParamInputMixin

class DummyParamInput(ParamInputMixin):
    def __init__(self, player_count=2, player_names=None, race_length=4):
        self._player_count = player_count
        self._player_names = player_names or ["A", "B"]
        self._race_length = race_length
    def ask_player_count(self):
        return self._player_count
    def ask_player_names(self, count):
        return self._player_names[:count]
    def ask_race_length(self):
        return self._race_length

def test_paraminput_get_game_params():
    dummy = DummyParamInput(player_count=3, player_names=["X", "Y", "Z"], race_length=6)
    players, length, names = dummy.get_game_params()
    assert players == 3
    assert length == 6
    assert names == ["X", "Y", "Z"]
