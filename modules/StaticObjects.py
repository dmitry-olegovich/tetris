""" READ ME
This module descirbes the basic classes for static objects used 
in tetris game, such as:
- screen boundary,
- fallen static cells.
"""

from .TetrisObjects import Figure, Cell

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

    @property
    def width(self):
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
            self._array[cell.y][cell.x] = figure.color

    def check_down(self, figure):
        """Check if figure can go down."""
        
        for cell in figure.cells:
            if cell.y + 1 >= self.height:
                return False
            if self._array[cell.y + 1][cell.x]:
                return False
        
        return True

    def check_left(self, figure):
        """Check if figure can go left."""

        for cell in figure.cells:
            if cell.x - 1 < 0:
                return False
            if self._array[cell.y][cell.x - 1]:
                return False
        
        return True

    def check_right(self, figure):
        """Check if figure can go right."""

        for cell in figure.cells:
            if cell.x + 1 >= self.width:
                return False
            if self._array[cell.y][cell.x + 1]:
                return False
        
        return True

    def check_rotation(self, figure):
        """Check if figure after rotation is not intersecting self."""

        for cell in figure.get_rotated_cells():
            if self._array[cell.y][cell.x]:
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

    def remove_lines(self, line_list: list):
        """Fills lines as passed (by line num.) in line_list w/ 0."""

        for index in line_list:
            self._array[index] = [0 for x in range(self.width)]

if __name__ == "__main__":
    field = Field()
    fig = Figure(0, 5, 19)
    field.grow(fig)
    print(field, end='\n\n')
    fig = Figure(0, 6, 6)
    fig.rotate()
    while field.check_down(fig):
        fig.drop()
    field.grow(fig)
    print(field)
    