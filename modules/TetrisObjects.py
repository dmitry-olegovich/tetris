""" READ ME
This module descirbes the basic classes for objects used in tetris game.

"""

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
    def __init__(self, x:int, y:int, color:int):
        self._pos = (x, y)
        self._color = color
        self._static = False
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def rotation(self):
        """Change position as if the cell is rotated 90 deg. clockwise
        around the 0,0 point.
        """
        self._pos = (self._pos[1], -self._pos[0])
    
    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]



class Figure():
    """Tetris figure - "consist" of 'Cell' objects as building blocks.
    
    Args:
        figure_code (int): code that defines what the figure will be;
            it is used to get the items for init process from a 
            '_FIGURES' class atribute.

    Atributes:
        _pos (tuple): position of the center cell (that is at 0,0).
        _cells (list): list of 'Cell' objects.
        _color (int): color of the cells.
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

    def __init__(self, figure_code):
        index = figure_code % len(self._FIGURES)
        self._color = index
        self._cells = [Cell(x, y, self._color) for x, y in self._FIGURES[index]]
            
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

    def __repr__(self):
        x_min, x_max = self.x_range
        y_min, y_max = self.y_range
        line = '.' * (abs(x_max - x_min) + 1)
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
    for i in range(7):
        obj = Figure(i)
        print(obj, end="\n\n")
   

