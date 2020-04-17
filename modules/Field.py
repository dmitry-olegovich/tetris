""" READ ME
This module descirbes the basic classes for static objects used 
in tetris game, such as:
- screen boundary,
- fallen static cells.
"""
import pdb

from .Timer import Counter
from .Figure import Figure, Cell

class Field():
    """Describes the fallen static cells.
    
    Args:
        max_x (int): horisontal size
        max_y (int): vertical size
    
    Attributes:
        _array (list): 2D list; 0 = empty, non-0 = color of cell
    """

    def __init__(self, max_x: int = 10, max_y: int = 20):
        self._array = [list([0] * max_x) for Y in range(max_y)]

    def __repr__(self):
        result = ''
        for line in self._array:
            for elem in line:
                if elem == 0:
                    result += '_'
                else:
                    result += 'X'
            result += '\n'
        return result

    def __len__(self):
        return len(self._arr)

    @property
    def width(self):
        #pdb.set_trace()
        return len(self._array[0])

    @property
    def height(self):
        return len(self._array)

    def draw(self, screen, palette, width):
        for y in range(self.height):
            for x in range(self.width):
                if self._array[y][x] != 0:
                    cell = Cell(x, y, self._array[y][x])
                    cell.draw(screen, palette, width)

    def grow(self, figure):
        """Add figure to field of fallen cells."""
        for cell in figure.cells:
            if cell.y < 0:    # endgame condition
                return False
            self._array[cell.y][cell.x] = figure.color

        return True

    def check_down(self, figure):
        """Check if figure can go down."""
        
        for cell in figure.cells:
            if cell.y + 1 < 0:
                continue  # this cell is not going out yet
            elif cell.y + 1 >= self.height:
                return False
            elif self._array[cell.y + 1][cell.x]:
                return False
        
        return True

    def check_left(self, figure):
        """Check if figure can go left."""

        for cell in figure.cells:
            x = cell.x
            y = cell.y
            if y < 0:
                y = 0  # top border doesn't matter
            if x - 1 < 0:
                return False
            if self._array[y][x - 1]:
                return False
        
        return True

    def check_right(self, figure):
        """Check if figure can go right."""

        for cell in figure.cells:
            x = cell.x
            y = cell.y
            if y < 0:
                y = 0  # top border doesn't matter
            if x + 1 >= self.width:
                return False
            if self._array[y][x + 1]:
                return False
        
        return True

    def check_rotation(self, figure):
        """Check if figure after rotation is not intersecting self."""

        for cell in figure.get_rotated_cells():
            x = cell.x
            y = cell.y
            if y < 0:
                y = 0  # top border doesn't matter
            if x < 0 or x >= self.width:
                return False
            if self._array[y][x]:
                return False
        
        return True

    def check_full_lines(self):
        """Return list of line numbers that are full."""
        
        result = []

        for i in range(self.height):
            if self.check_full_line(i):
                result.append(i)
        
        return result

    def check_full_line(self, line_num):
        """Return True if line is full."""
        
        if 0 in self._array[line_num]:
            return False

        return True
    
    def flash_lines(self, numbers):
        """CURRENTLY DOESN'T WORK AS INTENDED"""
        if len(numbers) == 0:
            return
        self.remove_lines(numbers)
        return
        
    def highlight_lines(self, numbers):
        """CURRENTLY DOESN'T WORK ANYWAY"""
        highlighted = [-1 for x in len(self._array[0])]
        for linenum in numbers:
            self._array[linenum] = highlighted

    def remove_lines(self, line_list: list):
        """Fills lines as passed (by line num.) in line_list w/ 0."""

        for index in line_list:
            self._array[index] = [0 for x in range(self.width)]

        self.shift_lines(line_list)

    def shift_lines(self, line_list):
        copy = [list([0] * self.width) for i 
            in range(len(line_list))]
        
        line_list = sorted(line_list)
        if line_list[-1] != self.height:
            line_list.append(self.height)

        segment_start = 0
        for line_num in line_list:
            if line_num - segment_start >= 0:
                copy += self._array[segment_start:line_num]
            segment_start = line_num + 1 
        
        self._array = copy
        



