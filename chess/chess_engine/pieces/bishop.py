from .piece import Piece


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 4

    def __repr__(self):
        return "Bishop"

    def valid_moves(self, board):
        moves = []

        # Up-Left
        x, y = self.x, self.y
        while board.valid_move((x-1, y-1), self.color):
            moves.append((x-1, y-1))
            if board.piece_at_coords((x-1, y-1)):
                break
            x -= 1
            y -= 1

        # Up-Right
        x, y = self.x, self.y
        while board.valid_move((x+1, y-1), self.color):
            moves.append((x+1, y-1))
            if board.piece_at_coords((x+1, y-1)):
                break
            x += 1
            y -= 1

        # Down-Left
        x, y = self.x, self.y
        while board.valid_move((x-1, y+1), self.color):
            moves.append((x-1, y+1))
            if board.piece_at_coords((x-1, y+1)):
                break
            x -= 1
            y += 1

        # Down-Right
        x, y = self.x, self.y
        while board.valid_move((x+1, y+1), self.color):
            moves.append((x+1, y+1))
            if board.piece_at_coords((x+1, y+1)):
                break
            x += 1
            y += 1

        return moves

# # from chess.chess_engine.pieces import Piece
# from .piece import Piece
#
#
# class Bishop(Piece):
#     def __init__(self, x, y, color):
#         super().__init__(x, y, color)
#         self.image = 4
#
#     def __repr__(self):
#         return "Bishop"
#
#     def valid_moves(self, board):
#         moves = []
#
#         # Up Left
#         x, y = self.x, self.y
#         while board.valid_move((x-1, y-1), self.color):
#             moves.append((x-1, y-1))
#             if board.piece_at_coords((x-1, y-1)):
#                 break
#             x -= 1
#             y -= 1
#
#         # Up Right
#         x, y = self.x, self.y
#         while board.valid_move((x+1, y-1), self.color):
#             moves.append((x+1, y-1))
#             if board.piece_at_coords((x+1, y-1)):
#                 break
#             x += 1
#             y -= 1
#
#         # Down Left
#         x, y = self.x, self.y
#         while board.valid_move((x-1, y+1), self.color):
#             moves.append((x-1, y+1))
#             if board.piece_at_coords((x-1, y+1)):
#                 break
#             x -= 1
#             y += 1
#
#         # Down Right
#         x, y = self.x, self.y
#         while board.valid_move((x+1, y+1), self.color):
#             moves.append((x+1, y+1))
#             if board.piece_at_coords((x+1, y+1)):
#                 break
#             x += 1
#             y += 1
#
#         return moves
