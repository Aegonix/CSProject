from widgets import *
from colors import *
from pages import WelcomePage
import mysql.connector as sql
import pygame
pygame.key.start_text_input()
pygame.font.init()


class LoginPage:
    def __init__(self, change_page, win):
        self.change_page = change_page
        self.bg = BG_COLOR
        self.win = win
        self.input_text_font = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 30)
        self.text_font = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", 35)
        self.logo = pygame.transform.smoothscale(
            pygame.image.load("assets/logo.png"), (375, 225)
        )
        self.creating = False
        self.error = False

        self.conn = sql.connect(
            host="localhost", user="root", password="sqlpassword", database="PROJECTDB"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS USERS (USERNAME VARCHAR(30) PRIMARY KEY, PASSWORD VARCHAR(30), HIGH_SCORE INT)")

        self.username_text = self.text_font.render("Username:", True, BLACK)
        self.username_rect = self.username_text.get_rect(bottomleft=(425, 325))
        self.username_input = TextBox(600, 350, self.input_text_font, 350)

        self.password_text = self.text_font.render("Password:", True, BLACK)
        self.password_rect = self.password_text.get_rect(bottomleft=(425, 425))
        self.password_input = TextBox(600, 450, self.input_text_font, 350)

        self.login_error_text = self.text_font.render(
            "Incorrect username or password.", True, RED
        )
        self.login_error_rect = self.login_error_text.get_rect(center=(600, 665))
        self.creation_error_text = self.text_font.render("Username already taken." , True, RED)
        self.creation_error_rect = self.creation_error_text.get_rect(center=(600, 665))

        self.login_button = Button(
            600,
            525,
            x_scale=3.3,
            y_scale=1.1,
            text="Login",
            font=self.text_font,
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=lambda: self.check_login(),
        )

        self.create_account_button = Button(
            600,
            600,
            x_scale=1.18,
            y_scale=1.1,
            text="Create Account",
            font=self.text_font,
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=lambda: self.change_creating(),
        )

        self.create_button = Button(
            600,
            525,
            x_scale=2.8,
            y_scale=1.1,
            text="Create",
            font=self.text_font,
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=lambda: self.create_account(),
        )

        self.back_button = Button(
            600,
            600,
            x_scale=4.2,
            y_scale=1.1,
            text="Back",
            font=self.text_font,
            color=LIGHT_YELLOW,
            text_color=BLACK,
            action=lambda: self.change_creating(),
        )

    def create_account(self):
        """Create a new account in the database."""

        username = self.username_input.grab()
        password = self.password_input.grab()
        try:
            self.cursor.execute(
                "INSERT INTO USERS VALUES (%s, %s, %s)",
                (username, password, 0),
            )
        except sql.errors.IntegrityError:
            self.error = True
            return

        self.conn.commit()
        self.username_input.clear()
        self.password_input.clear()
        self.change_creating()

    def check_login(self):
        """Check the login credentials against the database."""

        username = self.username_input.grab()
        password = self.password_input.grab()
        self.cursor.execute("SELECT * FROM USERS")
        users = self.cursor.fetchall()
        for user in users:
            if user[0] == username and user[1] == password:
                user_dict = {
                    "username": user[0],
                    "password": user[1],
                    "high_score": user[2]
                }
                self.clean()
                self.change_page(
                    WelcomePage.WelcomePage(self.change_page, user_dict, self.win)
                )
                return
        self.error = True

    def change_creating(self):
        """Toggle between login and create account modes."""

        self.creating = not self.creating
        self.error = False

    def draw(self):
        """Draw the elements of the login page to the screen."""

        self.win.fill(self.bg)
        logo_rect = self.logo.get_rect(center=(600, 150))
        logo_bg_rect = pygame.Rect(0, logo_rect.top, 1200, logo_rect.height)
        pygame.draw.rect(self.win, LOGO_YELLOW, logo_bg_rect)
        self.win.blit(self.logo, logo_rect)

        self.win.blit(self.username_text, self.username_rect)
        self.username_input.draw(self.win)

        self.win.blit(self.password_text, self.password_rect)
        self.password_input.draw(self.win)

        if self.creating:
            self.create_button.draw(self.win)
            self.back_button.draw(self.win)
        else:
            self.login_button.draw(self.win)
            self.create_account_button.draw(self.win)

        if self.error:
            if self.creating:
                self.win.blit(self.creation_error_text, self.creation_error_rect)
            else:
                self.win.blit(self.login_error_text, self.login_error_rect)


    def update(self, event):
        """Update the login page based on user input."""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.username_input.active = False
                self.password_input.active = True

        self.username_input.update(event, self.password_input)
        self.password_input.update(event, self.username_input)
        if self.creating:
            self.create_button.update(event)
            self.back_button.update(event)
        else:
            self.login_button.update(event)
            self.create_account_button.update(event)

    def clean(self):
        self.username_input.clear()
        self.password_input.clear()
        self.error = False
        self.creating = False
        self.conn.close()
        pygame.key.stop_text_input()
