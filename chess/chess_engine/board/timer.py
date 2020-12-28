import pygame
from ...data.settings import *


class Timer:
    """
    A class that creates and manages a timer to limit the time each player has to make a move

    ...

    Attributes
    ----------
    time : int
        a variable to initialize the maximum countdown time (in seconds)
    pos : str
        a string to represent a particular position for placing the timer display

    Methods
    -------
    tick(dt)
        Decreases the current timer by a given number of seconds
    reset()
        Resets the timer back to the initial maximum value
    draw()
        Draws the timer display to the screen
    """

    def __init__(self, time: int, pos: str):
        """Class Parameters

        :param time: int
        :param pos: str
        """

        self.initial_time = time
        self.time = time
        self.pos = pos
        self.font = FONT

    def tick(self, dt: int) -> None:
        """Decreases the current timer by a given number of seconds

        :param dt: An integer representing the number of seconds to tick
        :return: None
        """

        self.time -= dt

    def reset(self) -> None:
        """Resets the timer back to the initial maximum value

        :return: None
        """

        self.time = self.initial_time

    def draw(self) -> None:
        """Draws the timer display to the screen

        :return: None
        """

        mins, secs = divmod(self.time, 60)
        ms = divmod(self.time, 1000)[1]
        if self.time <= 10:
            s = f'{ms:.01f}'
        else:
            s = f'{int(mins):02}:{int(secs):02}'
        txt = self.font.render(s, True, SMALL_TEXT_COLOR)
        if self.pos == "top":
            pygame.draw.rect(SCREEN, BG_COLOR_LIGHT, [BOARD_X + BOARD_SIZE - TILE_SIZE, BOARD_Y - 36, TILE_SIZE, 28])
            SCREEN.blit(txt, (BOARD_X + BOARD_SIZE - TILE_SIZE + 8, BOARD_Y - 34))
        else:
            pygame.draw.rect(SCREEN, BG_COLOR_LIGHT,
                             [BOARD_X+BOARD_SIZE-TILE_SIZE, BOARD_Y+BOARD_SIZE+8, TILE_SIZE, 28])
            SCREEN.blit(txt, (BOARD_X+BOARD_SIZE-TILE_SIZE+8, BOARD_Y+BOARD_SIZE+10))
