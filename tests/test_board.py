from src.board import Board
import curses
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_screen():
    screen = Mock()
    screen.getch = Mock(return_value=ord('q'))  # Simulate a keypress
    screen.getmaxyx = Mock(return_value=(20, 20))
    return screen

def test_board_initialization(mock_screen):
    board = Board(mock_screen)
    assert board.screen == mock_screen

def test_board_clear(mock_screen):
    board = Board(mock_screen)
    board.clear()
    mock_screen.clear.assert_called_once()

def test_board_draw_box(mock_screen):
    board = Board(mock_screen)
    box = board.draw_box(10, 10)
    assert isinstance(box, Board)

def test_board_message(mock_screen):
    board = Board(mock_screen)
    board.message("Test Message")
    mock_screen.addstr.assert_called_with(0, 0, "Test Message", 0)

def test_board_get_game_length(mock_screen):
    mock_screen.getch = Mock(return_value=52)  # Simulate '4' key
    board = Board(mock_screen)
    length = board.get_game_length()
    assert length == 4
