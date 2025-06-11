"""Races Game Board pygame implementation"""

import pygame
import sys
import os
from typing import Optional, Tuple
from .game import Game
from .card import Card
from .paraminput import ParamInputMixin
from .i18n import tr, get_language


class GraphicBoard(ParamInputMixin):
    """
    Represents the graphical game board using pygame.

    Maintains the same interface as the curses Board class.
    """

    # Constants matching the original Board class
    CARD_WIDTH = 80
    CARD_HEIGHT = 120
    EXIT_KEYS = [pygame.K_q]

    LENGTH_VALUES = {pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7}
    PLAYER_VALUES = {pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}
    # YES/NO keys will be set in __init__ based on language
    YES_NO_VALUES = None

    # Colors for suits (RGB values)
    SUIT_COLORS = {
        "coins": (255, 215, 0),  # Gold
        "cups": (220, 20, 60),  # Crimson
        "swords": (0, 191, 255),  # Deep Sky Blue
        "clubs": (34, 139, 34),  # Forest Green
    }

    SUITS = {
        "coins": {"symbol": "🪙", "color": SUIT_COLORS["coins"]},
        "cups": {"symbol": "🍷", "color": SUIT_COLORS["cups"]},
        "swords": {"symbol": "⚔", "color": SUIT_COLORS["swords"]},
        "clubs": {"symbol": "🌳", "color": SUIT_COLORS["clubs"]},
    }

    FIGURES = {
        Card.JACK: "J",
        Card.KNIGHT: "K",
        Card.KING: "R",
    }

    def __init__(self):
        """Initialize pygame and create the game window."""
        pygame.init()
        pygame.font.init()

        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(tr("CARRERAS - Horse Racing Game"))

        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # Colors
        self.bg_color = (0, 100, 0)  # Dark green
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)

        self.clock = pygame.time.Clock()
        self.running = True

        self.base_img_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "img"
        )

        # Cargar imágenes de cartas y dorso
        self.card_images = self._load_card_images()
        self.back_image = self._load_back_image()

        # Set YES_NO_VALUES based on language
        lang = get_language()
        if lang == "en":
            self.YES_NO_VALUES = {pygame.K_y: 1, pygame.K_n: 0}
        else:
            self.YES_NO_VALUES = {pygame.K_s: 1, pygame.K_n: 0}

    def _load_card_images(self):
        """Carga todas las imágenes de cartas disponibles en un diccionario."""
        card_images = {}
        suits = [
            "coins",
            "cups",
            "swords",
            "clubs",
        ]
        ranks = range(1, 13)
        for suit in suits:
            for rank in ranks:
                path = os.path.join(self.base_img_path, suit, f"{rank}.jpg")
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(
                        image, (self.CARD_WIDTH, self.CARD_HEIGHT)
                    )
                    card_images[(suit, rank)] = image
                except Exception:
                    pass  # Si no existe la imagen, se maneja en _draw_card
        return card_images

    def _load_back_image(self):
        """Carga la imagen de dorso de carta (back.jpg)."""
        try:
            path = os.path.join(self.base_img_path, "back.jpg")
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (self.CARD_WIDTH, self.CARD_HEIGHT))
            return image
        except Exception:
            return None

    def ask_game_params_screen(self) -> tuple[int, int, list[str]]:
        """Pantalla única para seleccionar cantidad de jugadores, nombres y largo de carrera con radio buttons."""
        player_options = [2, 3, 4]
        length_options = [4, 5, 6, 7]
        selected_players = 2
        selected_length = 4
        names = ["" for _ in range(selected_players)]
        active_name_idx = 0
        error_msg = ""
        running = True
        while running:
            self.screen.fill(self.bg_color)
            # Título
            self._draw_text(tr("Game Setup"), self.font_large, self.white, 50, 30)
            # Selección de cantidad de jugadores (radio buttons)
            self._draw_text(tr("Players:"), self.font_medium, self.white, 50, 100)
            for idx, val in enumerate(player_options):
                cx = 180 + idx * 90
                cy = 115
                # Dibuja círculo (radio button)
                pygame.draw.circle(self.screen, self.black, (cx, cy), 15, 2)
                if val == selected_players:
                    pygame.draw.circle(self.screen, (50, 200, 50), (cx, cy), 10)
                text = self.font_medium.render(str(val), True, self.black)
                text_rect = text.get_rect(midleft=(cx + 22, cy))
                self.screen.blit(text, text_rect)
            # Campos de nombres dinámicos
            self._draw_text(tr("Player names:"), self.font_medium, self.white, 50, 160)
            if len(names) < selected_players:
                names += ["" for _ in range(selected_players - len(names))]
            elif len(names) > selected_players:
                names = names[:selected_players]
            for idx in range(selected_players):
                y = 200 + idx * 55
                rect = pygame.Rect(50, y, 320, 40)
                color = (200, 255, 200) if idx == active_name_idx else self.white
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.black, rect, 2)
                name = names[idx] if idx < len(names) else ""
                text = self.font_medium.render(name, True, self.black)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
                label = self.font_small.render(f"{tr('Player')} {idx+1}", True, self.gray)
                self.screen.blit(label, (rect.x, rect.y - 18))
            # Selección de largo de carrera (radio buttons)
            y_radio = 200 + selected_players * 55 + 35
            self._draw_text(tr("Race length:"), self.font_medium, self.white, 50, y_radio)
            for idx, val in enumerate(length_options):
                cx = 210 + idx * 90
                cy = y_radio + 20
                pygame.draw.circle(self.screen, self.black, (cx, cy), 15, 2)
                if val == selected_length:
                    pygame.draw.circle(self.screen, (50, 200, 50), (cx, cy), 10)
                text = self.font_medium.render(str(val), True, self.black)
                text_rect = text.get_rect(midleft=(cx + 22, cy))
                self.screen.blit(text, text_rect)
            # Mensaje de error
            if error_msg:
                err = self.font_small.render(error_msg, True, (255, 0, 0))
                self.screen.blit(err, (50, y_radio + 70))
            # Botón continuar
            cont_rect = pygame.Rect(400, y_radio + 50, 160, 40)
            pygame.draw.rect(self.screen, (100, 200, 100), cont_rect)
            pygame.draw.rect(self.screen, self.black, cont_rect, 2)
            cont_text = self.font_medium.render(tr("Continue"), True, self.white)
            cont_text_rect = cont_text.get_rect(center=cont_rect.center)
            self.screen.blit(cont_text, cont_text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.destroy()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Selección de cantidad de jugadores (radio buttons)
                    for idx, val in enumerate(player_options):
                        cx = 180 + idx * 90
                        cy = 115
                        if (pos[0] - cx) ** 2 + (pos[1] - cy) ** 2 <= 15 ** 2:
                            selected_players = val
                            if len(names) < val:
                                names += ["" for _ in range(val - len(names))]
                            elif len(names) > val:
                                names = names[:val]
                            if active_name_idx >= val:
                                active_name_idx = val - 1
                    # Selección de largo de carrera (radio buttons)
                    for idx, val in enumerate(length_options):
                        cx = 210 + idx * 90
                        cy = y_radio + 20
                        if (pos[0] - cx) ** 2 + (pos[1] - cy) ** 2 <= 15 ** 2:
                            selected_length = val
                    # Selección de campo de nombre
                    for idx in range(selected_players):
                        rect = pygame.Rect(50, 200 + idx * 55, 320, 40)
                        if rect.collidepoint(pos):
                            active_name_idx = idx
                    # Botón continuar
                    if cont_rect.collidepoint(pos):
                        if any(not n.strip() for n in names[:selected_players]):
                            error_msg = tr("The name cannot be empty.")
                        elif len(set(n.strip() for n in names[:selected_players])) < selected_players:
                            error_msg = tr("The name has already been used. Choose another.")
                        else:
                            return selected_players, selected_length, [n.strip() for n in names[:selected_players]]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        active_name_idx = (active_name_idx + 1) % selected_players
                    elif event.key == pygame.K_BACKSPACE:
                        names[active_name_idx] = names[active_name_idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif event.unicode and len(names[active_name_idx]) < 20:
                        names[active_name_idx] += event.unicode
            self.clock.tick(60)
        return selected_players, selected_length, [n.strip() for n in names[:selected_players]]

    def ask_player_count(self) -> int:
        players, _, _ = self.ask_game_params_screen()
        return players

    def ask_race_length(self) -> int:
        _, length, _ = self.ask_game_params_screen()
        return length

    def ask_player_names(self, count: int) -> list[str]:
        _, _, names = self.ask_game_params_screen()
        return names

    def __init__(self):
        """Initialize pygame and create the game window."""
        pygame.init()
        pygame.font.init()

        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(tr("CARRERAS - Horse Racing Game"))

        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # Colors
        self.bg_color = (0, 100, 0)  # Dark green
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)

        self.clock = pygame.time.Clock()
        self.running = True

        self.base_img_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "img"
        )

        # Cargar imágenes de cartas y dorso
        self.card_images = self._load_card_images()
        self.back_image = self._load_back_image()

        # Set YES_NO_VALUES based on language
        lang = get_language()
        if lang == "en":
            self.YES_NO_VALUES = {pygame.K_y: 1, pygame.K_n: 0}
        else:
            self.YES_NO_VALUES = {pygame.K_s: 1, pygame.K_n: 0}

    def _load_card_images(self):
        """Carga todas las imágenes de cartas disponibles en un diccionario."""
        card_images = {}
        suits = [
            "coins",
            "cups",
            "swords",
            "clubs",
        ]
        ranks = range(1, 13)
        for suit in suits:
            for rank in ranks:
                path = os.path.join(self.base_img_path, suit, f"{rank}.jpg")
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(
                        image, (self.CARD_WIDTH, self.CARD_HEIGHT)
                    )
                    card_images[(suit, rank)] = image
                except Exception:
                    pass  # Si no existe la imagen, se maneja en _draw_card
        return card_images

    def _load_back_image(self):
        """Carga la imagen de dorso de carta (back.jpg)."""
        try:
            path = os.path.join(self.base_img_path, "back.jpg")
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (self.CARD_WIDTH, self.CARD_HEIGHT))
            return image
        except Exception:
            return None

    def ask_player_count(self) -> int:
        """Show buttons for player count selection (2, 3, 4)."""
        options = [2, 3, 4]
        button_rects = []
        while self.running:
            self.screen.fill(self.bg_color)
            self._draw_text(tr("Select number of players:"), self.font_large, self.white, 50, 100)
            for idx, val in enumerate(options):
                rect = pygame.Rect(50 + idx * 200, 200, 180, 80)
                pygame.draw.rect(self.screen, self.white, rect)
                pygame.draw.rect(self.screen, self.black, rect, 3)
                text = self.font_large.render(str(val), True, self.black)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
                button_rects.append((rect, val))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.destroy()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for rect, val in button_rects:
                        if rect.collidepoint(pos):
                            return val
            self.clock.tick(60)
        return 2

    def ask_player_names(self, count: int) -> list[str]:
        """Show a form with one input box per player for names."""
        names = ["" for _ in range(count)]
        active_idx = 0
        error_msg = ""
        while self.running:
            self.screen.fill(self.bg_color)
            self._draw_text(tr("Enter player names:"), self.font_large, self.white, 50, 50)
            for idx in range(count):
                y = 150 + idx * 70
                rect = pygame.Rect(50, y, 400, 50)
                color = (200, 255, 200) if idx == active_idx else self.white
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.black, rect, 2)
                name = names[idx]
                text = self.font_medium.render(name, True, self.black)
                self.screen.blit(text, (rect.x + 10, rect.y + 10))
                label = self.font_small.render(f"{tr('Player')} {idx+1}", True, self.gray)
                self.screen.blit(label, (rect.x, rect.y - 20))
            # Draw Accept button
            accept_rect = pygame.Rect(500, 150, 200, 60)
            pygame.draw.rect(self.screen, (100, 200, 100), accept_rect)
            pygame.draw.rect(self.screen, self.black, accept_rect, 2)
            accept_text = self.font_large.render(tr("Accept"), True, self.white)
            self.screen.blit(accept_text, (accept_rect.x + 30, accept_rect.y + 10))
            # Draw error message if any
            if error_msg:
                err = self.font_small.render(error_msg, True, (255, 0, 0))
                self.screen.blit(err, (50, 150 + count * 70))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.destroy()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx in range(count):
                        rect = pygame.Rect(50, 150 + idx * 70, 400, 50)
                        if rect.collidepoint(pos):
                            active_idx = idx
                    if accept_rect.collidepoint(pos):
                        # Validate
                        if any(not n.strip() for n in names):
                            error_msg = tr("The name cannot be empty.")
                        elif len(set(n.strip() for n in names)) < count:
                            error_msg = tr("The name has already been used. Choose another.")
                        else:
                            return [n.strip() for n in names]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        active_idx = (active_idx + 1) % count
                    elif event.key == pygame.K_BACKSPACE:
                        names[active_idx] = names[active_idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        pass  # Ignore enter in text fields
                    elif event.unicode and len(names[active_idx]) < 20:
                        names[active_idx] += event.unicode
            self.clock.tick(60)
        return names

    def ask_race_length(self) -> int:
        """Show buttons for race length selection (4, 5, 6, 7)."""
        options = [4, 5, 6, 7]
        button_rects = []
        while self.running:
            self.screen.fill(self.bg_color)
            self._draw_text(tr("Select race length:"), self.font_large, self.white, 50, 100)
            for idx, val in enumerate(options):
                rect = pygame.Rect(50 + idx * 150, 200, 120, 80)
                pygame.draw.rect(self.screen, self.white, rect)
                pygame.draw.rect(self.screen, self.black, rect, 3)
                text = self.font_large.render(str(val), True, self.black)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
                button_rects.append((rect, val))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.destroy()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for rect, val in button_rects:
                        if rect.collidepoint(pos):
                            return val
            self.clock.tick(60)
        return 4

    def draw_game(self, game: Game):
        """Draw the complete game state."""
        self.screen.fill(self.bg_color)

        # Draw title
        self._draw_text(tr("CARRERAS"), self.font_large, self.white, 50, 20)

        # Draw player status
        self._draw_player_status(game)

        # Draw race track
        self._draw_race_track(game)

        # Draw current card
        self._draw_current_card(game)

        # Draw instructions
        self._draw_text(
            tr("Press Q to quit, any other key to continue"),
            self.font_small,
            self.gray,
            50,
            self.height - 30,
        )

        pygame.display.flip()
        self._wait_for_key()

    def _draw_player_status(self, game: Game):
        """Draw player rankings and status."""
        y_start = 70

        # Calculate rankings
        rank = {
            row: i + 1
            for i, row in enumerate(
                sorted(set(k["row"] for k in game.knights.values()), reverse=True)
            )
        }

        status = sorted(
            (
                rank[k["row"]],
                k["player"],
                k["card"].suit,
            )
            for k in game.knights.values()
        )

        for i, (ranking, player, suit) in enumerate(status):
            color = self.SUIT_COLORS[suit]
            # Mostrar el nombre traducido del palo junto al jugador
            suit_name = tr(suit)
            text = f"{ranking}: {player} ({suit_name})"
            self._draw_text(text, self.font_medium, color, 50, y_start + i * 30)

    def _draw_race_track(self, game: Game):
        """Draw the race track with knights and steps."""
        # Reducir el espacio vertical entre cartas de paso y filas de jugadores
        track_start_x = 300
        track_start_y = 100 + self.CARD_HEIGHT // 2  # Menos espacio arriba

        # Encabezado: nombre de cada jugador sobre su fila
        for knight_num, knight in game.knights.items():
            y = track_start_y + knight_num * self.CARD_HEIGHT
            player_name = knight["player"]
            self._draw_text(
                player_name,
                self.font_small,
                self.white,
                track_start_x - 90,
                y + self.CARD_HEIGHT // 2 - 10,
            )

        # Draw finish line
        finish_x = track_start_x + (game.length + 1) * self.CARD_WIDTH
        pygame.draw.line(
            self.screen,
            self.white,
            (finish_x, track_start_y),
            (finish_x, track_start_y + game.players * self.CARD_HEIGHT),
            3,
        )
        self._draw_text(
            tr("FINISH"), self.font_medium, self.white, finish_x + 10, track_start_y
        )

        # Draw step cards (ahora más cerca de la pista)
        for step_num, step in game.steps.items():
            x = track_start_x + step_num * self.CARD_WIDTH
            y = track_start_y - self.CARD_HEIGHT + 10  # Menos separación
            self._draw_card(
                x,
                y,
                "?" if step["hidden"] else step["card"].value,
                None if step["hidden"] else step["card"].suit,
            )

        # Draw knights
        for knight_num, knight in game.knights.items():
            x = track_start_x + knight["row"] * self.CARD_WIDTH
            y = track_start_y + knight_num * self.CARD_HEIGHT
            self._draw_card(x, y, knight["card"].value, knight["card"].suit)

    def _draw_current_card(self, game: Game):
        """Draw the current top card."""
        if game.top_card:
            self._draw_card(50, 300, game.top_card.value, game.top_card.suit)
            self._draw_text(tr("Current Card:"), self.font_medium, self.white, 50, 270)
        else:
            self._draw_card(50, 300, "?", None)
            self._draw_text(tr("No Card"), self.font_medium, self.white, 50, 270)

    def _draw_card(self, x: int, y: int, value, suit: Optional[str]):
        """Dibuja una carta: imagen, dorso o cuadro blanco si no existe."""
        rect = pygame.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        if suit is None or value == "?":
            # Carta oculta: mostrar dorso si existe, si no, cuadro blanco
            if self.back_image:
                self.screen.blit(self.back_image, (x, y))
            else:
                pygame.draw.rect(self.screen, self.white, rect)
                pygame.draw.rect(self.screen, self.black, rect, 2)
        else:
            img = self.card_images.get((suit, value))
            if img:
                self.screen.blit(img, (x, y))
            else:
                # Si no hay imagen, cuadro blanco con borde
                pygame.draw.rect(self.screen, self.white, rect)
                pygame.draw.rect(self.screen, self.black, rect, 2)
                # Además, mostrar valor y símbolo
                color = self.SUIT_COLORS[suit]
                display_value = self.FIGURES.get(value, str(value))
                text_surface = self.font_medium.render(str(display_value), True, color)
                text_rect = text_surface.get_rect(
                    center=(x + self.CARD_WIDTH // 2, y + self.CARD_HEIGHT // 2 - 10)
                )
                self.screen.blit(text_surface, text_rect)
                suit_text = self.SUITS[suit]["symbol"]
                suit_surface = self.font_small.render(suit_text, True, color)
                suit_rect = suit_surface.get_rect(
                    center=(x + self.CARD_WIDTH // 2, y + self.CARD_HEIGHT // 2 + 15)
                )
                self.screen.blit(suit_surface, suit_rect)

    def _draw_text(
        self, text: str, font: pygame.font.Font, color: tuple, x: int, y: int
    ):
        """Draw text at specified position."""
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def _wait_for_key(self):
        """Wait for user input: key or mouse click."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    self.destroy()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            self.clock.tick(60)

    def ask_restart(self) -> Tuple[bool, bool]:
        """Ask if user wants to restart the game."""
        restart = self._ask_yes_no(tr("Restart game"))
        if not restart:
            return False, False

        same_params = self._ask_yes_no(tr("Same players and length"))
        return True, same_params

    def _ask_yes_no(self, question: str) -> bool:
        """Show Yes/No buttons for confirmation."""
        while self.running:
            self.screen.fill(self.bg_color)
            self._draw_text(question, self.font_large, self.white, 50, 200)
            yes_rect = pygame.Rect(50, 300, 150, 70)
            no_rect = pygame.Rect(250, 300, 150, 70)
            pygame.draw.rect(self.screen, (100, 200, 100), yes_rect)
            pygame.draw.rect(self.screen, (200, 100, 100), no_rect)
            pygame.draw.rect(self.screen, self.black, yes_rect, 2)
            pygame.draw.rect(self.screen, self.black, no_rect, 2)
            yes_text = self.font_large.render(tr("Yes"), True, self.white)
            no_text = self.font_large.render(tr("No"), True, self.white)
            self.screen.blit(yes_text, (yes_rect.x + 40, yes_rect.y + 15))
            self.screen.blit(no_text, (no_rect.x + 40, no_rect.y + 15))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.destroy()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if yes_rect.collidepoint(pos):
                        return True
                    if no_rect.collidepoint(pos):
                        return False
            self.clock.tick(60)
        return False

    def destroy(self):
        """Clean up pygame resources."""
        pygame.quit()

    def get_game_params(self) -> tuple[int, int, list[str]]:
        """Obtiene todos los parámetros del juego: jugadores, nombres y largo."""
        return self.ask_game_params_screen()
