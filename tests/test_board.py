from board import Board
import curses
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_screen():
    screen = Mock()
    screen.getch = Mock(return_value=ord("q"))  # Simulate a keypress
    screen.getmaxyx = Mock(return_value=(20, 20))
    screen.getstr = Mock(return_value=b"Mocky Mock")  # Return bytes, not str
    return screen


def test_board_initialization(mock_screen):
    board = Board(mock_screen)
    assert board.screen == mock_screen


def test_board_clear(mock_screen):
    board = Board(mock_screen)
    board.clear()
    mock_screen.clear.assert_called_once()


def test_board_draw_box(mock_screen):
    def setUp(self):
        src.board.curses = Mock()

    def test_function(self):
        board = Board(mock_screen)
        box = board.draw_box(10, 10)
        assert isinstance(box, Board)


def test_board_message(mock_screen):
    board = Board(mock_screen)
    board.message("Test Message")
    mock_screen.addstr.assert_called_with(0, 0, "Test Message", 0)


def test_board_get_game_length(mock_screen):
    mock_screen.getch = Mock(return_value=52)  # Simulate '4' key
    # Simulate unique names for each player
    mock_screen.getstr = Mock(side_effect=[b"A", b"B", b"C", b"D"])
    board = Board(mock_screen)
    players, length, players_names = board.get_game_params()
    assert players == 4 and length == 4 and players_names == ["A", "B", "C", "D"]
