from .piece import Piece


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 8

    def __repr__(self):
        return "Rook"

    def valid_moves(self, board):
        moves = []

        # Up
        for y in range(self.y-1, -1, -1):
            if board.valid_move((self.x, y), self.color):
                moves.append((self.x, y))
            if board.piece_at_coords((self.x, y)):
                break

        # Down
        for y in range(self.y+1, 8, 1):
            if board.valid_move((self.x, y), self.color):
                moves.append((self.x, y))
            if board.piece_at_coords((self.x, y)):
                break

        # Left
        for x in range(self.x-1, -1, -1):
            if board.valid_move((x, self.y), self.color):
                moves.append((x, self.y))
            if board.piece_at_coords((x, self.y)):
                break

        # Right
        for x in range(self.x+1, 8, 1):
            if board.valid_move((x, self.y), self.color):
                moves.append((x, self.y))
            if board.piece_at_coords((x, self.y)):
                break

        return moves

# # from chess.chess_engine.pieces import Piece
# from .piece import Piece
#
#
# class Rook(Piece):
#     def __init__(self, x, y, color):
#         super().__init__(x, y, color)
#         self.image = 8
#
#     def __repr__(self):
#         return "Rook"
#
#     def valid_moves(self, board):
#         moves = []
#
#         # Up
#         for y in range(self.y-1, -1, -1):
#             if board.valid_move((self.x, y), self.color):
#                 moves.append((self.x, y))
#             if board.piece_at_coords((self.x, y)):
#                 break
#
#         # Down
#         for y in range(self.y+1, 8, 1):
#             if board.valid_move((self.x, y), self.color):
#                 moves.append((self.x, y))
#             if board.piece_at_coords((self.x, y)):
#                 break
#
#         # Left
#         for x in range(self.x-1, -1, -1):
#             if board.valid_move((x, self.y), self.color):
#                 moves.append((x, self.y))
#             if board.piece_at_coords((x, self.y)):
#                 break
#
#         # Right
#         for x in range(self.x+1, 8, 1):
#             if board.valid_move((x, self.y), self.color):
#                 moves.append((x, self.y))
#             if board.piece_at_coords((x, self.y)):
#                 break
#
#         return moves
