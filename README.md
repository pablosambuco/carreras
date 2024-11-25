# Horse Racing Game

A terminal-based horse racing game written in Python using the `curses` library. The game involves moving horses based on card draws from a shuffled deck.

## Features

- Terminal-based UI with color support
- Interactive game with user inputs
- Customizable game length
- Real-time horse movements based on card draws

## Installation

To run this game, make sure you have Python 3.11 installed on your machine. You can install the required dependencies using `pip` and the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage 
Ensure you have set up the environment with the necessary dependencies. Refer to the [Installation](#installation) section for instructions on how to install the required packages.
To start the game, run the `carreras.py` file. 
```bash 
python -m src.main
```

## Game Rules

1. The game begins by asking the user to select the length of the race.
2. Each horse is represented by a suit (`golds`, `cups`, `swords`, `clubs`).
3. Horses move forward or backward based on the drawn card's suit.
4. The game ends when a horse crosses the finish line.

## Code Overview

### Card Class

Represents a single card in the deck.

### Deck Class

Represents the deck of cards, with functionality to shuffle and draw cards.

### Board Class

Handles the display and user interaction using the `curses` library.

### Game Class

Manages the game logic, including initializing the game, drawing the game board, and moving horses.

## Future Improvements 
- **Modularization:** The game will be split into several modules to improve portability and facilitate integration with other graphical interfaces. This will make the game more flexible and easier to extend.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by classic card games and the need for interactive terminal-based games.
- Developed with the help of the Python `curses` library for terminal handling.

## Contact

If you have any questions or feedback, keep it to yourself XD
