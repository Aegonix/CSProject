from widgets import *
from colors import *
from pages import Classic, VsAI, VsFriend, WatchAI
import pygame
pygame.font.init()

class WelcomePage:
    def __init__(self, change_page, win):
        self.change_page = change_page
        self.bg = BG_COLOR
        self.win = win
        self.text_font = pygame.font.SysFont("JetBrains Mono", 40)
        self.logo = pygame.transform.smoothscale(
            pygame.image.load("assets/logo_up.png"), (375, 225)
        )

        classic_button = Button(
            x=0,
            y=0,
            x_scale=1.3,
            y_scale=1.05,
            text="Play Classic",
            font=self.text_font,
            color=(240, 225, 24),
            text_color=BLACK,
            action=lambda: self.change_page(Classic.Classic(self.change_page, win)),
            border_radius=5
        )

        vs_ai_button = Button(
            x=0,
            y=0,
            x_scale=1.25,
            y_scale=1.05,
            text="Play Against AI",
            font=self.text_font,
            color=(240, 225, 24),
            text_color=BLACK,
            action=lambda: self.change_page(VsAI.VsAI(self.change_page, win)),
            border_radius=5
        )

        play_friend_button = Button(
            x=0,
            y=0,
            x_scale=1.15,
            y_scale=1.05,
            text="Play Against Friend",
            font=self.text_font,
            color=(240, 225, 24),
            text_color=BLACK,
            action=lambda: self.change_page(VsFriend.VsFriend(self.change_page, win)),
            border_radius=5
        )

        watch_ai_button = Button(
            x=0,
            y=0,
            x_scale=1.5,
            y_scale=1.05,
            text="Watch AI Play",
            font=self.text_font,
            color=(240, 225, 24),
            text_color=BLACK,
            action=lambda: self.change_page(WatchAI.WatchAI(self.change_page, win)),
            border_radius=5
        )

        close_button = Button(
            x=0,
            y=0,
            x_scale=1.5,
            y_scale=1.05,
            text="Close",
            font=self.text_font,
            color=RED,
            text_color=BLACK,
            action=lambda: self.play_menu.close(),
            border_radius=5
        )

        self.play_menu = Menu(
            win,
            600,
            350,
            [classic_button, vs_ai_button, play_friend_button, watch_ai_button, close_button],
            GREY,
        )

        self.play_button = Button(
            x=600,
            y=350,
            x_scale=2.5,
            y_scale=1.05,
            text="Play",
            font=self.text_font,
            color=(240, 225, 24),
            text_color=BLACK,
            action=lambda: self.play_menu.open(),
            border_radius=5
        )

        self.quit_button = Button(
            x=600,
            y=425,
            x_scale=2.5,
            y_scale=1.05,
            text="Quit",
            font=self.text_font,
            color=RED,
            text_color=BLACK,
            action=lambda: exit(),
            border_radius=5
        )


    def draw(self):
        self.win.fill(self.bg)
        self.play_button.draw(self.win)
        self.quit_button.draw(self.win)
        logo_rect = self.logo.get_rect(center=(600, 150))
        logo_bg_rect = pygame.Rect(0, logo_rect.top, 1200, logo_rect.height)
        pygame.draw.rect(self.win, YELLOW, logo_bg_rect)
        self.win.blit(self.logo, logo_rect)
        self.play_menu.draw()

    def update(self, event):
        if not self.play_menu.display:
            self.play_button.update(event)
            self.quit_button.update(event)
        self.play_menu.update(event)