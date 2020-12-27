from .piece import Piece


class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 6

    def __repr__(self):
        return "Knight"

    def valid_moves(self, board):
        moves = []

        # Move 1 Diagonal and 1 Straight
        for x in range(self.x-2, self.x+3):
            for y in range(self.y-2, self.y+3):
                if abs(self.x - x) == 2 and abs(self.y - y) == 1 or abs(self.x - x) == 1 and abs(self.y - y) == 2:
                    if board.valid_move((x, y), self.color):
                        moves.append((x, y))
        return moves

# # from chess.chess_engine.pieces import Piece
# from .piece import Piece
#
#
# class Knight(Piece):
#     def __init__(self, x, y, color):
#         super().__init__(x, y, color)
#         self.image = 6
#
#     def __repr__(self):
#         return "Knight"
#
#     def valid_moves(self, board):
#         moves = []
#
#         # Move 1 diagonal and 1 straight
#         for x in range(self.x-2, self.x+3):
#             for y in range(self.y-2, self.y+3):
#                 if abs(self.x - x) == 2 and abs(self.y - y) == 1 or abs(self.x - x) == 1 and abs(self.y - y) == 2:
#                     if board.valid_move((x, y), self.color):
#                         moves.append((x, y))
#
#         return moves
