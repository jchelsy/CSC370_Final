from .piece import Piece
from .bishop import Bishop
from .rook import Rook


class Queen(Piece):
    """
    A class that represents a Queen piece and controls all movement logic

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
        self.image = 2

    def __repr__(self):
        return "Queen"

    def valid_moves(self, board) -> list:
        """Determines valid moves for the Piece in the current gamestate

        :param board: reference to the Board object
        :return: List[Tuple[int, int]]
        """

        # Queen's move set is Rook and Bishop combined
        moves = Rook.valid_moves(self, board) + Bishop.valid_moves(self, board)

        return moves
