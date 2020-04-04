"""File that defines the entry point and has the main loop.
"""
#import pdb

import pygame

from modules.Figure import Figure
from modules.Field import Field
from modules.Timer import Timer
import modules.ControlLogic as control
import tetris_conf as conf


pygame.init()
screen = pygame.display.set_mode((conf.SCREEN_WIDTH,
    conf.SCREEN_HEIGHT))
running = True

# timer used to count cycles until figure drops down on its own
timer = Timer(conf.TIME_MULT)
# timer used to count cycles until figure does user input on key held
timer_input = Timer(150)
# playing field
field = Field(conf.WIDTH, conf.HEIGHT)
# test block
fig = control.generate_new_figure(field.width)

# main loop
while running:
    timer.increment()
    timer_input.increment()
    # user input catched here
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        if event.type == pygame.locals.KEYDOWN:
           running, fig = control.process_input(event.key, field, fig)

    # timers
    if not timer.checks_out():
        timer.reset()
        fig = control.down_or_stop(field, fig)
    if not timer_input.checks_out():
        timer_input.reset()
    
    # draw segment
    screen.fill(conf.BG_COLOR)
    fig.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    field.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    
    pygame.display.flip()
