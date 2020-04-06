#import pdb
import sys
from collections import deque
from random import randrange
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from .Field import Field
from .Figure import Figure
from .MoveLogic import idle, down_or_stop, left_or_not, right_or_not,\
    rotate_or_not

class Moveset():
    """DOCSTRING HERE
    """
    
    IDLE = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    ROTATE = 4

    moves = [
        idle,
        down_or_stop,
        left_or_not,
        right_or_not,
        rotate_or_not,
    ]

def process_input(event, figure, field):
    """Return new figure after a move based on a keypress event."""

    if event.type == QUIT:
        return False, figure
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            return False, figure
        if event.key == K_DOWN:
            figure = down_or_stop(field, figure)
        elif event.key == K_LEFT:
            figure = left_or_not(field, figure)
        elif event.key == K_RIGHT:
            figure = right_or_not(field, figure)
        elif event.key == K_UP:
            figure = rotate_or_not(field, figure)
    
    return True, figure

def process_input_held(key_list):
    """Return a dict of moves w/ 0/1 values based on held keys."""

    moves = {}
    moves[Moveset.DOWN] = key_list[K_DOWN]
    moves[Moveset.RIGHT] = key_list[K_RIGHT]
    moves[Moveset.LEFT] = key_list[K_LEFT]
    
    return moves

def move_figure(moveset: dict, figure: Figure, field: Field):
    """Return new figure after a move based on a moves in moveset dict.
    """
    
    for key in moveset:
        if moveset[key]:
            figure = Moveset.moves[key](field, figure)

    return figure