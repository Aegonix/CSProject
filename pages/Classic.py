from widgets import *
from colors import *
import pygame
pygame.font.init()

class Classic:
    def __init__(self, change_page, win):
        self.change_page = change_page
        self.win = win
        self.bg = BG_COLOR
        self.score_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 50)
        self.reset_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 40)
        self.game_over_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 100)
        self.board = Board((345, 100), 510)

        # Resets the board when clicked
        self.reset_button = Button(
            x=1050,
            y=300,
            x_scale=1.5,
            y_scale=1.05,
            text="Reset",
            font=self.reset_text,
            color=(240, 225, 24),
            text_color=BLACK,
            action=self.board.reset,
            border_radius=5
        )

    def draw(self):
        """Draw the elements of the classic game page to the screen."""

        self.win.fill(self.bg)
        self.board.draw(self.win)
        self.score_surface = self.score_text.render(f"SCORE:", True, BLACK)
        self.score_number = self.score_text.render(str(self.board.score), True, BLACK)
        self.score_rect = self.score_surface.get_rect(topleft=(75, 250))
        self.score_number_rect = self.score_number.get_rect(center=(self.score_rect.centerx, 340))
        self.win.blit(self.score_surface, self.score_rect)
        self.win.blit(self.score_number, self.score_number_rect)
        self.reset_button.draw(self.win)
        if self.board.game_over():
            self.game_over_surface = self.game_over_text.render("GAME OVER", True, BLACK)
            self.game_over_rect = self.game_over_surface.get_rect(center=(600, 300))
            self.win.blit(self.game_over_surface, self.game_over_rect)

    def update(self, event):
        """Update the classic game page based on user input."""

        self.board.update(event)
        self.reset_button.update(event)

    def clean(self):
        pass