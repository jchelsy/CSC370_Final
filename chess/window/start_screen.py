import pygame
import os
from chess import img_dir
from ..data import *
from .widgets import Button

# Initialize Images
bg_img = pygame.image.load(os.path.join(img_dir, 'ui', 'background', 'start_bg.png'))
newgame_img = [os.path.join(img_dir, 'ui', 'button', 'newgame_default.png'),
               os.path.join(img_dir, 'ui', 'button', 'newgame_hover.png'),
               os.path.join(img_dir, 'ui', 'button', 'newgame_click.png')]
quit_img = [os.path.join(img_dir, 'ui', 'button', 'quit_default.png'),
            os.path.join(img_dir, 'ui', 'button', 'quit_hover.png'),
            os.path.join(img_dir, 'ui', 'button', 'quit_click.png')]


class StartScreen:
    """
    A class to execute and manage the Main Menu screen

    ...

    Methods
    -------
    draw(screen)
        Draws all screen components
    update(event)
        Updates and handles all widget events on the page
    """

    def __init__(self):
        self.background_image = bg_img

        self.newgame_button = Button(int((self.background_image.get_width() - 250) / 2),
                                     260, 250, 75, image=newgame_img)
        self.quit_button = Button(int((self.background_image.get_width() - 250) / 2),
                                  360, 250, 75, image=quit_img, space_around=45)

        self.running = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draws all screen components

        :param screen: the main pygame surface to blit all content onto
        :return: None
        """

        # Background
        screen.blit(self.background_image, self.background_image.get_rect())

        # Widgets
        for w in [self.newgame_button, self.quit_button]:
            w.draw(screen)

    def update(self, event) -> None:
        """Updates and handles all widget events on the page

        :param event: pygame event for widget event handling
        :return: None
        """

        for w in [self.newgame_button, self.quit_button]:
            w.handle_event(event)

            if w.command_switch:
                # 'New Game' button
                if w == self.newgame_button:
                    fade(self)
                    self.running = False
                # 'Quit' button
                elif w == self.quit_button:
                    pygame.quit()
                    exit()


def fade(page, max_alpha=255) -> None:
    """Creates a fading animation to transition between pages

    :param page: the page to fade out from
    :param max_alpha: the maximum alpha value (default: 255)
    :return: None
    """

    veil = SCREEN.copy()
    veil.fill((0, 0, 0))

    for alpha in range(0, max_alpha):
        veil.set_alpha(alpha)
        page.draw(SCREEN)
        SCREEN.blit(veil, (0, 0))
        pygame.display.update()
        pygame.time.delay(1)
