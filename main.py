import pygame
from pages.WelcomePage import WelcomePage
pygame.init()

WIDTH, HEIGHT = 1200, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def change_page(new_page):
    global page
    page = new_page

page = WelcomePage(change_page, win)

def main():
    global page

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            page.update(win, event)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()