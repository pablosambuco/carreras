import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_screen():
    screen = Mock()
    screen.getch = Mock(return_value=ord('q'))
    screen.getmaxyx = Mock(return_value=(20, 20))
    return screen

