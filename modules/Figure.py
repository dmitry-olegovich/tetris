""" READ ME
This module descirbes the basic classes for objects used in tetris game.

"""
from collections import namedtuple
import pygame

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

    def draw(self, screen, palette, width):
        x = self.x * width
        y = self.y * width
        pygame.draw.rect(screen, palette[self._color], 
            (x,y, width, width), 0)
    
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
        self._code = index
        if index == 6:
            self._dont_rotate = True
        else:
            self._dont_rotate = False

    def __repr__(self):
        result = ''
        for cell in self._cells:
            result += str(cell)
        return result
    
    def rotate(self):
        """Rotate figure 90 deg counter-clockwise. No safety check!"""
        
        if self._dont_rotate:
            return

        for cell in self._cells:
            cell.rotate()

    def get_rotated_cells(self):
        """Return a copy of cells as if they were rotated."""
        copy = [Cell(cell.x, cell.y, cell._color) for cell 
            in self._cells]
        for cell in copy:
            cell.rotate()
        
        return self.get_absolute_cells(self.x, self.y, copy)
        
    def left(self):
        """Change postion of the figure left. No safety check!"""

        self._pos = Coordinate(self._pos.x - 1, self._pos.y)

    def right(self):
        """Change postion of the figure right. No safety check!"""

        self._pos = Coordinate(self._pos.x + 1, self._pos.y)

    def drop(self):
        """Change postion of the figure down. No safety check!"""

        self._pos = Coordinate(self._pos.x, self._pos.y + 1)

    def draw(self, screen, palette, cell_width):
        """Draw cells one by one in absolute coordinates."""

        for cell in self.cells:
            cell.draw(screen, palette, cell_width)

    def copy(self):
        return Figure(self._code, 0, 0)

    @property
    def cells(self):
        """Return cells list with absolute coordinates."""

        return self.get_absolute_cells(self.x, self.y, self._cells)

    @property
    def color(self):
        return self._color

    @property
    def x(self):
        return self._pos.x

    @property
    def y(self):
        return self._pos.y

    @staticmethod
    def get_absolute_cells(X:int, Y:int, cell_list:list):
        """Return cell list with coordinates changed to absolute 
        relative to X,Y point.
        """
        result = []
        for cell in cell_list:
            result.append(Cell(cell.x + X,
                cell.y + Y, cell._color))

        return result

