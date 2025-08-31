from widgets import *
from colors import *
import pygame
pygame.font.init()

class VsFriend:
    def __init__(self, change_page, win):
        self.change_page = change_page
        self.win = win
        self.bg = BG_COLOR
        self.score_text = pygame.font.SysFont("JetBrains Mono", 50)
        self.reset_text = pygame.font.SysFont("JetBrains Mono", 40)
        self.player_text = pygame.font.SysFont("JetBrains Mono", 60)
        self.game_over_text = pygame.font.SysFont("JetBrains Mono", 120)

        # Reset the board when clicked
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

        self.player1_board = Board((25, 100), 510)
        self.player2_board = Board((665, 100), 510)


    def draw(self):
        """Draw the elements of the Vs Friend page to the screen."""

        self.win.fill(self.bg)
        
        self.player1_board.draw(self.win)
        self.player2_board.draw(self.win)

        self.player_surface = self.player_text.render("PLAYER 1", True, BLACK)
        self.player_rect = self.player_surface.get_rect(center=(280, 50))
        self.win.blit(self.player_surface, self.player_rect)

        self.AI_surface = self.player_text.render("PLAYER 2", True, BLACK)
        self.AI_rect = self.AI_surface.get_rect(center=(920, 50))
        self.win.blit(self.AI_surface, self.AI_rect)

        self.score_surface = self.score_text.render("SCORE:", True, BLACK)

        self.player1_score_number = self.score_text.render(str(self.player1_board.score), True, BLACK)
        self.player1_score_rect = self.score_surface.get_rect(topleft=(25, 610))
        self.player1_score_number_rect = self.player1_score_number.get_rect(topleft=(self.player1_score_rect.right + 10, 610))
        self.win.blit(self.score_surface, self.player1_score_rect)
        self.win.blit(self.player1_score_number, self.player1_score_number_rect)

        self.player2_score_number = self.score_text.render(str(self.player2_board.score), True, BLACK)
        self.player2_score_number_rect = self.player2_score_number.get_rect(topright=(1175, 610))
        self.player2_score_rect = self.score_surface.get_rect(topright=(self.player2_score_number_rect.left - 10, 610))
        self.win.blit(self.score_surface, self.player2_score_rect)
        self.win.blit(self.player2_score_number, self.player2_score_number_rect)

        if self.player1_board.game_over() and self.player2_board.game_over():
            self.game_over_surface = self.game_over_text.render("GAME OVER", True, BLACK)
            self.game_over_rect = self.game_over_surface.get_rect(center=(600, 280))
            pygame.draw.rect(self.win, LIGHT_GREY, self.game_over_rect.scale_by(1.2, 1.05), border_radius=10)
            self.win.blit(self.game_over_surface, self.game_over_rect)

            if self.player1_board.score > self.player2_board.score:
                winner_text = "PLAYER 1 WINS!"
            elif self.player2_board.score > self.player1_board.score:
                winner_text = "PLAYER 2 WINS!"
            else:
                winner_text = "IT'S A TIE!"
            
            self.winner_surface = self.game_over_text.render(winner_text, True, BLACK)
            self.winner_rect = self.winner_surface.get_rect(center=(600, 420))
            pygame.draw.rect(self.win, LIGHT_GREY, self.winner_rect.scale_by(1.1, 1.05), border_radius=10)
            self.win.blit(self.winner_surface, self.winner_rect)


        self.reset_button.draw(self.win)

    def update(self, event):
        """Update the Vs Friend page based on user input."""

        self.player1_board.update(event)
        self.reset_button.update(event)

        keymap = {pygame.K_w: pygame.K_UP,
                  pygame.K_s: pygame.K_DOWN,
                  pygame.K_a: pygame.K_LEFT,
                  pygame.K_d: pygame.K_RIGHT}
        
        if event.type == pygame.KEYDOWN:
            if self.player2_board.move(keymap.get(event.key), []):
                self.player2_board.random_tile()

    def reset(self):
        """Reset the game boards."""

        self.player1_board.reset()
        self.player2_board.reset()
    
    def clean(self):
        pass