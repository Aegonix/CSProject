import pygame
from colors import *
from random import choice, randint
from copy import deepcopy

pygame.font.init()


class Button:
    def __init__(
        self,
        x,
        y,
        x_scale,
        y_scale,
        text,
        font,
        color,
        text_color,
        action,
        border_radius=0,
    ):
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.border_radius = border_radius
        self.action = action
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.text_surface.get_rect().scale_by(x=x_scale, y=y_scale)
        self.rect.center = (x, y)

    def draw(self, win):
        """Draw the button to the screen."""
        
        pygame.draw.rect(
            win, self.color, self.rect, border_radius=self.border_radius
        )
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        win.blit(self.text_surface, text_rect)

    def update(self, event):
        """Check if the button is clicked and perform the action."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.action()


class Board:
    def __init__(self, topleft, size):
        self.board = [[0, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.topleft = topleft
        self.score = 0
        self.size = size
        self.tile_gap = 10
        self.grid_rect = pygame.Rect(topleft, (self.size, self.size))

        self.images = {
            2: pygame.transform.smoothscale(
                pygame.image.load("assets/2.svg"), (115, 115)
            ),
            4: pygame.transform.smoothscale(
                pygame.image.load("assets/4.svg"), (115, 115)
            ),
            8: pygame.transform.smoothscale(
                pygame.image.load("assets/8.svg"), (115, 115)
            ),
            16: pygame.transform.smoothscale(
                pygame.image.load("assets/16.svg"), (115, 115)
            ),
            32: pygame.transform.smoothscale(
                pygame.image.load("assets/32.svg"), (115, 115)
            ),
            64: pygame.transform.smoothscale(
                pygame.image.load("assets/64.svg"), (115, 115)
            ),
            128: pygame.transform.smoothscale(
                pygame.image.load("assets/128.png"), (115, 115)
            ),
            256: pygame.transform.smoothscale(
                pygame.image.load("assets/256.svg"), (115, 115)
            ),
            512: pygame.transform.smoothscale(
                pygame.image.load("assets/512.svg"), (115, 115)
            ),
            1024: pygame.transform.smoothscale(
                pygame.image.load("assets/1024.svg"), (115, 115)
            ),
            2048: pygame.transform.smoothscale(
                pygame.image.load("assets/2048.svg"), (115, 115)
            ),
            4096: pygame.transform.smoothscale(
                pygame.image.load("assets/4096.svg"), (115, 115)
            ),
            8192: pygame.transform.smoothscale(
                pygame.image.load("assets/8192.svg"), (115, 115)
            ),
        }

    def draw(self, win):
        """Draw the board to the screen."""

        pygame.draw.rect(win, GREY, self.grid_rect, border_radius=10)
        for row in range(self.tile_gap, self.grid_rect.width, 125):
            for height in range(self.tile_gap, self.grid_rect.height, 125):
                rect = pygame.Rect(self.grid_rect.x + row, self.grid_rect.y + height, 115, 115)
                pygame.draw.rect(win, LIGHT_GREY, rect, border_radius=5)

        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val != 0:
                    win.blit(
                        self.images[val],
                        (
                            self.grid_rect.x + self.tile_gap + (j * 125),
                            self.grid_rect.y + self.tile_gap + (i * 125),
                        )
                    )

    def update(self, event):
        """Update the board based on user input."""

        if event.type == pygame.KEYDOWN:
            if self.move(event.key, []):
                self.random_tile()

    def reset(self):
        """Reset the board to the initial state."""

        self.board = [[0, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score = 0
    
    def random_tile(self):
        """Add a random tile (2 or 4) to an empty spot on the board."""

        empty = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if not self.board[i][j]:
                    empty.append((i, j))

        x, y = choice(empty)
        if randint(1, 10) == 1:
            self.board[x][y] = 4
        else:
            self.board[x][y] = 2


    def move(self, key, merged):
        """Move the tiles in the specified direction."""

        copy = deepcopy(self.board)
        i_range = []
        j_range = []
        match key:
            case pygame.K_LEFT:
                i_range = range(len(self.board))
                j_range = range(len(self.board))
                i_increment = 0
                j_increment = -1

            case pygame.K_RIGHT:
                i_range = range(len(self.board))
                j_range = range(len(self.board))[::-1]
                i_increment = 0
                j_increment = 1

            case pygame.K_UP:
                i_range = range(len(self.board))
                j_range = range(len(self.board))
                i_increment = -1
                j_increment = 0

            case pygame.K_DOWN:
                i_range = range(len(self.board))[::-1]
                j_range = range(len(self.board))
                i_increment = 1
                j_increment = 0

        if not i_range:
            return

        for i in i_range:
            for j in j_range:
                if self.board[i][j]:
                    tile = self.board[i][j]
                    next_i = i + i_increment
                    next_j = j + j_increment
                    if not (0 <= next_i <= 3 and 0 <= next_j <= 3):
                        continue
                    if (
                        tile == self.board[next_i][next_j]
                        and (next_i, next_j) not in merged
                        and (i, j) not in merged
                    ):
                        self.board[i][j] = 0
                        self.board[next_i][next_j] = 2 * tile
                        self.score += 2 * tile
                        merged.append((next_i, next_j))
                    elif self.board[next_i][next_j] == 0:
                        self.board[next_i][next_j] = tile
                        self.board[i][j] = 0

        if copy != self.board:
            self.move(key, merged)
            return self.board

        return False


    def game_over(self):
        """Check if the game is over (no more valid moves)."""

        if not any(row.count(0) for row in self.board):
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    tile = self.board[i][j]
                    if 0 < j < 3 and (tile == self.board[i][j + 1] or tile == self.board[i][j - 1]):
                        return False
                    if 0 < i < 3 and (tile == self.board[i + 1][j] or tile == self.board[i - 1][j]):
                        return False

            return True
        

class Menu:
    def __init__(self, win, x, y, buttons, bg_color, display=False):
        self.win = win
        self.x = x
        self.y = y
        self.buttons = buttons
        self.bg_color = bg_color
        self.display = display

        self.height = sum(button.rect.height for button in buttons) * 1.5
        self.width = max(button.rect.width for button in buttons) * 1.1

        ## x and y are center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)

        self.just_opened = False

    def draw(self):
        """Draw the menu and its buttons to the screen."""

        if not self.display:
            return

        pygame.draw.rect(self.win, self.bg_color, self.rect, border_radius=10)
        gaps = sum(button.rect.height for button in self.buttons) * 0.5 / (len(self.buttons) + 1)
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            button.rect.centerx = self.rect.centerx
            button.rect.y = self.rect.y + (i + 1) * gaps + sum(button.rect.height for button in self.buttons[:i])
            button.draw(self.win)

    def update(self, event):
        """Check if menu buttons are clicked and perform their actions."""

        if not self.display:
            return

        if self.just_opened:
            self.just_opened = False
            return

        for button in self.buttons:
            button.update(event)

    def open(self):
        self.display = True
        self.just_opened = True

    def close(self):
        self.display = False

class BackButton:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.transform.smoothscale(pygame.image.load("assets/back.png"), (50, 50))
        self.rect = self.img.get_rect(topleft=(x, y))

    def draw(self, win):
        """Draw the back button to the screen."""

        win.blit(self.img, self.rect)

    def clicked(self, event):
        """Check if the back button is clicked."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
