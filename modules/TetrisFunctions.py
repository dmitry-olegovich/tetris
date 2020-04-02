import pdb

from random import randrange

from .StaticObjects import Field
from .TetrisObjects import Figure

def down_or_stop(field, fig):
    """Drop figure if no field cells in the way."""

    if field.check_down(fig):
        fig.drop()
        return fig
    else:
        field.grow(fig)
        return generate_new_figure(field.width)

def left_or_not(field, fig):
    """Move figure left if no field cells in the way."""

    if field.check_left(fig):
        fig.left()

def right_or_not(field, fig):
    """Move figure right if no field cells in the way."""

    if field.check_right(fig):
        fig.right()

def rotate_or_not(field, fig):
    """Rotate figure if it won't intersect with field after."""

    if field.check_rotation(fig):
        fig.rotate()

def generate_new_figure(width):
    code = randrange(0, len(Figure._FIGURES))
    return Figure(code, x=int(width/2) - 1, y=0)




