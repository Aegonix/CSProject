import time
from widgets import *
from colors import *
from AI import AI
import threading
import pygame
pygame.font.init()

class VsAI:
    def __init__(self, change_page, win):
        self.change_page = change_page
        self.win = win
        self.bg = BG_COLOR
        self.score_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 50)
        self.reset_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 40)
        self.player_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 60)
        self.game_over_text = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 120)

        self.reset_button = Button(
            x=600,
            y=640,
            x_scale=1.5,
            y_scale=1.05,
            text="Reset",
            font=self.reset_text,
            color=(240, 225, 24),
            text_color=BLACK,
            action=self.reset,
            border_radius=5
        )

        self.player_board = Board((25, 100), 510)
        self.ai_board = Board((665, 100), 510)

        self.ai = AI(5)
        self.ai.update_board(self.ai_board.board)
        self.done = False
        self.ai_thread = threading.Thread(target=self.handle_ai)
        self.ai_thread.daemon = True
        self.ai_thread.start()


    def draw(self):
        """Draw the elements of the Vs AI page to the screen."""

        self.win.fill(self.bg)
        
        self.player_board.draw(self.win)
        self.ai_board.draw(self.win)

        self.player_surface = self.player_text.render("PLAYER", True, BLACK)
        self.player_rect = self.player_surface.get_rect(center=(280, 50))
        self.win.blit(self.player_surface, self.player_rect)

        self.AI_surface = self.player_text.render("AI", True, BLACK)
        self.AI_rect = self.AI_surface.get_rect(center=(920, 50))
        self.win.blit(self.AI_surface, self.AI_rect)

        self.score_surface = self.score_text.render("SCORE:", True, BLACK)
        self.score_number = self.score_text.render(str(self.player_board.score), True, BLACK)
        self.score_rect = self.score_surface.get_rect(topleft=(25, 610))
        self.score_number_rect = self.score_number.get_rect(topleft=(self.score_rect.right + 10, 610))
        self.win.blit(self.score_surface, self.score_rect)
        self.win.blit(self.score_number, self.score_number_rect)

        self.ai_score_surface = self.score_text.render("SCORE:", True, BLACK)
        self.ai_score_number = self.score_text.render(str(self.ai_board.score), True, BLACK)
        self.ai_score_number_rect = self.ai_score_number.get_rect(topright=(1175, 610))
        self.ai_score_rect = self.ai_score_surface.get_rect(topright=(self.ai_score_number_rect.left - 10, 610))
        self.win.blit(self.ai_score_surface, self.ai_score_rect)
        self.win.blit(self.ai_score_number, self.ai_score_number_rect)

        if self.player_board.game_over():
            self.game_over_surface = self.game_over_text.render("GAME OVER", True, BLACK)
            self.game_over_rect = self.game_over_surface.get_rect(center=(600, 280))
            pygame.draw.rect(self.win, LIGHT_GREY, self.game_over_rect.scale_by(1.2, 1.05), border_radius=10)
            self.win.blit(self.game_over_surface, self.game_over_rect)


            if self.ai_board.game_over():
                if self.player_board.score > self.ai_board.score:
                    result = "YOU WIN!"
                elif self.player_board.score < self.ai_board.score:
                    result = "AI WINS!"
                else:
                    result = "IT'S A TIE!"
            else:
                result = "AI WINS!"
            
            self.result_surface = self.game_over_text.render(result, True, BLACK)
            self.result_rect = self.result_surface.get_rect(center=(600, 420))
            pygame.draw.rect(self.win, LIGHT_GREY, self.result_rect.scale_by(1.2, 1.01), border_radius=10)
            self.win.blit(self.result_surface, self.result_rect)

        self.reset_button.draw(self.win)

    def update(self, event):
        """Update the Vs AI page based on user input."""

        self.player_board.update(event)
        self.reset_button.update(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.ai_board.board = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]

    def reset(self):
        """Reset the game boards and restart the AI thread."""

        self.player_board.reset()
        self.ai_board.reset()

        if not self.ai_thread.is_alive():
            self.ai.update_board(self.ai_board.board)
            self.ai_thread = threading.Thread(target=self.handle_ai)
            self.ai_thread.daemon = True
            self.ai_thread.start()

    def handle_ai(self):
        """Handle the AI moves in a separate thread until game over or page changed."""

        while not self.ai_board.game_over() and not self.done:
            time.sleep(0.2)
            move = self.ai.move()
            if self.ai_board.move(move, []):
                self.ai_board.random_tile()
            self.ai.update_board(self.ai_board.board)

    def clean(self):
        """Stop the AI thread when changing pages."""

        self.done = True
