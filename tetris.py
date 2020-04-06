"""File that defines the entry point and has the main loop.
"""
#import pdb
from collections import deque

import pygame


from modules.Game import Tetris #, InfoPanel  # planned
from modules.Figure import Figure
from modules.Field import Field
from modules.Timer import Counter
import modules.ControlLogic as control
import modules.MoveLogic as moveing
import tetris_conf as conf


pygame.init()

display = pygame.display.set_mode((conf.SCREEN_WIDTH,
    conf.SCREEN_HEIGHT))
running = True

game = Tetris(conf.TEST)
#info = Info()
"""
########################################################################
#                       Currently being tested to replace this code
########################################################################

# timer used to count cycles until figure drops down on its own
timer = Counter(conf.TIME_MULT)
# timer used to count cycles until figure does user input on key held
timer_input_lag = Counter(200)
timer_input_slow = Counter(70)
timer_lines_flash = Counter(50)
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
"""

### main loop ###
while running:

    game.process_input(pygame.event.get())
    #game.process_input_held(pygame.key.get_pressed())  # not tested at this itteration
    
    # tick
    if not game.paused:
        game.tick()  # increase timers, drop figure, process inputs,
                     # check full lines, flush full lines, increase Score,
                     # Lines, Speed
    else:
        game.tick_paused()  # this is planned to be used to flash full lines while game logic is on pause

    # update info for info pannel
    #info.update(game.info_update())  # return (next figure, score, lines, speed)
    
    game_panel = game.draw()  # a pygame Surface object returned
    #info_panel = info.draw()  # a pygame Surface object returned

    display.fill(conf.BG_COLOR)
    display.blit(game_panel, (0,0))
    #display.blit(info_panel, (info_panel coords))

    pygame.display.update()
    running = game.is_active

    """
    ####################################################################
    #                       Currently being tested to replace this code
    ####################################################################

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
    timer_lines_flash.increment()

    if not timer.checks_out():
        timer.reset()
        fig = control.down_or_stop(field, fig)
    if not timer_input_lag.checks_out() and \
    not timer_input_slow.checks_out():
        timer_input_slow.reset()
        fig = control.move_figure(moves, fig, field)
    
    lines_cleared = field.check_full_lines()
    field.flash_lines(lines_cleared, timer_lines_flash)

    # drawing phase
    screen.fill(conf.BG_COLOR)
    fig.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    field.draw(screen, conf.COLORS, conf.CELL_WIDTH)
    
    pygame.display.flip()
    """
