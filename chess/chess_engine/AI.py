import random
from math import inf
from ..data.settings import *


def random_move(board) -> list:
    """Selects a random valid move for the current player

    :param board: reference to the current Board object
    :return: a tuple representation of a move; format ((sourceX, sourceY), (destX, destY))
    """

    moves = board.get_moves()
    if moves:
        return random.choice(moves)


def evaluate(board, maximizing_color: tuple) -> int:
    """Provides a value representing the board at a given state (Heuristic Evaluation)

    :param board: reference to the current Board object
    :param maximizing_color: RGB color associated with the maximizing player
    :return: an integer representing the current board status
    """

    if maximizing_color == WHITE:
        return board.whiteScore - board.blackScore
    else:
        return board.blackScore - board.whiteScore


def minimax(board, depth: int, alpha: float, beta: float, maximizing_player: bool, maximizing_color: tuple) -> tuple:
    """Minimax Algorithm to find the best move for the AI

    :param board: reference to the current Board object
    :param depth: how deep to search the tree of possible moves
    :param alpha: the best value that the maximizer can guarantee at the current level and above
    :param beta: the best value that the minimizer can guarantee at the current level and above
    :param maximizing_player: True if the player is the Maximizer
    :param maximizing_color: RGB color of the AI using this function
    :return: a tuple representation of a move; format: (move, eval)
    """

    if depth == 0 or board.gameover:
        return None, evaluate(board, maximizing_color)

    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximizing_player:
        max_eval = -inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, False, maximizing_color)[1]
            board.unmake_move()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            """ Alpha-beta pruning """
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
            """ ================== """
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, True, maximizing_color)[1]
            board.unmake_move()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            """ Alpha-beta pruning """
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
            """ ================== """
        return best_move, min_eval
