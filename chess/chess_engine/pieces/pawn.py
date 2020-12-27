from .piece import Piece


class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 10

    def __repr__(self):
        return "Pawn"

    def valid_moves(self, board):
        moves = []

        if board.bottomPlayerTurn:
            # Move forward 1
            if board.valid_move((self.x, self.y-1), self.color) \
                    and not board.piece_at_coords((self.x, self.y-1)):
                moves.append((self.x, self.y-1))

                # Move forward 2 (on first move)
                if board.valid_move((self.x, self.y-2), self.color) \
                        and not board.piece_at_coords((self.x, self.y-2)) \
                        and self.firstMove:
                    moves.append((self.x, self.y-2))

            # Attack Diagonal-Left
            if board.valid_move((self.x-1, self.y-1), self.color) \
                    and board.enemy_at_coords((self.x-1, self.y-1), self.color):
                moves.append((self.x-1, self.y-1))

            # Attack Diagonal-Right
            if board.valid_move((self.x+1, self.y-1), self.color) \
                    and board.enemy_at_coords((self.x+1, self.y-1), self.color):
                moves.append((self.x+1, self.y-1))
        else:
            # Move forward 1
            if board.valid_move((self.x, self.y+1), self.color) \
                    and not board.piece_at_coords((self.x, self.y+1)):
                moves.append((self.x, self.y+1))

                # Move forward 2 (on first move)
                if board.valid_move((self.x, self.y+2), self.color) \
                        and not board.piece_at_coords((self.x, self.y+2)) \
                        and self.firstMove:
                    moves.append((self.x, self.y+2))

            # Attack Diagonal-Left
            if board.valid_move((self.x-1, self.y+1), self.color) \
                    and board.enemy_at_coords((self.x-1, self.y+1), self.color):
                moves.append((self.x-1, self.y+1))

            # Attack Diagonal-Right
            if board.valid_move((self.x+1, self.y+1), self.color) \
                    and board.enemy_at_coords((self.x+1, self.y+1), self.color):
                moves.append((self.x+1, self.y+1))

        return list(set(moves))

# # from chess.chess_engine.pieces import Piece
# from .piece import Piece
#
#
# class Pawn(Piece):
#     def __init__(self, x, y, color):
#         super().__init__(x, y, color)
#         self.image = 10
#
#     def __repr__(self):
#         return "Pawn"
#
#     def valid_moves(self, board):
#         moves = []
#
#         if board.bottomPlayerTurn:
#             # Move forward 1
#             if board.valid_move((self.x, self.y-1), self.color) \
#                     and not board.piece_at_coords((self.x, self.y-1)):
#                 moves.append((self.x, self.y-1))
#
#                 # Move forward 2 (on first move)
#                 if board.valid_move((self.x, self.y-2), self.color) \
#                         and not board.piece_at_coords((self.x, self.y-2)) \
#                         and self.firstMove:
#                     moves.append((self.x, self.y-2))
#
#             # Attack Diagonal Left
#             if board.valid_move((self.x-1, self.y-1), self.color) \
#                     and board.enemy_at_coords((self.x-1, self.y-1), self.color):
#                 moves.append((self.x-1, self.y-1))
#
#             # Attack Diagonal Right
#             if board.valid_move((self.x+1, self.y-1), self.color) \
#                     and board.enemy_at_coords((self.x+1, self.y-1), self.color):
#                 moves.append((self.x+1, self.y-1))
#         else:
#             # Move forward 1
#             if board.valid_move((self.x, self.y+1), self.color) \
#                     and not board.piece_at_coords((self.x, self.y+1)):
#                 moves.append((self.x, self.y+1))
#
#                 # Move forward 2 (on first move)
#                 if board.valid_move((self.x, self.y+2), self.color) \
#                         and not board.piece_at_coords((self.x, self.y+2)) \
#                         and self.firstMove:
#                     moves.append((self.x, self.y+2))
#
#             # Attack Diagonal Left
#             if board.valid_move((self.x-1, self.y+1), self.color) \
#                     and board.enemy_at_coords((self.x-1, self.y+1), self.color):
#                 moves.append((self.x-1, self.y+1))
#
#             # Attack Diagonal Right
#             if board.valid_move((self.x+1, self.y+1), self.color) \
#                     and board.enemy_at_coords((self.x+1, self.y+1), self.color):
#                 moves.append((self.x+1, self.y+1))
#
#         return list(set(moves))
