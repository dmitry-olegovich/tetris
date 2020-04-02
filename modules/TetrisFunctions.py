
from .StaticObjects import Field
from .TetrisObjects import Figure

def down_or_stop(field, fig):
    """Drop figure if no field cells in the way."""

    if field.check_down(fig):
        fig.drop()
    else:
        field.grow(fig)

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




