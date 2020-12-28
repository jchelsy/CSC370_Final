import pygame as pg


class Selector:
    """
    A class to create an instance of a Selector widget with customized images

    ...

    Attributes
    ----------
    x : int
        widget's x-coordinate position
    y : int
        widget's y-coordinate position
    w : int
        widget's width
    h : int
        widget's height
    options : list
        a list of tuples of information regarding the selection options

    Methods
    -------
    update()
        Updates the size of the selection arrows depending on the current state
    switch_left()
        Handles the left arrow selector click
    switch_right()
        Handles the right arrow selector click
    handle_event(event)
        Handles all necessary event handlers for the Selector
    draw(screen)
        Draws the widget on the screen
    """

    def __init__(self, x: int, y: int, w: int, h: int, options, **kwargs):
        """Class Parameters

        :param x: widget's x-coordinate position
        :param y: widget's y-coordinate position
        :param w: widget's width
        :param h: widget's height
        :param options: a list of tuples of information regarding the selection options
        :param kwargs: 'left_arrow', 'right_arrow'
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.bounds = pg.Rect(self.x, self.y, self.w, self.h)

        self.arrow_left = []
        self.arrow_right = []
        self.options = []

        for img in kwargs.get('left_arrow'):
            self.arrow_left.append(pg.image.load(img))

        for img in kwargs.get('right_arrow'):
            self.arrow_right.append(pg.image.load(img))

        for item in options:
            self.options.append((pg.image.load(item[0]), item[1]))

        self.state_left = 0
        self.state_right = 0

        self.current_index = 0

        self.first_index = 0
        self.last_index = len(self.options) - 1

        self.left_rect = None
        self.right_rect = None
        self.option_rect = None
        self.update()

        self.command_switch = False

        if self.current_index == self.first_index:
            self.state_left = 3

        if self.current_index == self.last_index:
            self.state_right = 3

    def update(self) -> None:
        """Updates the size of the selection arrows depending on the current state

        :return: None
        """

        self.left_rect = pg.Rect(self.x,
                                 self.y + int((self.h - self.arrow_left[self.state_left].get_height()) / 2),
                                 self.arrow_left[self.state_left].get_width(),
                                 self.arrow_left[self.state_left].get_height())

        self.right_rect = pg.Rect(self.x + (self.w - self.arrow_right[self.state_right].get_width()),
                                  self.y + int((self.h - self.arrow_right[self.state_right].get_height()) / 2),
                                  self.arrow_right[self.state_right].get_width(),
                                  self.arrow_right[self.state_right].get_height())

        self.option_rect = pg.Rect(self.x + int((self.w - self.options[self.current_index][0].get_width()) / 2),
                                   self.y + int((self.h - self.options[self.current_index][0].get_height()) / 2),
                                   self.options[self.current_index][0].get_width(),
                                   self.options[self.current_index][0].get_height())

    def switch_left(self) -> None:
        """Handles the left arrow selector click

        :return: None
        """

        self.current_index -= 1
        self.command_switch = True

        if self.current_index == self.first_index:
            self.state_left = 3

        if self.current_index != self.last_index:
            self.state_right = 0

    def switch_right(self) -> None:
        """Handles the right arrow selector click

        :return: None
        """

        self.current_index += 1
        self.command_switch = True

        if self.current_index == self.last_index:
            self.state_right = 3

        if self.current_index != self.first_index:
            self.state_left = 0

    def handle_event(self, event) -> None:
        """Handles all necessary event handlers for the Selector

        :param event: the pygame event for handling widget events
        :return: None
        """

        self.command_switch = False

        if self.current_index == self.first_index:
            self.state_left = 3

        if self.current_index == self.last_index:
            self.state_right = 3

        pos = pg.mouse.get_pos()
        if self.bounds.collidepoint(pos):
            if self.left_rect.collidepoint(pos):
                if self.state_left != 3:
                    # Click Release (SUBMIT)
                    if event.type == pg.MOUSEBUTTONUP and self.state_left == 2:
                        self.switch_left()
                        if self.state_left != 3:
                            self.state_left = 1

                    # Click
                    elif event.type == pg.MOUSEBUTTONDOWN or self.state_left == 2:
                        self.state_left = 2

                    # Hover
                    else:
                        self.state_left = 1
                else:
                    return

            elif self.right_rect.collidepoint(pos):
                if self.state_right != 3:
                    # Click Release (SUBMIT)
                    if event.type == pg.MOUSEBUTTONUP and self.state_right == 2:
                        self.switch_right()
                        if self.state_right != 3:
                            self.state_right = 1

                    # Click
                    elif event.type == pg.MOUSEBUTTONDOWN or self.state_right == 2:
                        self.state_right = 2

                    # Hover
                    else:
                        self.state_right = 1
                else:
                    return

            else:
                if self.state_left != 3:
                    self.state_left = 0
                if self.state_right != 3:
                    self.state_right = 0
        else:
            if self.state_left != 3:
                self.state_left = 0
            if self.state_right != 3:
                self.state_right = 0

    def draw(self, screen: pg.Surface) -> None:
        """Draws the widget on the screen

        :param screen: the surface to draw the widget onto
        :return: None
        """

        left = self.arrow_left[self.state_left]
        right = self.arrow_right[self.state_right]
        option = self.options[self.current_index][0]

        self.update()

        screen.blit(left, self.left_rect)
        screen.blit(right, self.right_rect)
        screen.blit(option, self.option_rect)
