"""File that defines the entry point and has the main loop.
"""
#import pdb

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from modules.TetrisObjects import Figure
from modules.StaticObjects import Field
import modules.TetrisFunctions as aux
import tetris_conf as conf


pygame.init()
screen = pygame.display.set_mode((conf.SCREEN_WIDTH,
    conf.SCREEN_HEIGHT))
running = True

# timer used to count cycles until figure drops down on its own
timer = 0
# playing field
field = Field(conf.WIDTH, conf.HEIGHT)
# test block
fig = aux.generate_new_figure(field.width)

# main loop
while running:
    timer +=1
    # user input catched here
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_DOWN:
                fig = aux.down_or_stop(field, fig)
            if event.key == K_LEFT:
                aux.left_or_not(field, fig)
            if event.key == K_RIGHT:
                aux.right_or_not(field, fig)
            if event.key == K_UP:
                aux.rotate_or_not(field, fig)

    # timer
    if timer == conf.TIME_MULT:
        #pdb.set_trace()
        timer = 0
        fig = aux.down_or_stop(field, fig)
        #pdb.set_trace()
    
    # draw segment
    screen.fill(conf.BG_COLOR)
    fig.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    field.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    
    pygame.display.flip()
