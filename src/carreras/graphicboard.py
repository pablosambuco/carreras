"""Races Game Board pygame implementation"""

import pygame
import sys
import os
from typing import Optional, Tuple
from .game import Game
from .card import Card
from .paraminput import ParamInputMixin


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
    YES_NO_VALUES = {pygame.K_s: 1, pygame.K_n: 0}

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
        pygame.display.set_caption("CARRERAS - Horse Racing Game")

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

        self.base_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

        # Cargar imágenes de cartas y dorso
        self.card_images = self._load_card_images()
        self.back_image = self._load_back_image()

    def _load_card_images(self):
        """Carga todas las imágenes de cartas disponibles en un diccionario."""
        card_images = {}
        suits = ["coins", "cups", "swords", "clubs"]
        ranks = range(1, 13)
        for suit in suits:
            for rank in ranks:
                path = os.path.join(self.base_img_path, suit, f"{rank}.jpg")
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (self.CARD_WIDTH, self.CARD_HEIGHT))
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
        """Ask for the number of players (2-4)."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    self.destroy()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in self.PLAYER_VALUES:
                    return self.PLAYER_VALUES[event.key]
            self.screen.fill(self.bg_color)
            self._draw_text("Press Q to quit", self.font_medium, self.white, 50, 50)
            self._draw_text(
                "Press 2, 3, or 4 to select number of players:",
                self.font_large,
                self.white,
                50,
                200,
            )
            pygame.display.flip()
            self.clock.tick(60)

        return 2  # fallback

    def ask_player_names(self, count: int) -> list[str]:
        """Ask for player names."""
        names = []
        current_name = ""

        for i in range(count):
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_q
                    ):
                        self.destroy()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if current_name.strip():
                                names.append(current_name.strip())
                                current_name = ""
                                break
                        elif event.key == pygame.K_BACKSPACE:
                            current_name = current_name[:-1]
                        else:
                            current_name += event.unicode

                self.screen.fill(self.bg_color)
                self._draw_text(
                    f"Enter name for player {i+1}:",
                    self.font_large,
                    self.white,
                    50,
                    200,
                )
                self._draw_text(current_name, self.font_medium, self.white, 50, 250)
                self._draw_text(
                    "Press Enter to confirm, Q to quit",
                    self.font_small,
                    self.gray,
                    50,
                    300,
                )
                pygame.display.flip()
                self.clock.tick(60)

                if len(names) > i:
                    break

        return names

    def ask_race_length(self) -> int:
        """Ask for the race length (4-7)."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    self.destroy()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in self.LENGTH_VALUES:
                    return self.LENGTH_VALUES[event.key]

            self.screen.fill(self.bg_color)
            self._draw_text(
                "Press 4, 5, 6, or 7 to select race length:",
                self.font_large,
                self.white,
                50,
                200,
            )
            pygame.display.flip()
            self.clock.tick(60)

        return 4  # fallback

    def draw_game(self, game: Game):
        """Draw the complete game state."""
        self.screen.fill(self.bg_color)

        # Draw title
        self._draw_text("CARRERAS", self.font_large, self.white, 50, 20)

        # Draw player status
        self._draw_player_status(game)

        # Draw race track
        self._draw_race_track(game)

        # Draw current card
        self._draw_current_card(game)

        # Draw instructions
        self._draw_text(
            "Press Q to quit, any other key to continue",
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
            text = f"{ranking}: {player} ({suit})"
            self._draw_text(text, self.font_medium, color, 50, y_start + i * 30)

    def _draw_race_track(self, game: Game):
        """Draw the race track with knights and steps."""
        track_start_x = 300
        track_start_y = 100

        # Encabezado: nombre de cada jugador sobre su fila
        for knight_num, knight in game.knights.items():
            y = track_start_y + knight_num * self.CARD_HEIGHT
            player_name = knight["player"]
            self._draw_text(
                player_name,
                self.font_small,
                self.white,
                track_start_x - 90,  # a la izquierda de la pista
                y + self.CARD_HEIGHT // 2 - 10
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
            "FINISH", self.font_medium, self.white, finish_x + 10, track_start_y
        )

        # Draw step cards
        for step_num, step in game.steps.items():
            x = track_start_x + step_num * self.CARD_WIDTH
            y = track_start_y - self.CARD_HEIGHT - 10

            if step["hidden"]:
                self._draw_card(x, y, "?", None)
            else:
                self._draw_card(x, y, step["card"].value, step["card"].suit)

        # Draw knights
        for knight_num, knight in game.knights.items():
            x = track_start_x + knight["row"] * self.CARD_WIDTH
            y = track_start_y + knight_num * self.CARD_HEIGHT
            self._draw_card(x, y, knight["card"].value, knight["card"].suit)

    def _draw_current_card(self, game: Game):
        """Draw the current top card."""
        if game.top_card:
            self._draw_card(50, 300, game.top_card.value, game.top_card.suit)
            self._draw_text("Current Card:", self.font_medium, self.white, 50, 270)
        else:
            self._draw_card(50, 300, "?", None)
            self._draw_text("No Card", self.font_medium, self.white, 50, 270)

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
        """Wait for user input."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    self.destroy()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return
            self.clock.tick(60)

    def ask_restart(self) -> Tuple[bool, bool]:
        """Ask if user wants to restart the game."""
        restart = self._ask_yes_no("Restart game? (S/N)")
        if not restart:
            return False, False

        same_params = self._ask_yes_no("Same players and length? (S/N)")
        return True, same_params

    def _ask_yes_no(self, question: str) -> bool:
        """Ask a yes/no question."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    self.destroy()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in self.YES_NO_VALUES:
                    return bool(self.YES_NO_VALUES[event.key])

            self.screen.fill(self.bg_color)
            self._draw_text(question, self.font_large, self.white, 50, 200)
            self._draw_text(
                "Press S for Yes, N for No", self.font_medium, self.gray, 50, 250
            )
            pygame.display.flip()
            self.clock.tick(60)

        return False

    def destroy(self):
        """Clean up pygame resources."""
        pygame.quit()
