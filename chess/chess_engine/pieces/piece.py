from ...data.settings import *
from ... import resource_dir
import os

bK = pygame.image.load(os.path.join(resource_dir, 'king-black.png'))
bQ = pygame.image.load(os.path.join(resource_dir, 'queen-black.png'))
bB = pygame.image.load(os.path.join(resource_dir, 'bishop-black.png'))
bN = pygame.image.load(os.path.join(resource_dir, 'knight-black.png'))
bR = pygame.image.load(os.path.join(resource_dir, 'rook-black.png'))
bp = pygame.image.load(os.path.join(resource_dir, 'pawn-black.png'))

wK = pygame.image.load(os.path.join(resource_dir, 'king-white.png'))
wQ = pygame.image.load(os.path.join(resource_dir, 'queen-white.png'))
wB = pygame.image.load(os.path.join(resource_dir, 'bishop-white.png'))
wN = pygame.image.load(os.path.join(resource_dir, 'knight-white.png'))
wR = pygame.image.load(os.path.join(resource_dir, 'rook-white.png'))
wp = pygame.image.load(os.path.join(resource_dir, 'pawn-white.png'))

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
          pygame.transform.scale(bp, IMG_SCALE)]  # 11 - Pawn (black)


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.image = None
        self.firstMove = True

    def draw(self):
        """Draws piece

        :return: None
        """

        if self.color == WHITE:
            SCREEN.blit(IMAGES[self.image], to_coords(self.x, self.y))
        else:
            SCREEN.blit(IMAGES[self.image+1], to_coords(self.x, self.y))

    def move(self, x, y):
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

# # from chess.data.settings import *
# from ...data.settings import *
#
# from chess import img_dir
# import os
#
# IMAGES = []
# for piece in ['wK', 'bK', 'wQ', 'bQ', 'wB', 'bB', 'wN', 'bN', 'wR', 'bR', 'wp', 'bp']:
#     img = pygame.image.load(os.path.join(img_dir, 'pieces', piece + ".png"))
#     IMAGES.append(pygame.transform.scale(img, IMG_SCALE))
#
#
# class Piece:
#     def __init__(self, x, y, color):
#         self.x = x
#         self.y = y
#         self.color = color
#         self.image = None
#         self.firstMove = True
#
#     def draw(self) -> None:
#         """Draws piece
#
#         :return: None
#         """
#
#         if self.color == WHITE:
#             SCREEN.blit(IMAGES[self.image], to_coords(self.x, self.y))
#         else:
#             SCREEN.blit(IMAGES[self.image + 1], to_coords(self.x, self.y))
#
#     def move(self, x, y) -> None:
#         """Updates x and y coordinates for Piece
#
#         :param x: x-coordinate
#         :type x: int
#         :param y: y-coordinate
#         :type y: int
#         :return: None
#         """
#
#         self.x = x
#         self.y = y
#
#     def copy(self):
#         """Creates a deep copy of the current Piece
#
#         :return: reference to a new Piece object
#         """
#
#         copy = type(self)(self.x, self.y, self.color)
#         copy.image = self.image
#         copy.firstMove = self.firstMove
#
#         return copy
