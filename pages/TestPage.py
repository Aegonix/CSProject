from widgets import *
from colors import *
from pages.BlankPage import BlankPage
import pygame
pygame.font.init()

class TestPage:
    def __init__(self, change_page):
        self.change_page = change_page
        self.count = 0
        self.bg = BG_COLOR
        self.font = pygame.font.SysFont("JetBrains Mono", 30)
        self.increment_button = Button(
            x=600,
            y=450,
            x_scale=1.1,
            y_scale=1.1,
            text="Increment Counter",
            font=self.font,
            color=GREEN,
            text_color=BLACK,
            action=self.increment_count,
            border_radius=5
        )
        ## Create decrement button, make it red and change the name but keep everything else same
        self.decrement_button = Button(
            x=600,
            y=500,
            x_scale=1.1,
            y_scale=1.1,
            text="Decrement Counter",
            font=self.font,
            color=RED,
            text_color=BLACK,
            action=self.decrement_count,
            border_radius=5
        )
        ### Create a done button, yellow, action returns BlankPage(), under decrement button
        self.done_button = Button(
            x=600,
            y=550,
            x_scale=1.5,
            y_scale=1.1,
            text="Done",
            font=self.font,
            color=YELLOW,
            text_color=BLACK,
            action=lambda: self.change_page(BlankPage()),
            border_radius=5
        )

    def increment_count(self):
        self.count += 1

    def decrement_count(self):
        self.count -= 1

    def draw(self, win):
        win.fill(self.bg)
        count_text = self.font.render(f"Count: {self.count}", True, BLACK)
        count_rect = count_text.get_rect(center=(600, 300))
        win.blit(count_text, count_rect)
        self.increment_button.draw(win)
        self.decrement_button.draw(win)
        self.done_button.draw(win)

    def update(self, win, event):
        self.increment_button.update(event)
        self.decrement_button.update(event)
        self.done_button.update(event)
        self.draw(win)