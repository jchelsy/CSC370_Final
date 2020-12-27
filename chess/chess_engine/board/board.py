from ...data.settings import *
from ..pieces.king import King
from ..pieces.queen import Queen
from ..pieces.bishop import Bishop
from ..pieces.knight import Knight
from ..pieces.rook import Rook
from ..pieces.pawn import Pawn
from ..board.tile import Tile
from .. import AI


class Board:
    def __init__(self, player_color):
        self.tilemap = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_tiles()
        self.selected = None
        self.blackKingCoords = None
        self.whiteKingCoords = None
        self.turn = WHITE
        self.player = player_color
        if self.player == WHITE:
            self.bottomPlayerTurn = True
        else:
            self.bottomPlayerTurn = False
        self.gameover = None

        self.weights = {King: 900, Queen: 90, Rook: 50, Bishop: 30, Knight: 30, Pawn: 10}
        self.blackScore = 1290
        self.whiteScore = 1290

        self.past_moves = []

    def print(self):
        """Prints all values of the current board state

        :return: None
        """

        print("\n-----------------------------------------")
        print("blackKingCoords:  ", self.blackKingCoords)
        print("whiteKingCoords:  ", self.whiteKingCoords)
        print("Turn:             ", self.turn)
        print("CanMoveCount:     ", self.checkmate_stalemate())
        print("InCheck:          ", self.in_check(self.turn))
        print("Player:           ", self.player)
        print("BottomPlayerTurn: ", self.bottomPlayerTurn)
        print("Gameover:         ", self.gameover)
        print("blackScore:       ", self.blackScore)
        print("whiteScore:       ", self.whiteScore)
        print("-----------------------------------------")

    def initialize_pieces(self) -> None:
        """Places all pieces in the correct starting position

        :return: None
        """

        # Remove all pieces from the board
        for x in range(8):
            for y in range(8):
                self.tilemap[x][y].piece = None

        # Add Pawns to the board
        for i in range(8):
            self.tilemap[i][1].piece = Pawn(i, 1, BLACK)
            self.tilemap[i][6].piece = Pawn(i, 6, WHITE)

        # Add Rooks to the board
        self.tilemap[0][0].piece = Rook(0, 0, BLACK)
        self.tilemap[7][0].piece = Rook(7, 0, BLACK)
        self.tilemap[0][7].piece = Rook(0, 7, WHITE)
        self.tilemap[7][7].piece = Rook(7, 7, WHITE)

        # Add Knights to the board
        self.tilemap[1][0].piece = Knight(1, 0, BLACK)
        self.tilemap[6][0].piece = Knight(6, 0, BLACK)
        self.tilemap[1][7].piece = Knight(1, 7, WHITE)
        self.tilemap[6][7].piece = Knight(6, 7, WHITE)

        # Add Bishops to the board
        self.tilemap[2][0].piece = Bishop(2, 0, BLACK)
        self.tilemap[5][0].piece = Bishop(5, 0, BLACK)
        self.tilemap[2][7].piece = Bishop(2, 7, WHITE)
        self.tilemap[5][7].piece = Bishop(5, 7, WHITE)

        # Add Queens to the board
        self.tilemap[3][0].piece = Queen(3, 0, BLACK)
        self.tilemap[3][7].piece = Queen(3, 7, WHITE)

        # Add Kings to the board
        self.tilemap[4][0].piece = King(4, 0, BLACK)
        self.tilemap[4][7].piece = King(4, 7, WHITE)

        # Store coordinates of both Kings
        self.blackKingCoords = (4, 0)
        self.whiteKingCoords = (4, 7)

        # Reverse piece positions if the player chose to play as black
        if self.player == BLACK:
            self.blackKingCoords = (4, 7)
            self.whiteKingCoords = (4, 0)
            for x in range(8):
                for y in range(8):
                    if self.piece_at_coords((x, y)):
                        if self.tilemap[x][y].piece.color == BLACK:
                            self.tilemap[x][y].piece.color = WHITE
                        else:
                            self.tilemap[x][y].piece.color = BLACK

    def initialize_tiles(self) -> None:
        """Initializes the tile grid for the chess board

        :return: None
        """

        # On-Off Switch
        count = 0  # White-Black-White-Black... (even % 2 == WHITE, odd % 2 == BLACK)
        for x in range(8):
            for y in range(8):
                tile = Tile(None, x, y)
                if count % 2 == 0:
                    tile.color = TILE_COLOR_LIGHT
                    tile.fill(TILE_COLOR_LIGHT)
                else:
                    tile.color = TILE_COLOR_DARK
                    tile.fill(TILE_COLOR_DARK)
                self.tilemap[x][y] = tile
                count += 1
            count += 1

    def draw(self) -> None:
        """Draws all board components

        :return: None
        """

        # Draw tiles and pieces
        for row in self.tilemap:
            for tile in row:
                tile.draw()

        # Draw circles to indicate valid move locations
        if self.selected:
            moves = self.selected.piece.valid_moves(self)  # + self.can_castle(self.selected.piece.color)
            for move in moves:
                if not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y),
                                                move, self.selected.piece.color):
                    tup = to_coords(move[0], move[1])
                    x = tup[0] + int(TILE_SIZE / 2)
                    y = tup[1] + int(TILE_SIZE / 2)
                    tup2 = x, y
                    pygame.draw.circle(SCREEN, LARGE_TEXT_COLOR, tup2, 10)

    def select(self) -> None:
        """Selects the tile that contains the mouse pointer (if valid)

        :return: None
        """

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Get coordinates of the top-left corner of the selected Tile
        x = (pos[0] - BOARD_X) // TILE_SIZE
        y = (pos[1] - BOARD_Y) // TILE_SIZE
        coords = x, y

        # Player can only move their own pieces
        if self.player != self.turn:
            return

        # If mouse position is out of bounds, de-select current Tile (if applicable) and restore its color
        if not self.in_bounds(coords):
            if self.selected:
                self.selected.fill(self.selected.color)
                self.selected = None
            return

        # If a piece is already selected, move to the selected Tile
        if self.selected and coords in self.selected.piece.valid_moves(self) \
                and not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y), coords,
                                                 self.selected.piece.color):
            # self.move_piece((self.selected.x, self.selected.y), (x, y))
            self.make_move((self.selected.x, self.selected.y), (x, y))
            self.selected = None
            self.next_turn()
            return

        # Restore color and de-select the previously selected Tile (before selecting new Tile)
        if self.selected:
            self.selected.fill(self.selected.color)
            self.selected = None

        # Select Tile at coordinates (and remember Tile)
        if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
            self.tilemap[x][y].select()
            self.selected = self.tilemap[x][y]

    def copy(self):
        """Creates a deep copy of the current Board

        :return: reference to a new Board object
        """

        copy = Board(self.player)
        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)):
                    copy.tilemap[x][y].piece = self.tilemap[x][y].piece.copy()

        copy.selected = self.selected
        copy.blackKingCoords = self.blackKingCoords
        copy.whiteKingCoords = self.whiteKingCoords
        copy.turn = self.turn
        copy.bottomPlayerTurn = self.bottomPlayerTurn
        copy.player = self.player
        copy.gameover = self.gameover
        copy.weights = self.weights
        copy.blackScore = self.blackScore
        copy.whiteScore = self.whiteScore

        return copy

    @staticmethod
    def in_bounds(coords) -> bool:
        """Returns True if the given coordinates are within the bounds of the board

        :param coords: coordinates to be checked
        :return: bool
        """

        if coords[0] < 0 or coords[0] >= 8 or coords[1] < 0 or coords[1] >= 8:
            return False
        return True

    def piece_at_coords(self, coords) -> bool:
        """Returns True if the Tile at the given coordinates contains a piece

        :param coords: coordinates to be checked
        :return: bool
        """

        if not self.in_bounds(coords) or self.tilemap[coords[0]][coords[1]].piece is None:
            return False
        return True

    def enemy_at_coords(self, coords, color) -> bool:
        """Returns True if the color of the piece at the given coordinates is not the same as the specified color

        :param coords: coordinates to be checked
        :param color: current player color
        :return: bool
        """

        if self.piece_at_coords(coords):
            return self.tilemap[coords[0]][coords[1]].piece.color != color

    def valid_move(self, dest, color) -> bool:
        """Returns True if the move to the destination coordinates is within the board's bounds and not obstructed

        :param dest: coordinates of the Tile being moved to
        :param color: player color that is moving
        :return: bool
        """

        if self.in_bounds(dest) \
                and (not self.piece_at_coords(dest) or self.enemy_at_coords(dest, color)):
            return True
        return False

    def in_check(self, color) -> bool:
        """Returns True if the player of the specified color is in check

        :param color: player color to check
        :return: bool
        """

        if color == BLACK:
            king_coords = self.blackKingCoords
        else:
            king_coords = self.whiteKingCoords

        # Check if position of the King is a valid move for the opposite player (is in check)
        for x in range(8):
            for y in range(8):
                if self.enemy_at_coords((x, y), color):
                    for move in self.tilemap[x][y].piece.valid_moves(self):
                        if move[0] == king_coords[0] and move[1] == king_coords[1]:
                            return True  # in check
        return False  # not in check

    def in_check_after_move(self, source, dest, color) -> bool:
        """Returns True if the player of the specified color is in check after a move from source to dest coordinates

        :param source: coordinates of the Tile that is being moved from
        :param dest: coordinates of the Tile that is being moved to
        :param color: player color that is moving
        :return: bool
        """

        # Get shorthand variables for the source and destination tiles and pieces
        source_tile = self.tilemap[source[0]][source[1]]
        dest_tile = self.tilemap[dest[0]][dest[1]]
        source_piece = source_tile.piece
        dest_piece = dest_tile.piece

        # Preserve King coordinates (if applicable)
        king_coords = None
        if type(source_piece) is King:
            if color == BLACK:
                king_coords = self.blackKingCoords
            else:
                king_coords = self.whiteKingCoords

        # Move piece from the source Tile to the destination Tile
        dest_tile.piece = source_piece
        dest_tile.piece.move(dest_tile.x, dest_tile.y)
        source_tile.piece = None

        # Set King coordinates (if applicable)
        if type(source_piece) is King:
            if color == BLACK:
                self.blackKingCoords = (dest_tile.piece.x, dest_tile.piece.y)
            else:
                self.whiteKingCoords = (dest_tile.piece.x, dest_tile.piece.y)

        # Set player position
        self.bottomPlayerTurn = not self.bottomPlayerTurn

        # See if the current player is in check after moving
        if self.in_check(color):
            in_check = True
        else:
            in_check = False

        # Restore King coordinates (if applicable)
        if type(source_piece) is King:
            if color == BLACK:
                self.blackKingCoords = king_coords
            else:
                self.whiteKingCoords = king_coords

        # Restore player position
        self.bottomPlayerTurn = not self.bottomPlayerTurn

        # Move the piece back
        source_tile.piece = source_piece
        dest_tile.piece = dest_piece
        source_tile.piece.move(source_tile.x, source_tile.y)

        return in_check

    def make_move(self, source, dest):
        """Moves a piece from source to dest coordinates and makes necessary updates to game state

        :param source: coordinates of the Tile that the piece is moving from
        :param dest: coordinates of the Tile that the piece is moving to
        :return: None
        """

        # Get shorthand variables for the source and destination Tiles
        source_tile = self.tilemap[source[0]][source[1]]
        dest_tile = self.tilemap[dest[0]][dest[1]]

        # Store previous state to allow for unmaking the move
        previous_state = {"blackScore": self.blackScore,
                          "whiteScore": self.whiteScore,
                          "blackKingCoords": self.blackKingCoords,
                          "whiteKingCoords": self.whiteKingCoords,
                          "tile1": (source, source_tile.copy()),
                          "tile2": (dest, dest_tile.copy()),
                          "gameover": self.gameover}

        self.past_moves.append(previous_state)

        # Update scores
        if dest_tile.piece:  # If a piece is on the destination Tile (opponent to be captured)
            if self.turn == WHITE:
                self.blackScore -= self.weights[type(dest_tile.piece)]  # remove opponent piece weight
            else:
                self.whiteScore -= self.weights[type(dest_tile.piece)]  # remove opponent piece weight

        # Promote Pawn (if requirements are met)
        if type(source_tile.piece) is Pawn:
            # If Pawn reached the end of the board (top/bottom)
            if (self.bottomPlayerTurn and dest_tile.y == 0) \
                    or (not self.bottomPlayerTurn and dest_tile.y == 7):
                # Promote the Pawn to a Queen
                source_tile.piece = Queen(source_tile.piece.x, source_tile.piece.y, source_tile.piece.color)

        # Move piece from the source Tile to the destination Tile
        dest_tile.piece = source_tile.piece
        source_tile.piece.move(dest_tile.x, dest_tile.y)
        dest_tile.piece.firstMove = False

        # Update King coordinates (if applicable)
        if type(source_tile.piece) is King:
            if source_tile.piece.color == BLACK:
                self.blackKingCoords = dest_tile.x, dest_tile.y
            else:
                self.whiteKingCoords = dest_tile.x, dest_tile.y

        # Remove piece from the source Tile
        source_tile.piece = None
        source_tile.fill(source_tile.color)

        # Check win conditions
        self.checkmate_stalemate()
        self.insufficient_material()

    def unmake_move(self):
        """Undoes previous move and restores the game state

        :return: None
        """

        # Revert to the previous game state (using stored values)
        previous_state = self.past_moves.pop()
        self.blackScore = previous_state["blackScore"]
        self.whiteScore = previous_state["whiteScore"]
        self.blackKingCoords = previous_state["blackKingCoords"]
        self.whiteKingCoords = previous_state["whiteKingCoords"]
        x = previous_state["tile1"][0][0]
        y = previous_state["tile1"][0][1]
        self.tilemap[x][y] = previous_state["tile1"][1]
        x = previous_state["tile2"][0][0]
        y = previous_state["tile2"][0][1]
        self.tilemap[x][y] = previous_state["tile2"][1]
        self.gameover = previous_state["gameover"]

        self.next_turn()

    def next_turn(self) -> None:
        """Swaps current board turn to the other player

        :return: None
        """

        # Swap turn color
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

        # Swap bottom/top player
        self.bottomPlayerTurn = not self.bottomPlayerTurn

    def checkmate_stalemate(self):  # -> bool
        """Checks for checkmate or stalemate status of the board

        :return: None
        """

        legal_moves = 0
        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
                    moves = self.tilemap[x][y].piece.valid_moves(self)  # + self.can_castle(self.tilemap[x][y].piece.color)
                    for move in moves:
                        if not self.in_check_after_move((x, y), move, self.tilemap[x][y].piece.color):
                            legal_moves += 1

        # Get current opponent color
        if self.turn == WHITE:
            opponent = BLACK
        else:
            opponent = WHITE

        # Check if there is a stalemate or checkmate
        if legal_moves == 0 and not self.in_check(self.turn):
            self.gameover = ("Stalemate", None)
        elif legal_moves == 0:
            self.gameover = ("Checkmate", opponent)

    def get_moves(self):
        """Returns a list of the available moves for the current player

        :return: list
        """

        moves = []

        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
                    for move in self.tilemap[x][y].piece.valid_moves(self):
                        if not self.in_check_after_move((x, y), move, self.turn):
                            if self.enemy_at_coords(move, self.turn):
                                moves.insert(0, ((x, y), move))
                            else:
                                moves.append(((x, y), move))
        return list(set(moves))  # randomizing effect

    def get_moves_sorted(self):
        """Returns a list of the available moves sorted in descending order by value for the current player

        :return: list
        """

        b = self.copy()
        moves = {}

        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
                    for move in self.tilemap[x][y].piece.valid_moves(self):
                        if not self.in_check_after_move((x, y), move, self.turn) and ((x, y), move) not in moves:
                            b.make_move((x, y), move)
                            moves[((x, y), move)] = AI.evaluate(b, self.turn)
                            b.unmake_move()

        return [move for move, score in sorted(moves.items(), key=lambda v: v[1], reverse=True)]

    def insufficient_material(self):
        piece_counts = {"wminor": 0, "bminor": 0, "king": 0, "wknight": 0, "bknight": 0}
        for x in range(8):
            for y in range(8):
                piece = self.tilemap[x][y].piece
                if piece:
                    if type(piece) is Queen:
                        return  # If a Queen is on the board, insufficient material is impossible
                    if type(piece) is King:
                        piece_counts["king"] += 1
                    elif type(piece) is Knight and piece.color == WHITE:
                        piece_counts["wknight"] += 1
                    elif type(piece) is Knight and piece.color == BLACK:
                        piece_counts["bknight"] += 1
                    else:
                        if piece.color == WHITE:
                            piece_counts["wminor"] += 1
                        elif piece.color == BLACK:
                            piece_counts["bminor"] += 1

        # King vs King
        if piece_counts["wminor"] == piece_counts["bminor"] == piece_counts["wknight"] == piece_counts["bknight"] == 0 \
                and piece_counts["king"] == 2:
            self.gameover = ("Insufficient Material", None)

        # King vs King + minor piece
        elif ((piece_counts["wminor"] == 1 and piece_counts["bminor"] == 0) or (piece_counts["bminor"] == 1
                                                                                and piece_counts["wminor"] == 0)) \
                and piece_counts["king"] == 2 and piece_counts["bknight"] == piece_counts["wknight"] == 0:
            self.gameover = ("Insufficient Material", None)

        # King vs King + 2 Knights
        elif (piece_counts["wknight"] == 2 and piece_counts["king"] == 2
              and piece_counts["wminor"] == piece_counts["bminor"] == 0) \
                or (piece_counts["bknight"] == 2 and piece_counts["king"] == 2
                    and piece_counts["wminor"] == piece_counts["bminor"] == 0):
            self.gameover = ("Insufficient Material", None)
        elif (piece_counts["wminor"] == 1 and piece_counts["king"] == 2 and piece_counts["bminor"] == 0) \
                or (piece_counts["bminor"] == 1 and piece_counts["king"] == 2 and piece_counts["wminor"] == 0):
            self.gameover = ("Insufficient Material", None)

# # from chess.chess_engine.pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn
# # from chess.chess_engine.board.tile import Tile
# # from chess.data.settings import *
# #
# # from chess.chess_engine import AI
#
# from ..pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn
# # from ..board import Tile
# from .tile import Tile
# from ...data.settings import *
#
# from .. import AI
#
#
# class Board:
#
#     def __init__(self, player_color):
#         self.tilemap = [[None for _ in range(8)] for _ in range(8)]
#         self.initialize_tiles()
#         self.selected = None
#         self.blackKingCoords = None
#         self.whiteKingCoords = None
#         self.turn = WHITE
#         self.player = player_color
#         if self.player == WHITE:
#             self.bottomPlayerTurn = True
#         else:
#             self.bottomPlayerTurn = False
#         self.gameover = None
#
#         self.weights = {King: 900, Queen: 90, Rook: 50, Bishop: 30, Knight: 30, Pawn: 10}
#         self.blackScore = 1290
#         self.whiteScore = 1290
#
#         self.past_moves = []
#
#     def print(self):
#         print("\n-----------------------------------------")
#         print("blackKingCoords:  ", self.blackKingCoords)
#         print("whiteKingCoords:  ", self.whiteKingCoords)
#         print("Turn:             ", self.turn)
#         print("CanMoveCount:     ", self.checkmate_stalemate())
#         print("InCheck:          ", self.in_check(self.turn))
#         print("Player:           ", self.player)
#         print("BottomPlayerTurn: ", self.bottomPlayerTurn)
#         print("Gameover:         ", self.gameover)
#         print("blackScore:       ", self.blackScore)
#         print("whiteScore:       ", self.whiteScore)
#         print("-----------------------------------------")
#
#     def initialize_pieces(self) -> None:
#         """
#         Places all pieces in the correct starting position
#         :return: None
#         """
#
#         # Remove all pieces from board
#         for x in range(8):
#             for y in range(8):
#                 self.tilemap[x][y].piece = None
#
#         # Pawns
#         for i in range(8):
#             self.tilemap[i][1].piece = Pawn(i, 1, BLACK)
#             self.tilemap[i][6].piece = Pawn(i, 6, WHITE)
#
#         # Rooks
#         self.tilemap[0][0].piece = Rook(0, 0, BLACK)
#         self.tilemap[7][0].piece = Rook(7, 0, BLACK)
#         self.tilemap[0][7].piece = Rook(0, 7, WHITE)
#         self.tilemap[7][7].piece = Rook(7, 7, WHITE)
#
#         # Knights
#         self.tilemap[1][0].piece = Knight(1, 0, BLACK)
#         self.tilemap[6][0].piece = Knight(6, 0, BLACK)
#         self.tilemap[1][7].piece = Knight(1, 7, WHITE)
#         self.tilemap[6][7].piece = Knight(6, 7, WHITE)
#
#         # Bishops
#         self.tilemap[2][0].piece = Bishop(2, 0, BLACK)
#         self.tilemap[5][0].piece = Bishop(5, 0, BLACK)
#         self.tilemap[2][7].piece = Bishop(2, 7, WHITE)
#         self.tilemap[5][7].piece = Bishop(5, 7, WHITE)
#
#         # Queens
#         self.tilemap[3][0].piece = Queen(3, 0, BLACK)
#         self.tilemap[3][7].piece = Queen(3, 7, WHITE)
#
#         # Kings
#         self.tilemap[4][0].piece = King(4, 0, BLACK)
#         self.tilemap[4][7].piece = King(4, 7, WHITE)
#
#         # Store coords of both kings
#         self.blackKingCoords = (4, 0)
#         self.whiteKingCoords = (4, 7)
#
#         # Reverse piece positions if player is playing black
#         if self.player == BLACK:
#             self.blackKingCoords = (4, 7)
#             self.whiteKingCoords = (4, 0)
#             for x in range(8):
#                 for y in range(8):
#                     if self.piece_at_coords((x, y)):
#                         if self.tilemap[x][y].piece.color == BLACK:
#                             self.tilemap[x][y].piece.color = WHITE
#                         else:
#                             self.tilemap[x][y].piece.color = BLACK
#
#     def initialize_tiles(self) -> None:
#         """
#         Initializes the tile grid for the chess board
#         :return: None
#         """
#         cnt = 0
#         for x in range(8):
#             for y in range(8):
#                 tile = Tile(None, x, y)
#                 if cnt % 2 == 0:
#                     tile.color = TILE_COLOR_LIGHT
#                     tile.fill(TILE_COLOR_LIGHT)
#                 else:
#                     tile.color = TILE_COLOR_DARK
#                     tile.fill(TILE_COLOR_DARK)
#                 self.tilemap[x][y] = tile
#                 cnt += 1
#             cnt += 1
#
#     def draw(self) -> None:
#         """
#         Draws all components of the board
#         :return: None
#         """
#
#         # Draw tiles and pieces
#         for row in self.tilemap:
#             for tile in row:
#                 tile.draw()
#
#         # Draw circles to indicate valid move locations
#         if self.selected:
#             moves = self.selected.piece.valid_moves(self)  # + self.can_castle(self.selected.piece.color)
#             for move in moves:
#                 if not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y),
#                                                 move, self.selected.piece.color):
#                     tup = to_coords(move[0], move[1])
#                     x = tup[0] + int(TILE_SIZE / 2)
#                     y = tup[1] + int(TILE_SIZE / 2)
#                     tup2 = x, y
#                     pygame.draw.circle(SCREEN, LARGE_TEXT_COLOR, tup2, 10)
#
#     def select(self) -> None:
#         """
#         Selects tile that contains the mouse pointer if tile is valid
#         :return: None
#         """
#
#         # Get position of mouse
#         pos = pygame.mouse.get_pos()
#
#         # Get coordinates of top left corner of selected tile
#         x = (pos[0] - BOARD_X) // TILE_SIZE
#         y = (pos[1] - BOARD_Y) // TILE_SIZE
#         coords = x, y
#
#         # Player can only move their own pieces
#         if self.player != self.turn:
#             return
#
#         # If mouse position is out of bounds, de-select current tile (if applicable) and restore its color
#         if not self.in_bounds(coords):
#             if self.selected:
#                 self.selected.fill(self.selected.color)
#                 self.selected = None
#             return
#
#         # If a piece is already selected, make move to selected tile
#         if self.selected and coords in self.selected.piece.valid_moves(self) \
#                 and not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y), coords,
#                                                  self.selected.piece.color):
#             #self.move_piece((self.selected.x, self.selected.y), (x, y))
#             self.make_move((self.selected.x, self.selected.y), (x, y))
#             self.selected = None
#             self.next_turn()
#             return
#
#         # Restore color and de-select previously selected tile before selecting new tile
#         if self.selected:
#             self.selected.fill(self.selected.color)
#             self.selected = None
#
#         # Select tile at coordinates and remember tile
#         if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
#             self.tilemap[x][y].select()
#             self.selected = self.tilemap[x][y]
#
#     def copy(self):
#         """
#         Creates a deep copy of the current board
#         :return: reference to a new Board object
#         """
#         copy = Board(self.player)
#         for x in range(8):
#             for y in range(8):
#                 if self.piece_at_coords((x, y)):
#                     copy.tilemap[x][y].piece = self.tilemap[x][y].piece.copy()
#         copy.selected = self.selected
#         copy.blackKingCoords = self.blackKingCoords
#         copy.whiteKingCoords = self.whiteKingCoords
#         copy.turn = self.turn
#         copy.bottomPlayerTurn = self.bottomPlayerTurn
#         copy.player = self.player
#         copy.gameover = self.gameover
#         copy.weights = self.weights
#         copy.blackScore = self.blackScore
#         copy.whiteScore = self.whiteScore
#         return copy
#
#     @staticmethod
#     def in_bounds(coords) -> bool:
#         """
#         Returns True if given coordinates are within the bounds of the board
#         :param coords: coords to be checked (tuple)
#         :return: bool
#         """
#         if coords[0] < 0 or coords[0] >= 8 or coords[1] < 0 or coords[1] >= 8:
#             return False
#         return True
#
#     def piece_at_coords(self, coords) -> bool:
#         """
#         Returns True if tile at coordinates contains a piece of any kind
#         :param coords: coords to be checked (tuple)
#         :return: bool
#         """
#         if not self.in_bounds(coords) or self.tilemap[coords[0]][coords[1]].piece is None:
#             return False
#         return True
#
#     def enemy_at_coords(self, coords, color) -> bool:
#         """
#         Returns True if color of the piece at coords is not same as specified color
#         :param coords: coords to be checked (tuple)
#         :param color: color of current player (tuple)
#         :return: bool
#         """
#         if self.piece_at_coords(coords):
#             return self.tilemap[coords[0]][coords[1]].piece.color != color
#
#     def valid_move(self, dest, color) -> bool:
#         """
#         Returns True if move to dest coords is within board's bounds and not obstructed
#         :param dest: coordinates of tile that is being moved to (tuple)
#         :param color: color of player that is moving (tuple)
#         :return: bool
#         """
#         if self.in_bounds(dest) \
#                 and (not self.piece_at_coords(dest) or self.enemy_at_coords(dest, color)):
#             return True
#         return False
#
#     def in_check(self, color) -> bool:
#         """
#         Returns True if player of specified color is in check
#         :param color: color of player to check (tuple)
#         :return: bool
#         """
#         if color == BLACK:
#             king_coords = self.blackKingCoords
#         else:
#             king_coords = self.whiteKingCoords
#
#         # Check if position of King is in any of the valid moves for opposite player
#         for x in range(8):
#             for y in range(8):
#                 if self.enemy_at_coords((x, y), color):
#                     for move in self.tilemap[x][y].piece.valid_moves(self):
#                         if move[0] == king_coords[0] and move[1] == king_coords[1]:
#                             return True
#
#         return False
#
#     def in_check_after_move(self, source, dest, color) -> bool:
#         """
#         Returns True if player of specified color is in check after a move from source to dest
#         :param source: coordinates of tile that is being moved from (tuple)
#         :param dest: coordinates of tile that is being moved to (tuple)
#         :param color: color of player that is moving (tuple)
#         :return: bool
#         """
#
#         # Get shorthand for source and destination tiles and pieces
#         source_tile = self.tilemap[source[0]][source[1]]
#         dest_tile = self.tilemap[dest[0]][dest[1]]
#         source_piece = source_tile.piece
#         dest_piece = dest_tile.piece
#
#         # Preserve king coords
#         king_coords = None
#         if type(source_piece) is King:
#             if color == BLACK:
#                 king_coords = self.blackKingCoords
#             else:
#                 king_coords = self.whiteKingCoords
#
#         # Move piece from source tile to dest tile
#         dest_tile.piece = source_piece
#         dest_tile.piece.move(dest_tile.x, dest_tile.y)
#         source_tile.piece = None
#
#         # Set king coords
#         if type(source_piece) is King:
#             if color == BLACK:
#                 self.blackKingCoords = (dest_tile.piece.x, dest_tile.piece.y)
#             else:
#                 self.whiteKingCoords = (dest_tile.piece.x, dest_tile.piece.y)
#
#         # Set player position
#         self.bottomPlayerTurn = not self.bottomPlayerTurn
#
#         # See if in check state after move
#         if self.in_check(color):
#             in_check = True
#         else:
#             in_check = False
#
#         # Restore king coords
#         if type(source_piece) is King:
#             if color == BLACK:
#                 self.blackKingCoords = king_coords
#             else:
#                 self.whiteKingCoords = king_coords
#
#         # Restore player position
#         self.bottomPlayerTurn = not self.bottomPlayerTurn
#
#         # Move piece back
#         source_tile.piece = source_piece
#         dest_tile.piece = dest_piece
#         source_tile.piece.move(source_tile.x, source_tile.y)
#
#         return in_check
#
#     def make_move(self, source, dest):
#         """
#         Moves piece from source coords to dest coords and makes necessary updates to game state
#         :param source: coordinates of tile that piece is moving from (tuple)
#         :param dest: coordinates of tile that piece is moving to (tuple)
#         :return: None
#         """
#
#         # Get shorthand for source and destination tiles
#         source_tile = self.tilemap[source[0]][source[1]]
#         dest_tile = self.tilemap[dest[0]][dest[1]]
#
#         # Store previous state to allow for unmaking move
#         previous_state = {"blackScore": self.blackScore,
#                           "whiteScore": self.whiteScore,
#                           "blackKingCoords": self.blackKingCoords,
#                           "whiteKingCoords": self.whiteKingCoords,
#                           "tile1": (source, source_tile.copy()),
#                           "tile2": (dest, dest_tile.copy()),
#                           "gameover": self.gameover
#                           }
#         self.past_moves.append(previous_state)
#
#         # Update scores
#         if dest_tile.piece:
#             if self.turn == WHITE:
#                 self.blackScore -= self.weights[type(dest_tile.piece)]
#             else:
#                 self.whiteScore -= self.weights[type(dest_tile.piece)]
#
#         # Promote piece if it meets requirements
#         if type(source_tile.piece) is Pawn:
#             if (self.bottomPlayerTurn and dest_tile.y == 0) or (not self.bottomPlayerTurn and dest_tile.y == 7):
#                 source_tile.piece = Queen(source_tile.piece.x, source_tile.piece.y, source_tile.piece.color)
#
#         # Move piece from source tile to dest tile
#         dest_tile.piece = source_tile.piece
#         source_tile.piece.move(dest_tile.x, dest_tile.y)
#         dest_tile.piece.firstMove = False
#
#         # Update king coords if necessary
#         if type(source_tile.piece) is King:
#             if source_tile.piece.color == BLACK:
#                 self.blackKingCoords = dest_tile.x, dest_tile.y
#             else:
#                 self.whiteKingCoords = dest_tile.x, dest_tile.y
#
#         # Remove piece from source tile
#         source_tile.piece = None
#         source_tile.fill(source_tile.color)
#
#         # Check win conditions
#         self.checkmate_stalemate()
#         self.insufficient_material()
#
#     def unmake_move(self):
#         """
#         Undoes previous move; restores game state
#         :return: None
#         """
#         # Revert to previous game state using stored values
#         previous_state = self.past_moves.pop()
#         self.blackScore = previous_state["blackScore"]
#         self.whiteScore = previous_state["whiteScore"]
#         self.blackKingCoords = previous_state["blackKingCoords"]
#         self.whiteKingCoords = previous_state["whiteKingCoords"]
#         x = previous_state["tile1"][0][0]
#         y = previous_state["tile1"][0][1]
#         self.tilemap[x][y] = previous_state["tile1"][1]
#         x = previous_state["tile2"][0][0]
#         y = previous_state["tile2"][0][1]
#         self.tilemap[x][y] = previous_state["tile2"][1]
#         self.gameover = previous_state["gameover"]
#
#         self.next_turn()
#
#     def next_turn(self) -> None:
#         """
#         Switches turn of board to the other player
#         :return: None
#         """
#         if self.turn == WHITE:
#             self.turn = BLACK
#         else:
#             self.turn = WHITE
#
#         self.bottomPlayerTurn = not self.bottomPlayerTurn
#
#     def checkmate_stalemate(self) -> bool:
#         """
#         Checks for checkmate or stalemate status of board
#         :return: None
#         """
#
#         legal_moves = 0
#         for x in range(8):
#             for y in range(8):
#                 if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
#                     moves = self.tilemap[x][y].piece.valid_moves(self)  # + self.can_castle(self.tilemap[x][y].piece.color)
#                     for move in moves:
#                         if not self.in_check_after_move((x, y), move, self.tilemap[x][y].piece.color):
#                             legal_moves += 1
#
#         if self.turn == WHITE:
#             opponent = BLACK
#         else:
#             opponent = WHITE
#
#         if legal_moves == 0 and not self.in_check(self.turn):
#             self.gameover = ("Stalemate", None)
#         elif legal_moves == 0:
#             self.gameover = ("Checkmate", opponent)
#
#     def get_moves(self):
#         """
#         Returns a list of the available moves for the current player
#         :return: list
#         """
#         moves = []
#         for x in range(8):
#             for y in range(8):
#                 if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
#                     for move in self.tilemap[x][y].piece.valid_moves(self):
#                         if not self.in_check_after_move((x, y), move, self.turn):
#                             if self.enemy_at_coords(move, self.turn):
#                                 moves.insert(0, ((x, y), move))
#                             else:
#                                 moves.append(((x, y), move))
#         return list(set(moves))          # converting to set then back to list has randomizing effect on moves
#
#     def get_moves_sorted(self):
#         """
#         Returns a list of the available moves sorted in descending order by value for the current player
#         :return: list
#         """
#         b = self.copy()
#         moves = {}
#         for x in range(8):
#             for y in range(8):
#                 if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
#                     for move in self.tilemap[x][y].piece.valid_moves(self):
#                         if not self.in_check_after_move((x, y), move, self.turn) and ((x, y), move) not in moves:
#                             b.make_move((x, y), move)
#                             moves[((x, y), move)] = AI.evaluate(b, self.turn)
#                             b.unmake_move()
#         return [move for move, score in sorted(moves.items(), key=lambda v: v[1], reverse=True)]
#
#     def insufficient_material(self):
#         # Insufficient material
#         piece_counts = {"wminor": 0, "bminor": 0, "king": 0, "wknight": 0, "bknight": 0}
#         for x in range(8):
#             for y in range(8):
#                 piece = self.tilemap[x][y].piece
#                 if piece:
#                     # if a Queen is present, insufficient material is impossible
#                     if type(piece) is Queen:
#                         return
#                     if type(piece) is King:
#                         piece_counts["king"] += 1
#                     elif type(piece) is Knight and piece.color == WHITE:
#                         piece_counts["wknight"] += 1
#                     elif type(piece) is Knight and piece.color == BLACK:
#                         piece_counts["bknight"] += 1
#                     else:
#                         if piece.color == WHITE:
#                             piece_counts["wminor"] += 1
#                         elif piece.color == BLACK:
#                             piece_counts["bminor"] += 1
#
#         # King vs King
#         if piece_counts["wminor"] == piece_counts["bminor"] == piece_counts["wknight"] == piece_counts["bknight"] == 0 and piece_counts["king"] == 2:
#             self.gameover = ("Insufficient Material", None)
#         # King + minor piece vs King
#         elif ((piece_counts["wminor"] == 1 and piece_counts["bminor"] == 0) or (piece_counts["bminor"] == 1 and piece_counts["wminor"] == 0)) and piece_counts["king"] == 2 and piece_counts["bknight"] == piece_counts["wknight"] == 0:
#             self.gameover = ("Insufficient Material", None)
#         # King + two Knights vs King
#         elif (piece_counts["wknight"] == 2 and piece_counts["king"] == 2 and piece_counts["wminor"] == piece_counts["bminor"] == 0) or (piece_counts["bknight"] == 2 and piece_counts["king"] == 2 and piece_counts["wminor"] == piece_counts["bminor"] == 0):
#             self.gameover = ("Insufficient Material", None)
#         elif (piece_counts["wminor"] == 1 and piece_counts["king"] == 2 and piece_counts["bminor"] == 0) or (piece_counts["bminor"] == 1 and piece_counts["king"] == 2 and piece_counts["wminor"] == 0):
#             self.gameover = ("Insufficient Material", None)
#
#
# # class Board:
# #     def __init__(self, player_color):
# #         self.tilemap = [[None for _ in range(8)] for _ in range(8)]
# #         self.initialize_tiles()
# #         self.selected = None
# #         self.blackKingCoords = None
# #         self.whiteKingCoords = None
# #         self.turn = WHITE
# #         self.player = player_color
# #         if self.player == WHITE:
# #             self.bottomPlayerTurn = True
# #         else:
# #             self.bottomPlayerTurn = False
# #         self.gameover = None
# #
# #         self.weights = {King: 900, Queen: 90, Rook: 50, Bishop: 30, Knight: 30, Pawn: 10}
# #         self.blackScore = 1290
# #         self.whiteScore = 1290
# #
# #         self.past_moves = []
# #
# #     def print(self) -> None:
# #         """Prints all values of the current board state
# #
# #         :return: None
# #         """
# #
# #         print("\n-----------------------------------------")
# #         print("blackKingCoords:  ", self.blackKingCoords)
# #         print("whiteKingCoords:  ", self.whiteKingCoords)
# #         print("Turn:             ", self.turn)
# #         print("CanMoveCount:     ", self.checkmate_stalemate())
# #         print("InCheck:          ", self.in_check(self.turn))
# #         print("Player:           ", self.player)
# #         print("BottomPlayerTurn: ", self.bottomPlayerTurn)
# #         print("Gameover:         ", self.gameover)
# #         print("blackScore:       ", self.blackScore)
# #         print("whiteScore:       ", self.whiteScore)
# #         print("-----------------------------------------")
# #
# #     def initialize_pieces(self) -> None:
# #         """Places all pieces in the correct starting position
# #
# #         :return: None
# #         """
# #
# #         # Remove all pieces from the board
# #         for x in range(8):
# #             for y in range(8):
# #                 self.tilemap[x][y].piece = None
# #
# #         # Add Pawns to the board
# #         for i in range(8):
# #             self.tilemap[i][1].piece = Pawn(i, 1, BLACK)
# #             self.tilemap[i][6].piece = Pawn(i, 6, WHITE)
# #
# #         # Add Rooks to the board
# #         self.tilemap[0][0].piece = Rook(0, 0, BLACK)
# #         self.tilemap[7][0].piece = Rook(7, 0, BLACK)
# #         self.tilemap[0][7].piece = Rook(0, 7, WHITE)
# #         self.tilemap[7][7].piece = Rook(7, 7, WHITE)
# #
# #         # Add Knights to the board
# #         self.tilemap[1][0].piece = Knight(1, 0, BLACK)
# #         self.tilemap[6][0].piece = Knight(6, 0, BLACK)
# #         self.tilemap[1][7].piece = Knight(1, 7, WHITE)
# #         self.tilemap[6][7].piece = Knight(6, 7, WHITE)
# #
# #         # Add Bishops to the board
# #         self.tilemap[2][0].piece = Bishop(2, 0, BLACK)
# #         self.tilemap[5][0].piece = Bishop(5, 0, BLACK)
# #         self.tilemap[2][7].piece = Bishop(2, 7, WHITE)
# #         self.tilemap[5][7].piece = Bishop(5, 7, WHITE)
# #
# #         # Add Queens to the board
# #         self.tilemap[3][0].piece = Queen(3, 0, BLACK)
# #         self.tilemap[3][7].piece = Queen(3, 7, WHITE)
# #
# #         # Add Kings to the board
# #         self.tilemap[4][0].piece = King(4, 0, BLACK)
# #         self.tilemap[4][7].piece = King(4, 7, WHITE)
# #
# #         # Store coordinates of both Kings
# #         self.blackKingCoords = (4, 0)
# #         self.blackKingCoords = (4, 7)
# #
# #         # Reverse piece positions if player chose to play as black
# #         if self.player == BLACK:
# #             self.blackKingCoords = (4, 7)
# #             self.whiteKingCoords = (4, 0)
# #             for x in range(8):
# #                 for y in range(8):
# #                     if self.piece_at_coords((x, y)):
# #                         if self.tilemap[x][y].piece.color == BLACK:
# #                             self.tilemap[x][y].piece.color = WHITE
# #                         else:
# #                             self.tilemap[x][y].piece.color = BLACK
# #
# #     def initialize_tiles(self) -> None:
# #         """Initializes the tile grid for the chess board
# #
# #         :return: None
# #         """
# #
# #         # On-Off switch
# #         count = 0  # white-black-white-black... (even % 2 == white, odd % 2 == black)
# #         for x in range(8):
# #             for y in range(8):
# #                 tile = Tile(None, x, y)
# #                 if count % 2 == 0:
# #                     tile.color = TILE_COLOR_LIGHT
# #                     tile.fill(TILE_COLOR_LIGHT)
# #                 else:
# #                     tile.color = TILE_COLOR_DARK
# #                     tile.fill(TILE_COLOR_DARK)
# #                 self.tilemap[x][y] = tile
# #                 count += 1
# #             count += 1
# #
# #     def draw(self) -> None:
# #         """Draws all board components
# #
# #         :return: None
# #         """
# #
# #         # Draw tiles and pieces
# #         for row in self.tilemap:
# #             for tile in row:
# #                 tile.draw()
# #
# #         # Draw circles to indicate valid move locations
# #         if self.selected:
# #             moves = self.selected.piece.valid_moves(self)
# #             for move in moves:
# #                 if not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y),
# #                                                 move, self.selected.piece.color):
# #                     coords = to_coords(move[0], move[1])
# #                     x = coords[0] + int(TILE_SIZE / 2)
# #                     y = coords[1] + int(TILE_SIZE / 2)
# #                     px_coords = x, y
# #                     pygame.draw.circle(SCREEN, LARGE_TEXT_COLOR, px_coords, 10)
# #
# #     def select(self) -> None:
# #         """Selects the tile that contains the mouse pointer (if valid)
# #
# #         :return: None
# #         """
# #
# #         # Get mouse position
# #         pos = pygame.mouse.get_pos()
# #
# #         # Get coordinates of the top-left corner of the selected Tile
# #         x = (pos[0] - BOARD_X) // TILE_SIZE
# #         y = (pos[1] - BOARD_Y) // TILE_SIZE
# #         coords = x, y
# #
# #         # Player can only move their own pieces
# #         if self.player != self.turn:
# #             return
# #
# #         # If mouse position is out of bounds, de-select current tile (if applicable) and restore its color
# #         if not self.in_bounds(coords):
# #             if self.selected:
# #                 self.selected.fill(self.selected.color)
# #                 self.selected = None
# #             return
# #
# #         # If a piece is already selected, move to the selected Tile
# #         if self.selected and coords in self.selected.piece.valid_moves(self) \
# #                 and not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y), coords,
# #                                                  self.selected.piece.color):
# #             self.make_move((self.selected.x, self.selected.y), (x, y))
# #             self.selected = None
# #             self.next_turn()
# #             return
# #
# #         # Restore color and de-select previously selected tile (before selecting new tile)
# #         if self.selected:
# #             self.selected.fill(self.selected.color)
# #             self.selected = None
# #
# #         # Select Tile at coordinates (and remember Tile)
# #         if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
# #             self.tilemap[x][y].select()
# #             self.selected = self.tilemap[x][y]
# #
# #     def copy(self):
# #         """Creates a deep copy of the current Board
# #
# #         :return: reference to a new Board object
# #         """
# #
# #         copy = Board(self.player)
# #         for x in range(8):
# #             for y in range(8):
# #                 if self.piece_at_coords((x, y)):
# #                     copy.tilemap[x][y].piece = self.tilemap[x][y].piece.copy()
# #
# #         copy.selected = self.selected
# #         copy.blackKingCoords = self.blackKingCoords
# #         copy.whiteKingCoords = self.whiteKingCoords
# #         copy.turn = self.turn
# #         copy.bottomPlayerTurn = self.bottomPlayerTurn
# #         copy.player = self.player
# #         copy.gameover = self.gameover
# #         copy.weights = self.weights
# #         copy.blackScore = self.blackScore
# #         copy.whiteScore = self.whiteScore
# #
# #         return copy
# #
# #     @staticmethod
# #     def in_bounds(coords) -> bool:
# #         """Returns True if given coordinates are within the bounds of the board
# #
# #         :param coords: coordinates to be checked
# #         :type coords: tuple
# #         :return: bool
# #         """
# #
# #         if coords[0] < 0 or coords[0] >= 8 or coords[1] < 0 or coords[1] >= 8:
# #             return False
# #         return True
# #
# #     def piece_at_coords(self, coords) -> bool:
# #         """Returns True if Tile at coordinates contains a piece
# #
# #         :param coords: coordinates to be checked
# #         :type coords: tuple
# #         :return: bool
# #         """
# #
# #         if not self.in_bounds(coords) or self.tilemap[coords[0]][coords[1]].piece is None:
# #             return False
# #         return True
# #
# #     def enemy_at_coords(self, coords, color) -> bool:
# #         """Returns True if the color of the piece at coords is not the same as the specified color
# #
# #         :param coords: coordinates to be checked
# #         :type coords: tuple
# #         :param color: current player color
# #         :type color: tuple
# #         :return: bool
# #         """
# #
# #         if self.piece_at_coords(coords):
# #             return self.tilemap[coords[0]][coords[1]].piece.color != color
# #
# #     def valid_move(self, dest, color) -> bool:
# #         """Returns True if move to dest coords is within the board's bounds and not obstructed
# #
# #         :param dest: coordinates of the Tile being moved to
# #         :type dest: tuple
# #         :param color: player color that is moving
# #         :type color: tuple
# #         :return: bool
# #         """
# #
# #         if self.in_bounds(dest) \
# #                 and (not self.piece_at_coords(dest) or self.enemy_at_coords(dest, color)):
# #             return True
# #         return False
# #
# #     def in_check(self, color) -> bool:
# #         """Returns True if player of specified color is in check
# #
# #         :param color: player color to check
# #         :type color: tuple
# #         :return: bool
# #         """
# #
# #         if color == BLACK:
# #             king_coords = self.blackKingCoords
# #         else:
# #             king_coords = self.whiteKingCoords
# #
# #         # Check if position of the King is a valid move for the opposite player (being in check)
# #         for x in range(8):
# #             for y in range(8):
# #                 if self.enemy_at_coords((x, y), color):
# #                     for move in self.tilemap[x][y].piece.valid_moves(self):
# #                         if move[0] == king_coords[0] and move[1] == king_coords[1]:
# #                             return True  # in check
# #         return False  # not in check
# #
# #     def in_check_after_move(self, source, dest, color) -> bool:
# #         """Returns True if player of specified color is in check after a move from source to dest coords
# #
# #         :param source: coordinates of Tile that is being moved from
# #         :type source: tuple
# #         :param dest: coordinates of Tile that is being moved to
# #         :type source: tuple
# #         :param color: player color that is moving
# #         :type color: tuple
# #         :return: bool
# #         """
# #
# #         # Get shorthand variables for the source and destination tiles and pieces
# #         source_tile = self.tilemap[source[0]][source[1]]
# #         dest_tile = self.tilemap[dest[0]][dest[1]]
# #         source_piece = source_tile.piece
# #         dest_piece = dest_tile.piece
# #
# #         # Preserve King coordinates (if applicable)
# #         king_coords = None
# #         if type(source_piece) is King:
# #             if color == BLACK:
# #                 king_coords = self.blackKingCoords
# #             else:
# #                 king_coords = self.whiteKingCoords
# #
# #         # Move piece from the source Tile to the destination Tile
# #         dest_tile.piece = source_piece
# #         dest_tile.piece.move(dest_tile.x, dest_tile.y)
# #         source_tile.piece = None
# #
# #         # Set King coordinates (if applicable)
# #         if type(source_piece) is King:
# #             if color == BLACK:
# #                 self.blackKingCoords = (dest_tile.piece.x, dest_tile.piece.y)
# #             else:
# #                 self.whiteKingCoords = (dest_tile.piece.x, dest_tile.piece.y)
# #
# #         # Set player position
# #         self.bottomPlayerTurn = not self.bottomPlayerTurn
# #
# #         # See if the current player is in check after moving
# #         if self.in_check(color):
# #             in_check = True
# #         else:
# #             in_check = False
# #
# #         # Restore King coordinates (if applicable)
# #         if type(source_piece) is King:
# #             if color == BLACK:
# #                 self.blackKingCoords = king_coords
# #             else:
# #                 self.whiteKingCoords = king_coords
# #
# #         # Restore player position
# #         self.bottomPlayerTurn = not self.bottomPlayerTurn
# #
# #         # Move the piece back
# #         source_tile.piece = source_piece
# #         dest_tile.piece = dest_piece
# #         source_tile.piece.move(source_tile.x, source_tile.y)
# #
# #         return in_check
# #
# #     def make_move(self, source, dest) -> None:
# #         """Moves piece from source to dest coords and makes necessary updates to game state
# #
# #         :param source: coordinates of Tile that piece is moving from
# #         :type source: tuple
# #         :param dest: coordinates of Tile that piece is moving to
# #         :type dest: tuple
# #         :return: None
# #         """
# #
# #         # Get shorthand variables for the source and destination Tiles
# #         source_tile = self.tilemap[source[0]][source[1]]
# #         dest_tile = self.tilemap[dest[0]][dest[1]]
# #
# #         # Store previous state to allow for unmaking the move
# #         previous_state = {"blackScore": self.blackScore,
# #                           "whiteScore": self.whiteScore,
# #                           "blackKingCoords": self.blackKingCoords,
# #                           "whiteKingCoords": self.whiteKingCoords,
# #                           "tile1": (source, source_tile.copy()),
# #                           "tile2": (dest, dest_tile.copy()),
# #                           "gameover": self.gameover}
# #
# #         self.past_moves.append(previous_state)
# #
# #         # Update scores
# #         if dest_tile.piece:  # If a piece is on the destination tile (opponent to be captured)
# #             if self.turn == WHITE:
# #                 self.blackScore -= self.weights[type(dest_tile.piece)]  # remove opponent piece weight
# #             else:
# #                 self.whiteScore -= self.weights[type(dest_tile.piece)]  # remove opponent piece weight
# #
# #         # Promote Pawn (if requirements are met)
# #         if type(source_tile.piece) is Pawn:
# #             # If Pawn reached the end of the board (top/bottom)
# #             if (self.bottomPlayerTurn and dest_tile.y == 0) \
# #                     or (not self.bottomPlayerTurn and dest_tile.y == 7):
# #                 # Promote the Pawn to a Queen
# #                 source_tile.piece = Queen(source_tile.piece.x, source_tile.piece.y, source_tile.piece.color)
# #
# #         # Move piece from the source Tile to the destination Tile
# #         dest_tile.piece = source_tile.piece
# #         source_tile.piece.move(dest_tile.x, dest_tile.y)
# #         dest_tile.piece.firstMove = False
# #
# #         # Update King coordinates (if applicable)
# #         if type(source_tile.piece) is King:
# #             if source_tile.piece.color == BLACK:
# #                 self.blackKingCoords = dest_tile.x, dest_tile.y
# #             else:
# #                 self.whiteKingCoords = dest_tile.x, dest_tile.y
# #
# #         # Remove piece from the source Tile
# #         source_tile.piece = None
# #         source_tile.fill(source_tile.color)
# #
# #         # Check win conditions
# #         self.checkmate_stalemate()
# #         self.insufficient_material()
# #
# #     def unmake_move(self) -> None:
# #         """Undoes previous move and restores game state
# #
# #         :return: None
# #         """
# #
# #         # Revert to the previous game state (using stored values)
# #         previous_state = self.past_moves.pop()
# #         self.blackScore = previous_state["blackScore"]
# #         self.whiteScore = previous_state["whiteScore"]
# #         self.blackKingCoords = previous_state["blackKingCoords"]
# #         self.whiteKingCoords = previous_state["whiteKingCoords"]
# #         x = previous_state["tile1"][0][0]
# #         y = previous_state["tile1"][0][1]
# #         self.tilemap[x][y] = previous_state["tile1"][1]
# #         x = previous_state["tile2"][0][0]
# #         y = previous_state["tile2"][0][1]
# #         self.tilemap[x][y] = previous_state["tile2"][1]
# #         self.gameover = previous_state["gameover"]
# #
# #         self.next_turn()
# #
# #     def next_turn(self) -> None:
# #         """Swaps current board turn to the other player
# #
# #         :return: None
# #         """
# #
# #         # Swap turn color
# #         if self.turn == WHITE:
# #             self.turn = BLACK
# #         else:
# #             self.turn = WHITE
# #
# #         # Swap bottom/top player
# #         self.bottomPlayerTurn = not self.bottomPlayerTurn
# #
# #     def checkmate_stalemate(self) -> None:
# #         """Checks for checkmate or stalemate status of board
# #
# #         :return: None
# #         """
# #
# #         legal_moves = 0
# #         for x in range(8):
# #             for y in range(8):
# #                 if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
# #                     moves = self.tilemap[x][y].piece.valid_moves(self)
# #                     for move in moves:
# #                         if not self.in_check_after_move((x, y), move, self.tilemap[x][y].piece.color):
# #                             legal_moves += 1
# #
# #         # Get current opponent color
# #         if self.turn == WHITE:
# #             opponent = BLACK
# #         else:
# #             opponent = WHITE
# #
# #         # Check if there is a stalemate or checkmate
# #         if legal_moves == 0 and not self.in_check(self.turn):
# #             self.gameover = ("Stalemate", None)  # stalemate: no winner
# #         elif legal_moves == 0:
# #             self.gameover = ("Checkmate", opponent)  # checkmate: opponent wins
# #
# #     def get_moves(self):
# #         """Returns a list of the available moves for the current player
# #
# #         :return: list
# #         """
# #
# #         moves = []
# #
# #         for x in range(8):
# #             for y in range(8):
# #                 if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
# #                     for move in self.tilemap[x][y].piece.valid_moves(self):
# #                         if not self.in_check_after_move((x, y), move, self.turn):
# #                             if self.enemy_at_coords(move, self.turn):
# #                                 moves.insert(0, ((x, y), move))
# #                             else:
# #                                 moves.append(((x, y), move))
# #
# #         return list(set(moves))  # randomizing effect
# #
# #     def get_moves_sorted(self):
# #         """Returns a list of the available moves sorted in descending order by value for the current player
# #
# #         :return: list
# #         """
# #
# #         b = self.copy()
# #         moves = {}
# #
# #         for x in range(8):
# #             for y in range(8):
# #                 if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
# #                     for move in self.tilemap[x][y].piece.valid_moves(self):
# #                         if not self.in_check_after_move((x, y), move, self.turn) and ((x, y), move) not in moves:
# #                             b.make_move((x, y), move)
# #                             moves[((x, y), move)] = AI.evaluate(b, self.turn)
# #                             b.unmake_move()
# #
# #         return [move for move, score in sorted(moves.items(), key=lambda v: v[1], reverse=True)]
# #
# #     def insufficient_material(self):
# #         piece_counts = {"wminor": 0, "bminor": 0, "king": 0, "wknight": 0, "bknight": 0}
# #         for x in range(8):
# #             for y in range(8):
# #                 piece = self.tilemap[x][y].piece
# #                 if piece:
# #                     if type(piece) is Queen:
# #                         return  # If a Queen is on the board, insufficient material is impossible
# #                     if type(piece) is King:
# #                         piece_counts["king"] += 1
# #                     elif type(piece) is Knight and piece.color == WHITE:
# #                         piece_counts["wknight"] += 1
# #                     elif type(piece) is Knight and piece.color == BLACK:
# #                         piece_counts["bknight"] += 1
# #                     else:
# #                         if piece.color == WHITE:
# #                             piece_counts["wminor"] += 1
# #                         elif piece.color == BLACK:
# #                             piece_counts["bminor"] += 1
# #
# #         # King vs King
# #         if piece_counts["wminor"] == piece_counts["bminor"] == piece_counts["wknight"] == piece_counts["bknight"] == 0 \
# #                 and piece_counts["king"] == 2:
# #             self.gameover = ("Insufficient Material", None)
# #
# #         # King vs King + minor piece
# #         elif ((piece_counts["wminor"] == 1 and piece_counts["bminor"] == 0) or (piece_counts["bminor"] == 1
# #                                                                                 and piece_counts["wminor"] == 0)) \
# #                 and piece_counts["king"] == 2 and piece_counts["bknight"] == piece_counts["wknight"] == 0:
# #             self.gameover = ("Insufficient Material", None)
# #
# #         # King vs King + 2 Knights
# #         elif (piece_counts["wknight"] == 2 and piece_counts["king"] == 2
# #               and piece_counts["wminor"] == piece_counts["bminor"] == 0) \
# #                 or (piece_counts["bknight"] == 2 and piece_counts["king"] == 2
# #                     and piece_counts["wminor"] == piece_counts["bminor"] == 0):
# #             self.gameover = ("Insufficient Material", None)
# #         elif (piece_counts["wminor"] == 1 and piece_counts["king"] == 2 and piece_counts["bminor"] == 0) \
# #                 or (piece_counts["bminor"] == 1 and piece_counts["king"] == 2 and piece_counts["wminor"] == 0):
# #             self.gameover = ("Insufficient Material", None)
