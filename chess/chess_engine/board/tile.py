import pygame
from ...data.settings import *


class Tile:
    """
    A class that represents each tile in the chess board grid (8x8)

    ...

    Attributes
    ----------
    piece : Piece object (default: None)
        a variable representing a chess piece contained within the Tile
    x : int
        an integer representing the x-coordinate of the Tile on the board
    y : int
        an integer representing the y-coordinate of the Tile on the board

    Methods
    -------
    fill(color)
        Fills tile with specified color
    select()
        Applies a highlighted effect to the Tile
    draw()
        Draws the Tile and (if applicable) the piece it contains
    contains_piece()
        Checks if the Tile contains a piece
    copy()
        Creates a deep copy of the current Tile
    """

    def __init__(self, piece, x: int, y: int):
        """Class Parameters

        :param piece: reference to a Piece object
        :param x: int
        :param y: int
        """

        self.piece = piece
        self.x = x
        self.y = y
        self.color = BLACK
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))

    def fill(self, color: tuple) -> None:
        """Fills tile with specified color

        :param color: RGB color representation to fill the tile with
        :return: None
        """

        self.surface.fill(color)

    def select(self) -> None:
        """Applies a highlighted effect to the Tile, indicating selection

        :return: None
        """

        if self.contains_piece():
            self.fill(HIGHLIGHT_COLOR)
            self.draw()

    def draw(self) -> None:
        """Draws the Tile and (if applicable) the piece it contains

        :return: None
        """

        SCREEN.blit(self.surface, to_coords(self.x, self.y))
        if self.piece:
            self.piece.draw()

    def contains_piece(self) -> bool:
        """Checks if the Tile contains a piece

        :return: a boolean representing whether or not the Tile contains a piece
        """

        if self.piece.image is None:
            return False
        return True

    def copy(self):
        """Creates a deep copy of the current Tile

        :return: reference to a new Tile object
        """

        piece = None
        if self.piece:
            piece = self.piece.copy()

        copy = Tile(piece, self.x, self.y)
        copy.fill(self.color)

        return copy
