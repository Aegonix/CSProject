import pygame
from pages.WelcomePage import WelcomePage
from widgets import BackButton
pygame.init()

WIDTH, HEIGHT = 1200, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
back = BackButton(20, 20)

def change_page(new_page):
    global page
    page = new_page
    pages.append(page)

page = WelcomePage(change_page, win)
pages = [page]

def main():
    global page

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