from .piece import Piece


class Rook(Piece):
    """
    A class that represents a Rook piece and controls all movement logic

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
        self.image = 8

    def __repr__(self):
        return "Rook"

    def valid_moves(self, board) -> list:
        """Determines valid moves for the Piece in the current gamestate

        :param board: reference to the Board object
        :return: List[Tuple[int, int]]
        """

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
