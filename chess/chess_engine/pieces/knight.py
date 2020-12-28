from .piece import Piece


class Knight(Piece):
    """
    A class that represents a Knight piece and controls all movement logic

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
        self.image = 6

    def __repr__(self):
        return "Knight"

    def valid_moves(self, board) -> list:
        """Determines valid moves for the Piece in the current gamestate

        :param board: reference to the Board object
        :return: List[Tuple[int, int]]
        """

        moves = []

        # Move 1 Diagonal and 1 Straight
        for x in range(self.x-2, self.x+3):
            for y in range(self.y-2, self.y+3):
                if abs(self.x - x) == 2 and abs(self.y - y) == 1 or abs(self.x - x) == 1 and abs(self.y - y) == 2:
                    if board.valid_move((x, y), self.color):
                        moves.append((x, y))
        return moves
