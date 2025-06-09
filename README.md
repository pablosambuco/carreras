# Horse Racing Game

A horse racing game written in Python. You can play it in the terminal (curses) or with a graphical interface (pygame).

## Features

- Terminal-based UI with color support (curses)
- Graphical UI with pygame (`--gui`)
- Interactive game with user inputs
- Customizable game length
- Horse movements based on card draws
- Automated tests with pytest

## Installation

Requires Python 3.10 or newer.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Terminal (curses) interface

```bash
python -m src.carreras.main
```

### Graphical (pygame) interface

```bash
python -m src.carreras.main --gui
```

### Language selection

You can select the language (Spanish or English) with the `--lang` parameter:

```bash
python -m src.carreras.main --lang es   # Spanish (default)
python -m src.carreras.main --lang en   # English
```

You can combine with `--gui`:

```bash
python -m src.carreras.main --gui --lang en
```

## Game Rules

1. The game begins by asking the user to select the number of players, their names and the length of the race.
2. Each horse is represented by a suit (`coins`, `cups`, `swords`, `clubs`).
3. Horses move forward or backward based on the drawn card's suit.
4. The game ends when a horse crosses the finish line.

## Code Overview

### Card Class

Represents a single card in the deck.

### Deck Class

Represents the deck of cards, with functionality to shuffle and draw cards.

### Board Class

Handles the display and user interaction using the `curses` library.

### GraphicBoard Class

Handles the display and user interaction using the `pygame` library.

### Game Class

Manages the game logic, including initializing the game and moving horses.

## Testing

Run all tests with:

```bash
pytest
```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by classic card games and the need for interactive terminal-based games.
- Developed with the help of the Python `curses` and `pygame` libraries for UI handling.

## Contact

If you have any questions or feedback, keep it to yourself XD
