import pygame
import threading
import queue
import sys
from math import inf
from ..data import *
from ..chess_engine import Board, Timer, AI


class ChessScreen:
    """
    A class to execute and manage the main Chess Game screen

    ...

    Attributes
    ----------
    p1_name : str
        the user's name
    p1_color : tuple
        the user's piece color (BLACK/WHITE)
    p2_name : str
        the name indicating the opponent type (AI/Human)

    Methods
    -------
    run()
        Runs the main Chess Game loop
    end_screen(condition, winner=None)
        Displays a 'Game Over' pop-up with information pertaining to the endgame
    reset_board()
        Resets the board and makes changes to the game state to restart the game
    draw_names()
        Displays both player names
    draw_turn_indicator()
        Displays an indicator of the current player's turn
    draw_resign_button()
        Displays the 'Resign' button on the screen
    draw_end_message(condition, winner)
        Draws the 'Game Over' message in the end screen pop-up
    determine_move()
        Determines the move for the AI (and places the move in a thread-safe container)
    fade(width, height, out=True, min_alpha=0, max_alpha=175, color=BG_COLOR)
        Creates a fading animation to transition between pages
    update(event=None)
        Empty method used for this class to be used with other pages
    """

    def __init__(self, p1_name: str, p1_color: tuple, p2_name: str):
        """Class Parameters

        :param p1_name: the user's name
        :param p1_color: the user's piece color (BLACK/WHITE)
        :param p2_name: the name indicating the opponent type (AI/Human)
        """

        self.p1_name = p1_name
        self.p2_name = p2_name

        self.p1_timer = Timer(600, "bot")
        self.p2_timer = Timer(600, "top")

        self.p1_color = p1_color
        self.p2_color = BLACK if p1_color == WHITE else WHITE

        self.ai_move = queue.Queue()
        self.lock = threading.Lock()

        self.board = Board(self.p1_color)
        self.board.initialize_pieces()

        self.first_run = True
        self.running = True  # When false, go back to main menu

    def run(self):
        """Runs the main Chess Game loop

        :return: end_screen() method to display the 'Game Over' pop-up
        """

        clock = pygame.time.Clock()
        dt = 0
        t = threading.Thread(target=self.determine_move)
        p1_resigned = False

        resign_button = pygame.Rect(BOARD_X + BOARD_SIZE + 8, BOARD_Y + BOARD_SIZE + 8,
                                    int((TILE_SIZE * 4 + 8) / 2 - 4), 28)

        fading = True  # Flag variable to control the fading effect

        while True:
            for event in pygame.event.get():
                # Window closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Mouse click (button pressed or piece selected
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.select()
                    mouse_pos = event.pos
                    self.board.draw()
                    pygame.display.flip()

                    # 'Resign' button pressed?
                    if resign_button.collidepoint(mouse_pos):
                        p1_resigned = True

            # Apply fade effect
            if fading and self.first_run:
                self.fade(SCREEN_WIDTH, SCREEN_HEIGHT, False, max_alpha=255, color=BLACK)
                fading = False
                self.first_run = False

            # Background
            SCREEN.fill(BG_COLOR)

            # Decrement timer for the current player's turn
            if self.board.turn == self.p2_color:
                self.p2_timer.tick(dt)
            else:
                self.p1_timer.tick(dt)

            # Draw UI elements
            self.draw_names()
            self.draw_turn_indicator()
            self.p1_timer.draw()
            self.p2_timer.draw()
            self.draw_resign_button()

            # Check for endgame state
            self.board.checkmate_stalemate()
            self.board.insufficient_material()

            # GAME OVER: Checkmate, Stalemate, or Insufficient Material
            if self.board.gameover:
                print("GAME OVER: ", self.board.gameover[0])
                if self.board.gameover[0] == "Insufficient Material" or self.board.gameover[0] == "Stalemate":
                    return self.end_screen(self.board.gameover[0], None)
                else:
                    if self.board.gameover[1] == self.board.player:
                        return self.end_screen(self.board.gameover[0], self.p1_name)
                    else:
                        return self.end_screen(self.board.gameover[0], self.p2_name)

            # GAME OVER: Player 1 ran out of time
            if self.p1_timer.time <= 0:
                print("GAME OVER: Timeout")
                return self.end_screen("Timeout", self.p2_name)

            # GAME OVER: Player 2 ran out of time
            if self.p2_timer.time <= 0:
                print("GAME OVER: Timeout")
                return self.end_screen("Timeout", self.p1_name)

            # GAME OVER: Player 1 has resigned
            if p1_resigned:
                print("GAME OVER: Resignation")
                return self.end_screen("Resignation", self.p2_name)

            if self.p2_name == "Computer":
                # Tell AI to determine move if...
                #   1. It is their turn
                #   2. They have not found a move yet
                #   3. The game is not over
                #   4. They are not currently finding a move ('determine_move' thread is not running)
                self.lock.acquire()
                if self.board.turn == self.p2_color \
                        and self.ai_move.qsize() == 0 \
                        and not self.board.gameover \
                        and not t.is_alive():
                    # Remake thread (since a thread can only be started once)
                    t = threading.Thread(target=self.determine_move)
                    t.start()
                self.lock.release()

                # Tell AI to make move if...
                #   1. It is their turn
                #   2. They found a move
                #   3. The game is not over
                if self.board.turn == self.p2_color \
                        and self.ai_move.qsize() > 0 \
                        and not self.board.gameover:
                    move = self.ai_move.get()
                    self.board.make_move(move[0], move[1])
                    self.board.next_turn()

            # Update the time since the last frame
            dt = clock.tick(30) / 1000

            # Draw all board components
            self.board.draw()

            # Update the display
            pygame.display.flip()

    def end_screen(self, condition: str, winner=None):
        """Displays a 'Game Over' pop-up with information pertaining to the endgame

        :param condition: a string representing the win condition that ended the game
        :param winner: the name of the winning player (if applicable)
        :return: None
        """

        # Background
        bg = pygame.Rect(int(BOARD_X + TILE_SIZE * 2.5), int(BOARD_Y + TILE_SIZE * 2.5), TILE_SIZE * 3, TILE_SIZE * 2)

        # Collision boxes for 'Rematch' and 'Leave' buttons
        rematch_button = pygame.Rect(bg.left, bg.bottom - 28, bg.centerx - bg.left - 2, 28)
        leave_button = pygame.Rect(bg.centerx + 2, bg.bottom - 28, bg.centerx - bg.left - 2, 28)

        fading = True  # Flag variable to control the fading effect

        # End screen loop
        while True:
            for event in pygame.event.get():
                # Window closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Mouse click (button pressed or piece selected)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # 'Rematch' button pressed
                    if rematch_button.collidepoint(mouse_pos):
                        self.reset_board()
                        self.fade(SCREEN_WIDTH, SCREEN_HEIGHT, False)
                        return self.run()

                    # 'Leave' button pressed
                    if leave_button.collidepoint(mouse_pos):
                        self.reset_board()
                        self.running = False
                        self.fade(SCREEN_WIDTH, SCREEN_HEIGHT, min_alpha=175, max_alpha=255)
                        return

            # Apply fade effect
            if fading:
                self.fade(SCREEN_WIDTH, SCREEN_HEIGHT)
                fading = False

            # Draw UI elements
            self.draw_end_message(condition, winner)

            # Update display
            pygame.display.flip()

    def reset_board(self) -> None:
        """Resets the board and makes changes to the game state to restart the game

        :return: None
        """

        self.p1_timer.reset()
        self.p2_timer.reset()
        self.board = Board(self.p1_color)
        self.board.initialize_pieces()
        self.ai_move = queue.Queue()

    def draw_names(self) -> None:
        """Displays both player names

        :return: None
        """

        # Draw the top player's name (player 2)
        pygame.draw.rect(SCREEN, BG_COLOR_LIGHT, [BOARD_X, BOARD_Y - 36, TILE_SIZE * 2, 28])
        p1name = FONT.render(self.p2_name, True, SMALL_TEXT_COLOR)
        SCREEN.blit(p1name, (BOARD_X + 4, BOARD_Y - 34))

        # Draw the bottom player's name (player 1)
        pygame.draw.rect(SCREEN, BG_COLOR_LIGHT, [BOARD_X, BOARD_Y + BOARD_SIZE + 8, TILE_SIZE * 2, 28])
        p2name = FONT.render(self.p1_name, True, SMALL_TEXT_COLOR)
        SCREEN.blit(p2name, (BOARD_X + 4, BOARD_Y + BOARD_SIZE + 10))

    def draw_turn_indicator(self) -> None:
        """Displays an indicator of the current player's turn

        :return: None
        """

        if self.board.turn == self.p1_color:
            txt = FONT.render("YOUR TURN", True, LARGE_TEXT_COLOR)
            SCREEN.blit(txt, (int(BOARD_X + TILE_SIZE * 3.5 + 8), BOARD_Y + BOARD_SIZE + 10))
        else:
            txt = FONT.render("Thinking...", True, LARGE_TEXT_COLOR)
            SCREEN.blit(txt, (int(BOARD_X + TILE_SIZE * 3.5 + 8), BOARD_Y + BOARD_SIZE + 10))

    @staticmethod
    def draw_resign_button() -> None:
        """Displays the 'Resign' button on the screen

        :return: None
        """

        pygame.draw.rect(SCREEN, BG_COLOR_LIGHT, [BOARD_X + BOARD_SIZE + 8, BOARD_Y + BOARD_SIZE + 8,
                                                  int((TILE_SIZE * 4 + 8) / 2 - 4), 28])
        txt = FONT.render("Resign", True, SMALL_TEXT_COLOR)
        SCREEN.blit(txt, (BOARD_X + BOARD_SIZE + 40, BOARD_Y + BOARD_SIZE + 10))

    @staticmethod
    def draw_end_message(condition: str, winner: str) -> None:
        """Draws the 'Game Over' message in the end screen pop-up

        :param condition: a string representing the win condition that ended the game
        :param winner: the name of the winning player (if applicable)
        :return: None
        """

        # Draw 'Game Over' text
        bg = pygame.draw.rect(SCREEN, BG_COLOR_LIGHT,
                              [int(BOARD_X + TILE_SIZE * 2.5), int(BOARD_Y + TILE_SIZE * 2.5), TILE_SIZE * 3,
                               TILE_SIZE * 2])
        pygame.draw.rect(SCREEN, BLACK,
                         [int(BOARD_X + TILE_SIZE * 2.5), int(BOARD_Y + TILE_SIZE * 2.5), TILE_SIZE * 3, TILE_SIZE * 2],
                         1)
        txt = BIG_FONT.render("Game Over", True, LARGE_TEXT_COLOR)
        SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3 - 8, int(BOARD_Y + TILE_SIZE * 2.5 + 4)))

        # Draw the win condition and the winning player (if applicable)
        if winner:
            txt = FONT.render(winner + " won", True, SMALL_TEXT_COLOR)
            SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3, BOARD_Y + TILE_SIZE * 3 + 4))
            txt = FONT.render(f"by {condition}", True, SMALL_TEXT_COLOR)
            SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3, int(BOARD_Y + TILE_SIZE * 3.4)))
        else:
            txt = FONT.render(f"{condition}", True, SMALL_TEXT_COLOR)
            if condition == "Insufficient Material":
                SCREEN.blit(txt, (int(BOARD_X + TILE_SIZE * 2.55), int(BOARD_Y + TILE_SIZE * 3.3)))
            else:
                SCREEN.blit(txt, (int(BOARD_X + TILE_SIZE * 3.2), int(BOARD_Y + TILE_SIZE * 3.3)))

        # Draw the 'Rematch' button
        pygame.draw.rect(SCREEN, BLACK, [bg.left, bg.bottom - 28, bg.centerx - bg.left + 3, 28], 1)
        txt = FONT.render("Rematch", True, SMALL_TEXT_COLOR)
        SCREEN.blit(txt, (bg.left + 8, bg.bottom - 28 + 2))

        # Draw the 'Leave' button
        pygame.draw.rect(SCREEN, BLACK, [bg.centerx + 2, bg.bottom - 28, bg.centerx - bg.left - 2, 28], 1)
        txt = FONT.render("Leave", True, SMALL_TEXT_COLOR)
        SCREEN.blit(txt, (bg.centerx + 20, bg.bottom - 28 + 2))

    def determine_move(self) -> None:
        """Determines the move for the AI (and places the move in a thread-safe container)

        :return: None
        """

        if self.p2_name == "Computer":
            self.ai_move.put(AI.minimax(self.board.copy(), 3, inf, -inf, True, self.p2_color)[0])

        # Close the thread after a move has been found
        sys.exit()

    def fade(self, width: int, height: int, out=True, min_alpha=0, max_alpha=175, color=BG_COLOR) -> None:
        """Creates a fading animation to transition between pages

        :param width: the screen width
        :param height: the screen height
        :param out: a flag variable for fading in/out (default: fade out)
        :param min_alpha: the minimum alpha value (default: 0)
        :param max_alpha: the maximum alpha value (default: 175)
        :param color: the background color to fade in/out from
        :return: None
        """

        if out:  # Fade out
            veil = pygame.Surface((width, height))
            veil.fill(color)
            for alpha in range(min_alpha, max_alpha):
                veil.set_alpha(alpha)
                self.board.draw()
                SCREEN.blit(veil, (0, 0))
                pygame.display.update()
                pygame.time.delay(1)

        else:  # Fade in
            veil = pygame.Surface((width, height))
            veil.fill(color)
            for alpha in reversed(range(min_alpha, max_alpha)):
                veil.set_alpha(alpha)

                # Draw UI elements
                SCREEN.fill(BG_COLOR)
                self.draw_names()
                self.draw_turn_indicator()
                self.p1_timer.draw()
                self.p2_timer.draw()
                self.draw_resign_button()
                self.board.draw()

                SCREEN.blit(veil, (0, 0))
                pygame.display.update()
                pygame.time.delay(1)

    def update(self, event=None):
        pass
