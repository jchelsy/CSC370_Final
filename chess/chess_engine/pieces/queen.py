from .piece import Piece
from .bishop import Bishop
from .rook import Rook


class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 2

    def __repr__(self):
        return "Queen"

    def valid_moves(self, board):
        # Queen's move set is Rook and Bishop combined
        moves = Rook.valid_moves(self, board) + Bishop.valid_moves(self, board)

        return moves

# # from chess.chess_engine.pieces import Piece
# # from chess.chess_engine.pieces import Rook
# # from chess.chess_engine.pieces import Bishop
# from .piece import Piece
# from .rook import Rook
# from .bishop import Bishop
#
#
# class Queen(Piece):
#     def __init__(self, x, y, color):
#         super().__init__(x, y, color)
#         self.image = 2
#
#     def __repr__(self):
#         return "Queen"
#
#     def valid_moves(self, board):
#         moves = Rook.valid_moves(self, board) + Bishop.valid_moves(self, board)
#
#         return moves
