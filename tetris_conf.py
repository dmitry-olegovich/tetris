BG_COLOR = (10, 10, 10)
IF_COLOR = (80, 80 , 80)

GAME = {
    'cell_width': 20,
    'width': 10,
    'height': 20,
    'turn_cycles': 40,
    'palette': [
        BG_COLOR,           # index = 0 - dark grey
        (200, 0, 0),        # index = 1 - red
        (0, 200, 0),        # index = 2 - green
        (160, 82, 45),      # index = 3 - brown
        (200, 130, 0),      # index = 4 - orange
        (0, 0, 200),        # index = 5 - blue
        (0, 200, 200),      # index = 6 - yellow
        (200, 200, 200),    # index = 7 - white
    ],
    'speed': 1,
    'FPS_limit': 40,
}

SCREEN_WIDTH = GAME['width'] * GAME['cell_width']
SCREEN_HEIGHT = GAME['height'] * GAME['cell_width']
