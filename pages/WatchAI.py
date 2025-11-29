from widgets import *
from colors import *
from AI import AI
import time
import threading
import pygame
pygame.font.init()

class WatchAI:
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
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=self.board.reset,
            border_radius=5
        )

        # Removes the delay between AI moves when clicked
        self.max_speed_button = Button(
            x=1050,
            y=375,
            x_scale=1.2,
            y_scale=1.05,
            text="Max Speed",
            font=self.reset_text,
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=self.change_speed,
            border_radius=5
        )

        # Adds the delay between AI moves when clicked
        self.normal_speed_button = Button(
            x=1050,
            y=375,
            x_scale=1.2,
            y_scale=1.05,
            text="Normal Speed",
            font=self.reset_text,
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=self.change_speed,
            border_radius=5
        )

        self.ai = AI(5)
        self.ai.update_board(self.board.board)
        self.done = False
        self.max_speed = False

        # Start a separate thread for the AI to run on
        self.ai_thread = threading.Thread(target=self.handle_ai)
        self.ai_thread.daemon = True
        self.ai_thread.start()

    def draw(self):
        """Draw the elements of the Watch AI page to the screen."""

        self.win.fill(self.bg)
        self.board.draw(self.win)
        self.score_surface = self.score_text.render(f"SCORE:", True, BLACK)
        self.score_number = self.score_text.render(str(self.board.score), True, BLACK)
        self.score_rect = self.score_surface.get_rect(topleft=(75, 250))
        self.score_number_rect = self.score_number.get_rect(center=(self.score_rect.centerx, 340))
        self.win.blit(self.score_surface, self.score_rect)
        self.win.blit(self.score_number, self.score_number_rect)
        self.reset_button.draw(self.win)

        if self.max_speed:
            self.normal_speed_button.draw(self.win)
        else:
            self.max_speed_button.draw(self.win)
        
        if self.board.game_over():
            self.game_over_surface = self.game_over_text.render("GAME OVER", True, BLACK)
            self.game_over_rect = self.game_over_surface.get_rect(center=(600, 300))
            self.win.blit(self.game_over_surface, self.game_over_rect)

    def update(self, event):
        """Update the elements of the Watch AI page based on user input."""

        self.reset_button.update(event)
        if self.max_speed:
            self.max_speed_button.update(event)
        else:
            self.normal_speed_button.update(event)

    def handle_ai(self):
        """Handle the AI moves in a separate thread until game over or page changed."""

        while not self.board.game_over() and not self.done:
            if not self.max_speed:
                time.sleep(0.3)
            move = self.ai.move()
            if self.board.move(move, []):
                self.board.random_tile()
            self.ai.update_board(self.board.board)

    def reset(self):
        """Reset the game board and restart the AI thread."""

        self.board.reset()

        if not self.ai_thread.is_alive():
            self.ai.update_board(self.board.board)
            self.ai_thread = threading.Thread(target=self.handle_ai)
            self.ai_thread.daemon = True
            self.ai_thread.start()

    def change_speed(self):
        """Toggle the speed of the AI moves."""

        self.max_speed = not self.max_speed

    def clean(self):
        """Stop the AI thread when changing pages."""

        self.done = True