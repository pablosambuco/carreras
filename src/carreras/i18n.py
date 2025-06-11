"""Internationalization (i18n) support for carreras game."""

import threading

_LANG = "es"
_LOCK = threading.Lock()

# Translation dictionaries
TRANSLATIONS = {
    "es": {
        # General
        "CARRERAS": "CARRERAS",
        "RACES": "CARRERAS",
        "Press Q to quit": "Presiona Q para salir del juego",
        "Press 2, 3, or 4 to select number of players:": "Presiona 2, 3 o 4 para definir la cantidad de jugadores:",
        "Enter name for player {num}:": "Ingresa el nombre para el jugador {num}:",
        "Press Enter to confirm, Q to quit": "Presiona Enter para confirmar, Q para salir",
        "The name cannot be empty.": "El nombre no puede estar vacío.",
        "The name has already been used. Choose another.": "El nombre ya fue usado. Elige otro.",
        "Press 4, 5, 6, or 7 to select race length:": "Presiona 4, 5, 6 o 7 para definir el largo de la carrera:",
        "Q: Exit": "Q: Salir",
        "FINISH": "LLEGADA",
        "LLEGADA": "LLEGADA",
        "Current Card:": "Carta actual:",
        "No Card": "Sin carta",
        "Press Q to quit, any other key to continue": "Presiona Q para salir, cualquier otra tecla para continuar",
        "Restart game? (S/N)": "¿Queres reiniciar el juego? S: Si / N: No",
        "Same players and length? (S/N)": "¿Mismos jugadores y largo? S: Si / N: No",
        "Press S for Yes, N for No": "Presiona S para Sí, N para No",
        "Press Y for Yes, N for No": "Presiona S para Sí, N para No",
        "Invalid key. Try again.": "Tecla inválida. Intenta de nuevo.",
        "Error getting game parameters: {error}": "Error al obtener los parámetros del juego: {error}",
        "Knights status:": "Estado de los caballos:",
        "Steps status:": "Estado de los pasos:",
        "Coins": "Oros",
        "Cups": "Copas",
        "Swords": "Espadas",
        "Clubs": "Bastos",
        "coins": "oros",
        "cups": "copas",
        "swords": "espadas",
        "clubs": "bastos",        
        # Interface
        "Game Setup": "Configuración del juego",
        "Players:": "Jugadores:",
        "Player names:": "Nombres de los jugadores:",
        "Race length:": "Largo de la carrera:",
        "Continue": "Continuar",
        "Accept": "Aceptar",
        "Enter player names:": "Ingresa los nombres de los jugadores:",
        "Select number of players:": "Selecciona la cantidad de jugadores:",
        "Select race length:": "Selecciona el largo de la carrera:",
        "Yes": "Sí",
        "No": "No",
        "Restart game": "¿Reiniciar juego?",
        "Same players and length": "¿Mismos jugadores y largo?",
        "Player": "Jugador",
    },
    "en": {
        # General
        "CARRERAS": "RACES",
        "RACES": "RACES",
        "Press Q to quit": "Press Q to quit",
        "Press 2, 3, or 4 to select number of players:": "Press 2, 3, or 4 to select number of players:",
        "Enter name for player {num}:": "Enter name for player {num}:",
        "Press Enter to confirm, Q to quit": "Press Enter to confirm, Q to quit",
        "The name cannot be empty.": "The name cannot be empty.",
        "The name has already been used. Choose another.": "The name has already been used. Choose another.",
        "Press 4, 5, 6, or 7 to select race length:": "Press 4, 5, 6, or 7 to select race length:",
        "Q: Exit": "Q: Exit",
        "FINISH": "FINISH",
        "LLEGADA": "FINISH",
        "Current Card:": "Current Card:",
        "No Card": "No Card",
        "Press Q to quit, any other key to continue": "Press Q to quit, any other key to continue",
        "Restart game? (S/N)": "Restart game? (Y/N)",
        "Same players and length? (S/N)": "Same players and length? (Y/N)",
        "Press S for Yes, N for No": "Press Y for Yes, N for No",
        "Press Y for Yes, N for No": "Press Y for Yes, N for No",
        "Invalid key. Try again.": "Invalid key. Try again.",
        "Error getting game parameters: {error}": "Error getting game parameters: {error}",
        "Knights status:": "Knights status:",
        "Steps status:": "Steps status:",
        "Coins": "Coins",
        "Cups": "Cups",
        "Swords": "Swords",
        "Clubs": "Clubs",
        "coins": "coins",
        "cups": "cups",
        "swords": "swords",
        "clubs": "clubs",        
        # Interface
        "Game Setup": "Game Setup",
        "Players:": "Players:",
        "Player names:": "Player names:",
        "Race length:": "Race length:",
        "Continue": "Continue",
        "Accept": "Accept",
        "Enter player names:": "Enter player names:",
        "Select number of players:": "Select number of players:",
        "Select race length:": "Select race length:",
        "Yes": "Yes",
        "No": "No",
        "Restart game": "Restart game?",
        "Same players and length": "Same players and length?",
        "Player": "Player",
    },
}

def set_language(lang: str):
    """Set the current language for translations."""
    global _LANG
    with _LOCK:
        if lang in TRANSLATIONS:
            _LANG = lang
        else:
            _LANG = "es"  # fallback

def get_language() -> str:
    return _LANG

def tr(msg: str, **kwargs) -> str:
    """Translate a message to the current language."""
    lang = _LANG
    text = TRANSLATIONS.get(lang, {}).get(msg, msg)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
