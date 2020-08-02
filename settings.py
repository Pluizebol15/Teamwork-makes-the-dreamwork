'''
File containing all configurable attributes of the game


# window settings:
    screen_size   : size of window in pixels (pref 16:9 ratio)
    fps           : Frames Per Second to be drawn
    spritespeed   : Speed of the animation cycles (Nr of frames per sprite)
    cycle_len     : Defeault nr of sprites in one animation cycle
    drawlayers    : nr of layers to draw sprites on. Higher layers will appear on
                    top of lower layers. Layer nr 0 is the background layer.
# game settings:
    player_speed  : Nr of pixels the player moves per frame while walking
    part_speed    : Nr of pixels a particle moves per frame (Should be larger than player_speed)
'''

screen_size = (1600,900)
fps = 60
spritespeed = 3
cycle_len = 5
drawlayers = 2
player_speed = 15
part_speed = 50
