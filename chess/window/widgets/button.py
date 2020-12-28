import pygame as pg


class Button:
    """
    A class to create an instance of a Button widget with customized images

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

    Methods
    -------
    handle_event(event)
        Handles all necessary event handlers for the Button
    draw(screen)
        Draws the widget on the screen
    """

    def __init__(self, x: int, y: int, w: int, h: int, **kwargs):
        """Class Parameters

        :param x: widget's x-coordinate position
        :param y: widget's y-coordinate position
        :param w: widget's width
        :param h: widget's height
        :param kwargs: 'image', 'space_around'
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.bounds = self.rect

        self.button_images = []
        for img in kwargs.get('image'):
            self.button_images.append(pg.image.load(img))
        # index[0] = default   index[1] = hover   index[2] = click

        if 'space_around' in kwargs:
            spacing = kwargs.get('space_around')
            self.bounds = pg.Rect(self.x + spacing, self.y, self.w - spacing * 2, self.h)

        self.command_switch = False  # Flag variable for detecting when to run the button command

        self.state = 0  # 0 = default, 1 = hover, 2 = click

    def handle_event(self, event) -> None:
        """Handles all necessary event handlers for the Button

        :param event: the pygame event for handling widget events
        :return: None
        """

        if self.bounds.collidepoint(pg.mouse.get_pos()):
            # Click Up (SUBMIT)
            if event.type == pg.MOUSEBUTTONUP and self.state == 2:
                self.state = 1
                self.command_switch = True

            # Click Down
            elif event.type == pg.MOUSEBUTTONDOWN or self.state == 2:
                self.state = 2

            # Hover
            else:
                self.state = 1

        # Default
        else:
            self.state = 0

    def draw(self, screen: pg.Surface) -> None:
        """Draws the widget on the screen

        :param screen: the surface to draw the widget onto
        :return: None
        """

        screen.blit(self.button_images[self.state], self.rect)
