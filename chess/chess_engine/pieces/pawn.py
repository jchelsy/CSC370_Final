from .piece import Piece


class Pawn(Piece):
    """
    A class that represents a Pawn piece and controls all movement logic

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
    valid_moves(board)
        Determines valid moves for the Piece in the current gamestate
    """

    def __init__(self, x: int, y: int, color: tuple):
        """Class Parameters

        :param x: int
        :param y: int
        :param color: tuple
        """

        super().__init__(x, y, color)
        self.image = 10

    def __repr__(self):
        return "Pawn"

    def valid_moves(self, board) -> list:
        """Determines valid moves for the Piece in the current gamestate

        :param board: reference to the Board object
        :return: List[Tuple[int, int]]
        """

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
