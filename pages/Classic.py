from widgets import *
from colors import *
from pages import *
import pygame
pygame.font.init()

class Classic:
    def __init__(self, change_page, win):
        self.change+page = change_page
        self.win = win
        self.bg = BG_COLOR

        self.board = Board(())