import pygame
import os
from chess import img_dir
from ..data import *
from .widgets import Button, Selector

# Initialize Images
bg_img = pygame.image.load(os.path.join(img_dir, 'ui', 'background', 'menu_bg.png'))
start_img = [os.path.join(img_dir, 'ui', 'button', 'start_default.png'),
             os.path.join(img_dir, 'ui', 'button', 'start_hover.png'),
             os.path.join(img_dir, 'ui', 'button', 'start_click.png')]
arrows = [os.path.join(img_dir, 'ui', 'selector', 'left_default.png'),
          os.path.join(img_dir, 'ui', 'selector', 'left_hover.png'),
          os.path.join(img_dir, 'ui', 'selector', 'left_click.png'),
          os.path.join(img_dir, 'ui', 'selector', 'left_disable.png'),
          os.path.join(img_dir, 'ui', 'selector', 'right_default.png'),
          os.path.join(img_dir, 'ui', 'selector', 'right_hover.png'),
          os.path.join(img_dir, 'ui', 'selector', 'right_click.png'),
          os.path.join(img_dir, 'ui', 'selector', 'right_disable.png')]
options = {"white": os.path.join(img_dir, 'ui', 'selector', 'option_white.png'),
           "black": os.path.join(img_dir, 'ui', 'selector', 'option_black.png'),
           "human": os.path.join(img_dir, 'ui', 'selector', 'option_human.png'),
           "computer": os.path.join(img_dir, 'ui', 'selector', 'option_computer.png')}


class NewGameMenu:
    """
    A class to execute and manage the 'New Game' pop-up from the Main Menu screen

    ...

    Attributes
    ----------
    names : tuple
        a tuple containing the updated names of both players
    colors : tuple
        a tuple containing the updated RGB color representation of both players

    Methods
    -------
    draw(screen)
        Draws all screen components
    update(event)
        Updates and handles all widget events on the page
    """

    def __init__(self, names, colors):
        """Class Parameters

        :param names: tuple
        :param colors: tuple
        """

        self.p1_name = names[0]
        self.p2_name = names[1]
        self.p1_color = colors[0]
        self.p2_color = colors[1]

        self.background_image = bg_img

        self.color_text = pygame.image.load(os.path.join(img_dir, 'ui', 'background', 'menu_text_color.png'))
        self.enemy_text = pygame.image.load(os.path.join(img_dir, 'ui', 'background', 'menu_text_enemy.png'))

        self.color_selector = Selector(140 + 240, 180, 260, 75,
                                       [(options['white'], WHITE), (options['black'], BLACK)],
                                       left_arrow=[arrows[0], arrows[1], arrows[2], arrows[3]],
                                       right_arrow=[arrows[4], arrows[5], arrows[6], arrows[7]])

        self.ai_selector = Selector(140 + 220, 260, 280, 75,
                                    [(options['computer'], "Computer"), (options['human'], "Player 2")],
                                    left_arrow=[arrows[0], arrows[1], arrows[2], arrows[3]],
                                    right_arrow=[arrows[4], arrows[5], arrows[6], arrows[7]])

        self.start_button = Button(int((SCREEN.get_width() - 250) / 2), 492, 250, 75,
                                   image=start_img, space_around=43)

        self.running = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draws all screen components

        :param screen: the main pygame surface to blit all content onto
        :return: None
        """

        # Background
        screen.fill((0, 0, 0))
        screen.blit(self.background_image,
                    pygame.Rect(int((screen.get_width() - self.background_image.get_width()) / 2),
                                int((screen.get_height() - self.background_image.get_height()) / 2),
                                self.background_image.get_width(),
                                self.background_image.get_height()))

        # Text
        screen.blit(self.color_text, (140, 180))
        screen.blit(self.enemy_text, (140, 260))

        # Widgets
        for w in [self.color_selector, self.ai_selector, self.start_button]:
            w.draw(screen)

    def update(self, event) -> None:
        """Updates and handles all widget events on the page

        :param event: pygame event for widget event handling
        :return: None
        """

        for w in [self.color_selector, self.ai_selector, self.start_button]:
            w.handle_event(event)

            if w.command_switch:
                # Color Selector
                if w == self.color_selector:
                    self.p1_color = self.color_selector.options[self.color_selector.current_index][1]
                    print(self.p1_color)

                # Opponent Selector
                if w == self.ai_selector:
                    self.p2_name = self.ai_selector.options[self.ai_selector.current_index][1]
                    print(self.p2_name)
                # 'Start' button
                if w == self.start_button:
                    fade(self)
                    self.running = False


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
