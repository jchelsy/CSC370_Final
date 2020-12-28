import pygame
import os
from ...data import *
from ... import img_dir

piece_dir = os.path.join(img_dir, 'pieces')

bK = pygame.image.load(os.path.join(piece_dir, 'black_king.png'))
bQ = pygame.image.load(os.path.join(piece_dir, 'black_queen.png'))
bB = pygame.image.load(os.path.join(piece_dir, 'black_bishop.png'))
bN = pygame.image.load(os.path.join(piece_dir, 'black_knight.png'))
bR = pygame.image.load(os.path.join(piece_dir, 'black_rook.png'))
bp = pygame.image.load(os.path.join(piece_dir, 'black_pawn.png'))

wK = pygame.image.load(os.path.join(piece_dir, 'white_king.png'))
wQ = pygame.image.load(os.path.join(piece_dir, 'white_queen.png'))
wB = pygame.image.load(os.path.join(piece_dir, 'white_bishop.png'))
wN = pygame.image.load(os.path.join(piece_dir, 'white_knight.png'))
wR = pygame.image.load(os.path.join(piece_dir, 'white_rook.png'))
wp = pygame.image.load(os.path.join(piece_dir, 'white_pawn.png'))

IMAGES = [pygame.transform.scale(wK, IMG_SCALE),  # 0  - King (white)
          pygame.transform.scale(bK, IMG_SCALE),  # 1  - King (black)
          pygame.transform.scale(wQ, IMG_SCALE),  # 2  - Queen (white)
          pygame.transform.scale(bQ, IMG_SCALE),  # 3  - Queen (black)
          pygame.transform.scale(wB, IMG_SCALE),  # 4  - Bishop (white)
          pygame.transform.scale(bB, IMG_SCALE),  # 5  - Bishop (black)
          pygame.transform.scale(wN, IMG_SCALE),  # 6  - Knight (white)
          pygame.transform.scale(bN, IMG_SCALE),  # 7  - Knight (black)
          pygame.transform.scale(wR, IMG_SCALE),  # 8  - Rook (white)
          pygame.transform.scale(bR, IMG_SCALE),  # 9  - Rook (black)
          pygame.transform.scale(wp, IMG_SCALE),  # 10 - Pawn (white)
          pygame.transform.scale(bp, IMG_SCALE)   # 11 - Pawn (black)
          ]


class Piece:
    """
    A class that represents a chess Piece and controls all movement logic

    ...

    Attributes
    ----------
    x : int
        an integer representing the x-coordinate of the Piece on the board
    y : int
        an integer representing the y-coordinate of the Piece on the board
    color : tuple
        a tuple representing the RGB color of the Piece (WHITE / BLACK)

    Methods
    -------
    draw()
        Draws the current Piece at its specified coordinates
    move(x, y)
        Updates the x- and y-coordinates of the current Piece
    copy()
        Creates a deep copy of the current Piece
    """

    def __init__(self, x: int, y: int, color: tuple):
        """Class Parameters

        :param x: int
        :param y: int
        :param color: tuple
        """

        self.x = x
        self.y = y
        self.color = color
        self.image = None
        self.firstMove = True

    def draw(self) -> None:
        """Draws a Piece at its given coordinates

        :return: None
        """

        if self.color == WHITE:
            SCREEN.blit(IMAGES[self.image], to_coords(self.x, self.y))
        else:
            SCREEN.blit(IMAGES[self.image+1], to_coords(self.x, self.y))

    def move(self, x: int, y: int) -> None:
        """Updates x and y coordinates for Piece

        :param x: x-coordinate
        :param y: y-coordinate
        :return: None
        """

        self.x = x
        self.y = y

    def copy(self):
        """Creates a deep copy of the current Piece

        :return: reference to a new Piece object
        """

        copy = type(self)(self.x, self.y, self.color)
        copy.image = self.image
        copy.firstMove = self.firstMove
        return copy
