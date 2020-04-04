"""File that defines the entry point and has the main loop.
"""
#import pdb
from collections import deque

import pygame

from modules.Figure import Figure
from modules.Field import Field
from modules.Timer import Timer
import modules.ControlLogic as control
import modules.MoveLogic as moveing
import tetris_conf as conf


pygame.init()
screen = pygame.display.set_mode((conf.SCREEN_WIDTH,
    conf.SCREEN_HEIGHT))
running = True

# timer used to count cycles until figure drops down on its own
timer = Timer(conf.TIME_MULT)
# timer used to count cycles until figure does user input on key held
timer_input_lag = Timer(200)
timer_input_slow = Timer(70)
# dictionary used to store commands from held down buttons
moves = {
    control.Moveset.IDLE: 0,
    control.Moveset.DOWN: 0,
    control.Moveset.LEFT: 0,
    control.Moveset.RIGHT: 0,
    control.Moveset.ROTATE: 0,
}
# playing field
field = Field(conf.WIDTH, conf.HEIGHT)
# generate first figure
fig = moveing.generate_new_figure(field.width)

### main loop ###
while running:
    for event in pygame.event.get():
        # imidiate reaction to keypresses processed here
        running, fig = control.process_input(event, fig, field)
        timer_input_lag.reset()

    # this dict is being used to process pressed and held keys
    moves = control.process_input_held(pygame.key.get_pressed())

    # timers
    timer.increment()
    timer_input_slow.increment()
    timer_input_lag.increment()

    if not timer.checks_out():
        timer.reset()
        fig = control.down_or_stop(field, fig)
    if not timer_input_lag.checks_out() and \
    not timer_input_slow.checks_out():
        timer_input_slow.reset()
        fig = control.move_figure(moves, fig, field)
    
    # drawing phase
    screen.fill(conf.BG_COLOR)
    fig.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    field.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    
    pygame.display.flip()
