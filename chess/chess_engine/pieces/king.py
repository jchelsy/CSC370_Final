from .piece import Piece


class King(Piece):
    """
    A class that represents a King piece and controls all movement logic

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
        self.image = 0

    def __repr__(self):
        return "King"

    def valid_moves(self, board) -> list:
        """Determines valid moves for the Piece in the current gamestate

        :param board: reference to the Board object
        :return: List[Tuple[int, int]]
        """

        moves = []

        # Move 1 in each direction
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if board.valid_move((x, y), self.color):
                    moves.append((x, y))
        return moves
