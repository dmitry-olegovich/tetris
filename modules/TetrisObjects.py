""" READ ME
This module descirbes the basic classes for objects used in tetris game.

"""
from collections import namedtuple

Coordinate = namedtuple('Coord', ['x', 'y'])

class Cell():
    """Simple cell - building block of other objects.

    Args:
        x (int): horisontal starting positon.
        y (int): vertical starting positon.
        color (int): color.

    Atributes:
        _pos (tuple): (x,y) positon of the cell, not relative to the
            object, that the cell is a part of.
        _color (int): this is used to store color number value.
        _static (bool): static cells do not move.
    """
    def __init__(self, x: int = 0, y: int = 0, color: int = 1):
        self._pos = Coordinate(x=x, y=y)
        self._color = color
        self._static = False
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def rotate(self):
        """Change position as if the cell is rotated 90 deg 
        counter-clockwise around the 0,0 point.
        """
        self._pos = Coordinate(self.y, -self.x)
    
    # Not needed maybe?
    @property
    def x(self):
        return self._pos.x
    
    # Not needed maybe?
    @property
    def y(self):
        return self._pos.y



class Figure():
    """Tetris figure - consists of 'Cell' objects as building blocks.
    
    Args:
        figure_code (int): code that defines what the figure will be;
            it is used to get the items for init process from a 
            '_FIGURES' class atribute.

    Atributes:
        _pos (tuple): position of the center cell (that is at 0,0),
        _cells (list): list of 'Cell' objects,
        _color (int): color of the cells,
        _dont_rotate (bool): as square blocks look wierd when rotated.
    """
    
    _FIGURES = [
        [(0,0), (-1,0), (1,0), (2,0)],      # line
        [(0,0), (0,-1), (0,1), (1,1)],      # L-shape
        [(0,0), (0,-1), (0,1), (-1,1)],     # mirrored L-shape
        [(0,0), (0,-1), (-1,0), (1,0)],     # tri-block
        [(0,0), (-1,0), (0,1), (1,1)],      # s-block
        [(0,0), (1,0), (0,1), (-1,1)],      # mirrored s-block
        [(0,0), (1,0), (0,1), (1,1)],       # square
    ]

    def __init__(self, figure_code: int = 0, x: int = 0, y: int = 0):
        index = figure_code % len(self._FIGURES)
        self._color = index + 1  # can never be 0
        self._cells = [Cell(x, y, self._color) for x, y 
            in self._FIGURES[index]]
        self._pos = Coordinate(x, y)
        if index = 6:
            self._dont_rotate = True
        else:
            self._dont_rotate = False
    
    def rotate(self):
        """Rotate figure 90 deg counter-clockwise. No safety check!"""
        
        if self._dont_rotate:
            return

        for cell in self._cells:
            cell.rotate()

    def left(self):
        """Change postion of the figure left. No safety check!"""

        self._pos = Coordinate(self._pos.x - 1, self._pos.y)

    def right(self):
        """Change postion of the figure right. No safety check!"""

        self._pos = Coordinate(self._pos.x + 1, self._pos.y)

    def drop(self):
        """Change postion of the figure down. No safety check!"""

        self._pos = Coordinate(self._pos.x, self._pos.y + 1)

    @property
    def cells(self):
        """Return cells list with absolute coordinates."""

        result = []
        for cell in self._cells:
            result.append(Cell(cell.x + self.x,
                cell.y + self.y, self.color))

        return result

    @property
    def color(self):
        return self._color

    @property
    def x(self):
        return self._pos.x

    @property
    def y(self):
        return self._pos.y

    # only used for debug purposed __repr__ 
    @property
    def x_range(self):
        """Return the min and max X coord of the cells."""

        min, max = 0, 0
        for cell in self._cells:
            if cell.x < min:
                min = cell.x
            if cell.x > max:
                max = cell.x
        
        return min, max
    
    # only used for debug purposed __repr__ 
    @property
    def y_range(self):
        """Return the min and max Y coord of the cells."""

        min, max = 0, 0
        for cell in self._cells:
            if cell.y < min:
                min = cell.y
            if cell.y > max:
                max = cell.y
        
        return min, max

    # only needed for debug purposes
    def __repr__(self):
        x_min, x_max = self.x_range
        y_min, y_max = self.y_range
        line = ' ' * (abs(x_max - x_min) + 1)
        text = [ list(line) for x in range((abs(y_max - y_min) + 1))]
        
        for cell in self._cells:
            text[cell.y - y_min][cell.x - x_min] = 'X'
        
        result = ''
        for line in text:
            for char in line:
                result += char
            result += '\n'

        return result

if __name__ == "__main__":
    """for i in range(7):
        obj = Figure(i)
        print(obj, end="\n")
        obj.rotate()
        print(obj, end="\n\n")
    """
    obj = Figure(1)
    print(obj, end="\n")
    obj.rotate()
    print(obj, end="\n\n")