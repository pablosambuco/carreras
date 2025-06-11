"""Parameter input mixin for board classes (curses/pygame)."""

from .i18n import tr

class ParamInputMixin:
    """Mixin para entrada de parámetros del juego (jugadores, nombres, largo)."""
    def ask_player_count(self) -> int:
        """Solicita la cantidad de jugadores al usuario."""
        raise NotImplementedError

    def ask_player_names(self, count: int) -> list[str]:
        """Solicita los nombres de los jugadores al usuario."""
        raise NotImplementedError

    def ask_race_length(self) -> int:
        """Solicita la longitud de la carrera al usuario."""
        raise NotImplementedError

    def get_game_params(self) -> tuple[int, int, list[str]]:
        """Obtiene todos los parámetros del juego: jugadores, nombres y largo."""
        raise NotImplementedError