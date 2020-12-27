from .piece import Piece


class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 0

    def __repr__(self):
        return "King"

    def valid_moves(self, board):
        moves = []

        # Move 1 in each direction
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if board.valid_move((x, y), self.color):
                    moves.append((x, y))
        return moves

# # from chess.chess_engine.pieces import Piece
# from .piece import Piece
#
#
# class King(Piece):
#     def __init__(self, x, y, color):
#         super().__init__(x, y, color)
#         self.image = 0
#
#     def __repr__(self):
#         return "King"
#
#     def valid_moves(self, board):
#         moves = []
#
#         # Move in 1 direction
#         for x in range(self.x-1, self.x+2):
#             for y in range(self.y-1, self.y+2):
#                 if board.valid_move((x, y), self.color):
#                     moves.append((x, y))
#
#         return moves
