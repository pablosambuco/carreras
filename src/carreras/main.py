"""Main"""

import argparse

from carreras.board import Board

# Intenta importar pygame, si falla, usa curses
try:
    import pygame  # noqa: F401
    from carreras.graphicboard import GraphicBoard

    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

from carreras.game import Game


def get_game_parameters(board: Board) -> tuple[int, int, list[str]]:
    """Obtiene los parámetros del juego desde el tablero."""
    try:
        players, length, players_names = board.get_game_params()
        return players, length, players_names
    except Exception as e:
        print(f"Error al obtener los parámetros del juego: {e}")
        return None, None, None


def iniciar_juego(
    board: Board,
    players: int,
    length: int,
    players_names: list[str],
) -> Game:
    """Inicia un nuevo juego."""
    game = Game(players, length, players_names)
    board.draw_game(game)
    return game


def run_game_loop(board: Board, game: Game) -> None:
    """Ejecuta el bucle principal del juego."""
    game_ended = False
    while not game_ended:
        game_ended = game.step()
        board.draw_game(game)


def handle_restart(board: Board) -> tuple[bool, int, int, list[str]]:
    """Maneja la lógica de reinicio del juego."""
    restart, same_params = board.ask_restart()
    if restart and same_params:
        # Reutilizar los mismos parámetros (no pedirlos de nuevo)
        return restart, None, None, None
    if restart and not same_params:
        players, length, players_names = board.get_game_params()
        return restart, players, length, players_names
    return restart, None, None, None


def main():
    """Función principal del juego."""
    parser = argparse.ArgumentParser(description="CARRERAS - Horse Racing Game")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Usar interfaz gráfica (pygame) en vez de curses",
    )
    parser.add_argument(
        "--lang",
        choices=["es", "en"],
        default="es",
        help="Idioma del juego: es (Español, por defecto) o en (English)",
    )
    args = parser.parse_args()

    from carreras.i18n import set_language

    set_language(args.lang)

    if args.gui:
        if HAS_PYGAME:
            board = GraphicBoard()
        else:
            print(
                "Pygame no está instalado. Usando interfaz de texto (curses) en su lugar."
            )
            board = Board()
    else:
        board = Board()

    restart = True
    players, length, players_names = board.get_game_params()
    # Guardar los parámetros originales para reinicio rápido
    orig_players, orig_length, orig_names = players, length, players_names

    while restart:
        if players is None:
            break  # Salir del bucle si hubo un error al obtener los parámetros

        game = iniciar_juego(board, players, length, players_names)
        run_game_loop(board, game)
        restart, new_players, new_length, new_names = handle_restart(board)
        if restart:
            if new_players is None and new_length is None and new_names is None:
                # Reutilizar los originales
                players, length, players_names = orig_players, orig_length, orig_names
            else:
                players, length, players_names = new_players, new_length, new_names
                orig_players, orig_length, orig_names = players, length, players_names

    board.destroy()


if __name__ == "__main__":
    main()
