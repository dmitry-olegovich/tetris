""" This module provides a Tetris class - all that is going on in the 
Tetris game screen, i.e. the the game field with falling figures.
"""
import pygame

from .Figure import Figure

class InfoPanel():
    """Describes game information object .
    
    Args:
        config (dict): a dictionary that must contain keys:
            'cell_width': (int) width of single cell in px,
            'width': (int) width of field in num of cells,
            'height': (int) height of field in num of cells,
            'turn_cycles': (int) number of ticks for a turn on speed 1,
            'palette': a list of colors set as (r,g,b) tuples,
            'speed': (int) initial game speed

    Attributes:
        _next (Figure.Figure): generated random next figure to drop;
        _score (int): current score;
        _lines (int): current total removed lines;
        _speed (int): current game speed;
        _cell_width (int): cell width in px from config
        _palette (list): list of used colors - (r,g,b) tuples.
        
    """
    
    def __init__(self, config: dict):
        self._next = Figure(0,0,0)
        self._score = 0
        self._lines = 0
        self._speed = config['speed']
        self._cell_width = config['cell_width']
        self._screen_res = (config['cell_width']*6,
            config['cell_width']*10)
        self._palette = config['palette'][:]
        
    def draw(self):
        """Return a pygame.Surface object with figure and field cell."""

        surface = pygame.Surface(self._screen_res)
        if self._next is not None:
            self._next.draw(surface, self._palette,
                self._cell_width)

        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        score = myfont.render(f'Score: {self._score}', False, (250, 250, 250))  # debug values
        score_coords = (0, 100)  # debug values
        level = myfont.render(f'Level: {self._speed}', False, (250, 250, 250))  # debug values
        level_coords = (0, 120)  # debug values
        lines = myfont.render(f'Lines: {self._lines}', False, (250, 250, 250))  # debug values
        lines_coords = (0, 140)  # debug values

        surface.blit(score, score_coords)
        surface.blit(level, level_coords)
        surface.blit(lines, lines_coords)

        return surface
        

        #print(f"SPEED: {self._speed}\nLINES: {self._lines}\nSCORE: {self._score}\nNEXT: {self._next}\n")  # debug
        #return 0
   
    def update(self, info):
        self._next = info['next']
        self._speed = info['level']
        self._score = info['score']
        self._lines = info['lines']

        if self._next is not None:
            self._next.drop()
            self._next.drop()
            self._next.right()
            self._next.right()
            

        
