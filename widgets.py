import pygame
from colors import *

pygame.font.init()


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        x_scale: float,
        y_scale: float,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        text_color: tuple,
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

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, self.rect, border_radius=self.border_radius
        )
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.action()


class Board:
    def __init__(self, topleft, size):
        self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.topleft = topleft
        self.size = size
        self.tile_gap = 10
        self.grid_rect = pygame.Rect(topleft, (size, size))

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
                pygame.image.load("assets/128.svg"), (115, 115)
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
        pygame.draw.rect(win, GREY, self.grid_rect, border_radius=10)
        for row in range(self.grid_rect.x + self.tile_gap, self.grid_rect.width, 125):
            for height in range(self.grid_rect.y + self.tile_gap, self.grid_rect.height, 125):
                rect = pygame.Rect(row, height, 115, 115)
                pygame.draw.rect(win, LIGHT_GREY, rect, border_radius=5)

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

