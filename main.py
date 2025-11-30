import pygame
from pages.LoginPage import LoginPage
from widgets import BackButton
pygame.init()

WIDTH, HEIGHT = 1200, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
back = BackButton(20, 45)

def change_page(new_page):
    """"Callback function to change the current page"""
    global page
    page = new_page
    pages.append(page)

page = LoginPage(change_page, win)
pages = [page]

def main():
    """Main Event Loop"""

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            page.update(event)
            if back.clicked(event):
                page.clean()
                change_page(pages[-2])
                pages.pop()
                pages.pop()

        page.draw()

        if len(pages) > 1:
            back.draw(win)

        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()