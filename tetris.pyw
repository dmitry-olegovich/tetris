"""File that defines the entry point and has the main loop.
"""
import pygame

from modules.Game import Tetris
from modules.Info import InfoPanel
from modules.Figure import Figure
from modules.Field import Field
from modules.Timer import Counter
import tetris_conf as conf


pygame.init()

y_margin = conf.GAME['cell_width']
game_panel_coords = (y_margin, y_margin)
info_panel_coords = (y_margin*2 + conf.SCREEN_WIDTH, y_margin)
display = pygame.display.set_mode((conf.SCREEN_WIDTH*2,
    conf.SCREEN_HEIGHT + y_margin*2))

running = True

clock = pygame.time.Clock()
game = Tetris(conf.GAME)
info = InfoPanel(conf.GAME)

### main loop ###
while running:
    game.process_input(pygame.event.get())
    game.process_input_held(pygame.key.get_pressed())  # held keys are processed with delay
    
    # tick
    if not game.paused:
        game.tick()  # increase timers, drop figure, process inputs,
                     # check full lines, flush full lines, increase Score,
                     # Lines, Speed
        pygame.display.set_caption('PyTetris')
    else:
        game.tick_paused()  # this is planned to be used to flash full lines while game logic is on pause
        pygame.display.set_caption('PyTetris (Paused)')

    # update info for info pannel
    info.update(game.info_update())
    
    game_panel = game.draw()  # a pygame Surface object returned
    info_panel = info.draw()  # a pygame Surface object returned

    display.fill(conf.IF_COLOR)
    display.blit(game_panel, game_panel_coords)
    display.blit(info_panel, info_panel_coords)

    pygame.display.update()
    running = game.is_active
    if not running:
        print(f"***DEBUG*** GAME OVER! Score: {game.score}")  # DEBUG
    clock.tick(conf.GAME['FPS_limit'])