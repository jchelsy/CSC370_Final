from ...data.settings import *


class Tile:
    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y
        self.color = BLACK
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))

    def fill(self, color):
        """Fills tile with specified color

        :param color: tile fill color
        :return: None
        """

        self.surface.fill(color)

    def select(self):
        """Applies highlighted effect to the Tile, indicating selection

        :return: None
        """

        if self.contains_piece():
            self.fill(HIGHLIGHT_COLOR)
            self.draw()

    def draw(self):
        """Draws the Tile and (if applicable) the piece it contains

        :return: None
        """

        SCREEN.blit(self.surface, to_coords(self.x, self.y))
        if self.piece:
            self.piece.draw()

    def contains_piece(self):
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

# # from chess.data.settings import *
# from ...data.settings import *
#
#
# class Tile:
#     def __init__(self, piece, x, y):
#         self.piece = piece
#         self.x = x
#         self.y = y
#         self.color = BLACK
#         self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
#
#     def fill(self, color) -> None:
#         """Fills tile with specified color
#
#         :param color: tile fill color
#         :type color: tuple
#         :return: None
#         """
#
#         self.surface.fill(color)
#
#     def select(self) -> None:
#         """Applies highlighted effect to tile, indicating selection
#
#         :return: None
#         """
#
#         if self.contains_piece():
#             self.fill(HIGHLIGHT_COLOR)
#             self.draw()
#
#     def draw(self) -> None:
#         """Draws tile and (if applicable) the piece it contains
#
#         :return: None
#         """
#
#         SCREEN.blit(self.surface, to_coords(self.x, self.y))
#         if self.piece:
#             self.piece.draw()
#
#     def contains_piece(self) -> bool:
#         """Checks if Tile contains a piece
#
#         :returns: a boolean representing whether or not Tile contains a piece
#         :rtype: bool
#         """
#
#         if self.piece.image is None:
#             return False
#         return True
#
#     def copy(self):
#         """Creates a deep copy of the current Tile
#
#         :return: reference to a new Tile object
#         """
#
#         piece = None
#         if self.piece:
#             piece = self.piece.copy()
#
#         copy = Tile(piece, self.x, self.y)
#         copy.fill(self.color)
#
#         return copy
