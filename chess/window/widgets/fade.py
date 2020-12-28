import pygame as pg


def fade(screen, page, out=False, max_alpha=255):
    alpha = 0
    veil = screen.copy()
    veil.fill((0, 0, 0))

    for alpha in range(0, max_alpha):
        veil.set_alpha(alpha)
        page.draw(screen)
        screen.blit(veil, (0, 0))
        pg.display.update()
        pg.time.delay(3)
