from colors import *
import pygame
pygame.font.init()

class BlankPage:
    def __init__(self):
        self.bg = WHITE

    def draw(self, win):
        win.fill(self.bg)

    def update(self, win, event):
        self.draw(win)