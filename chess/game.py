import pygame
import os
from chess import img_dir
from chess.data import *
from chess.window import StartScreen, NewGameMenu, ChessScreen


class Game:
    """
    The controller class for the Game

    ...

    Methods
    -------
    run()
        Initializes the running of the Game
    handle_events()
        Initializes the event handling for the pages
    draw()
        Draws the current page to the screen
    """

    def __init__(self):
        pygame.display.set_caption("Chess")
        pygame.display.set_icon(pygame.image.load(os.path.join(img_dir, 'icon.png')))

        self.clock = pygame.time.Clock()

        # Variables
        self.p1_name = "Player 1"
        self.p2_name = "Computer"

        self.p1_color = WHITE
        self.p2_color = BLACK

        self.pages = {"start": StartScreen(),
                      "menu": NewGameMenu((self.p1_name, self.p2_name), (self.p1_color, self.p2_color)),
                      "chess": ChessScreen(self.p1_name, self.p1_color, self.p2_name)}
        self.current_page = self.pages["start"]

    def run(self) -> None:
        """Initializes the running of the Game

        :return: None
        """

        while True:
            self.clock.tick(60)

            self.handle_events()
            self.draw()

    def handle_events(self) -> None:
        """Initializes the event handling for the pages

        :return: None
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            self.current_page.update(event)

    def draw(self) -> None:
        """Draws the current page to the screen

        :return: None
        """

        # Is there a page transition?
        if type(self.current_page) == StartScreen and not self.current_page.running:
            self.p2_name = self.pages["menu"]

            self.pages["title"] = StartScreen()
            self.current_page = self.pages["menu"]
            fade(self.current_page)

        elif type(self.current_page) == NewGameMenu and not self.current_page.running:
            # Add p1_name Textbox
            self.p1_color = self.pages["menu"].p1_color  # Player color

            self.p2_name = self.pages["menu"].p2_name  # "Computer" / "Human"

            print("\n\n" + str(self.p1_color) + "\n" + str(self.p2_name) + "\n\n")

            self.pages["menu"] = NewGameMenu((self.p1_name, self.p2_name), (self.p1_color, self.p2_color))
            self.pages["chess"] = ChessScreen(self.p1_name, self.p1_color, self.p2_name)

            self.current_page = self.pages["chess"]
            # fade_in(self.SCREEN, self.current_page)
            self.current_page.run()

        elif type(self.current_page) == ChessScreen and not self.current_page.running:
            self.pages["chess"] = ChessScreen(self.p1_name, self.p1_color, self.p2_name)
            print("BOOM!")
            self.current_page = self.pages["title"]
            fade(self.current_page)

        else:  # If there is no page transition
            self.current_page.draw(SCREEN)
            pygame.display.update()


def fade(page, max_alpha=255) -> None:
    """Creates a fade-in animation to transition to a page

    :param page: the page to fade in to
    :param max_alpha: the maximum alpha value (default: 255)
    :return: None
    """

    veil = SCREEN.copy()
    veil.fill((0, 0, 0))

    for alpha in reversed(range(0, max_alpha)):
        veil.set_alpha(alpha)
        page.draw(SCREEN)
        SCREEN.blit(veil, (0, 0))
        pygame.display.update()
        pygame.time.delay(1)
