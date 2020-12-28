from .piece import Piece


class Bishop(Piece):
    """
    A class that represents a Bishop piece and controls all movement logic

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
        self.image = 4

    def __repr__(self):
        return "Bishop"

    def valid_moves(self, board) -> list:
        """Determines valid moves for the Piece in the current gamestate

        :param board: reference to the Board object
        :return: List[Tuple[int, int]]
        """

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
