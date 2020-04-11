""" This module provides a Tetris class - all that is going on in the 
Tetris game screen, i.e. the the game field with falling figures.
"""
import pdb

import pygame
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
from .Timer import Counter

class Tetris():
    """Describes the Tetris game screen with all of it's objects.
    
    Args:
        config (dict): a dictionary that must contain keys:
            'cell_width': (int) width of single cell in px,
            'width': (int) width of field in num of cells,
            'height': (int) height of field in num of cells,
            'turn_cycles': (int) number of ticks for a turn on speed 1,
            'palette': a list of colors set as (r,g,b) tuples,
            'speed': (int) initial game speed

    Attributes:
        _canvas (pygame.Surface): the canvas on which to draw figures;
        _timer (Timer.Counter): main counter;
        _moves (dict): a dict of moves from held keys;
        _field (Field.Field): the game field;
        _figure (Figure.Figure): current figure on the field under 
            players control;
        _next (Figure.Figure): generated random next figure to drop;
        _score (int): current score;
        _lines (int): current total removed lines;
        _speed (int): current game speed;
        _pause (bool): game logic paused if True;
        _active (bool): quit game if False;
        _screen_res (tuple of int): drawing area size in px;
        _palette (list): list of used colors - (r,g,b) tuples.

    """

    _hold_key_speed_lag = 2  # move figure if keyheld every X ticks
    _held_key_input_lag = 5  # after first move, X ticks lag on key held
    _lines_num_speed_up = 4  # increase speed every X lines
    
    def __init__(self, config: dict):
        self._field = Field(config['width'], config['height'])
        self._figure = Figure(0,0,0)
        self._next = Figure(0,0,0)
        self._score = 0
        self._lines = 0
        self._speed = config['speed']
        self._config = dict(config)
        self._moves = {
            K_DOWN: None,
            K_RIGHT: None,
            K_LEFT: None,
        }
        self._screen_res = (config['cell_width']*self._field.width,
            config['cell_width']*self._field.height)
        self._pause = False
        self._active = True
        self._palette = config['palette'][:]
        # swap random figures instead of default ones
        self._next = self._generate_new_figure()
        self._next = self._generate_new_figure()
        self._moves_keys = self._moves.keys()
        self._timer = Counter(self._calc_turn_ticks())
        self._lines_since_lvl_up = 0

    @property
    def width(self):
        return self._field.width
    
    @property
    def height(self):
        return self._field.height

    @property
    def paused(self):
        return True if self._pause else False

    @property
    def is_active(self):
        return self._active
    
    @property
    def score(self):
        return self._score

    def process_input(self, events: list):
        """Process input events out of passed pygame events."""

        for event in events:
            self._process_event(event)
    
    def _process_event(self, event: pygame.event.Event):
        """Process a single pygame event."""

        if event.type == QUIT:
            self._active = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self._active = False
            if event.key == K_DOWN:
                self._down_or_stop()
            elif event.key == K_LEFT:
                self._left_or_not()
            elif event.key == K_RIGHT:
                self._right_or_not()
            elif event.key == K_UP:
                self._rotate_or_not()

    def process_input_held(self, pressed_list):
        """Process held keys passed in pressed_list - list of 0/1 w/
        indexes values corresponding to pygame.locals definitions."""

        for key in self._moves_keys:
            if pressed_list[key] == 0:
                self._moves[key] = None
            if pressed_list[key] == 1 and self._moves[key] is None:
                self._moves[key] = Counter(self._held_key_input_lag)
    
    def tick(self):
        """Make a game logic tick."""

        # make moves if needed for held down keys
        for key in self._moves_keys:
            if self._moves[key] is None:
                continue
            self._moves[key].increment()
            if not self._moves[key].checks_out():
                # drop timer from input lag to move slowdown value
                self._moves[key] = Counter(self._hold_key_speed_lag)
                # now make a move
                getattr(self, Moveset.moves[key]) ()
        
        self._timer.increment()
        if not self._timer.checks_out():
            self._timer.reset()
            self._down_or_stop()
        
        
        lines_full = self._field.check_full_lines()
        self._update_info(lines_full)
        self._field.flash_lines(lines_full)

    def tick_paused(self):
        """Make a time tick without game logic tick."""
        
        # not implemented yet
        pass

    def info_update(self):
        """Return a dict with updated game info for Info class method."""

        info = {
            'score': self._score,
            'lines': self._lines,
            'level': self._speed,
        }

        if self._next is None:
            info['next'] = None
        else:
            info['next'] = self._next.copy()

        return info

    def draw(self):
        """Return a pygame.Surface object with figure and field cell."""

        surface = pygame.Surface(self._screen_res)
        surface.fill(self._config['palette'][0])

        self._figure.draw(surface, self._config['palette'],
            self._config['cell_width'])
        self._field.draw(surface, self._config['palette'],
            self._config['cell_width'])

        return surface
    
    def _idle(self):
        pass

    def _down_or_stop(self):
        """Drop figure if no field cells in the way."""
        if self._field.check_down(self._figure):
            self._figure.drop()
        else:
            self._active = self._field.grow(self._figure)
            self._generate_new_figure()

    def _left_or_not(self):
        """Move figure left if no field cells in the way."""

        if self._field.check_left(self._figure):
            self._figure.left()

    def _right_or_not(self):
        """Move figure right if no field cells in the way."""

        if self._field.check_right(self._figure):
            self._figure.right()

    def _rotate_or_not(self):
        """Rotate figure if it won't intersect with field after."""

        if self._field.check_rotation(self._figure):
            self._figure.rotate()

    def _generate_new_figure(self):
        """Push current next figure to being current figure and generate
        new random figure postitioned at the top of the game-screen.
        """
        width = self.width
        code = randrange(0, len(Figure._FIGURES))
        if self._next:
            self._figure = self._next
        else:
            code = randrange(0, len(Figure._FIGURES))
            self._figure = Figure(code, x=int(width/2) - 1, y=0)
        self._next = Figure(code, x=int(width/2) - 1, y=0)

    
    def _move_figure(self):
        """Move figure based on moves input via held down keys."""

        for key in self._moves:
            if self._moves[key]:
                getattr(self, Moveset.moves[key]) ()

    def _update_info(self, lines:list):
        """Update score, level, lines records.
        Called every tick.
        """
        score = 1
        for line in lines:
            self._score += score
            score *= 2

        self._lines += len(lines)
        self._lines_since_lvl_up += len(lines)
        if self._check_speed_increase():
            self._lines_since_lvl_up = 0
            self._speed += 1
            cycles = self._config['turn_cycles']
            self._timer = Counter(self._calc_turn_ticks())

    def _check_speed_increase(self):
        """Return True every 4 self._lines."""

        if self._lines_since_lvl_up // self._lines_num_speed_up >= 1:
            return True
      
        return False

    def _calc_turn_ticks(self):
        """Return calculated ticks per turn."""

        return self._config['turn_cycles'] * self._exp(self._speed)
    
    @staticmethod
    def _exp(number):
        """Formula used to calculate ticks per turn depending on speed.
        
        At number = 1 roughly = 1, at 10 roughly = 0.18
        """
        c = 0.585
        k = 0.3

        return c * (2.71 ** (1 / (k*(number - 1) + 1)) - 1) 

        
class Moveset():
    """Defines a number of constants for processing moves."""
    
    moves = {
            K_DOWN: '_down_or_stop',
            K_RIGHT: '_right_or_not',
            K_LEFT: '_left_or_not',
    }
