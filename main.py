import pygame as pg
import settings
import game_objects as gob
from os import getcwd

# operation defenitions (like drawing frames, calculating movement, ect)

def loadsprite(EntityLetter, cycletype=None, cyclelen=None):
    # loadsprite loads images to use, and groups them for animation-cycles
    # return either one image in list, or a list of subsequent images
    if cyclelen and cycletype:
        returnlist = []  # list with loaded images to return
        for n in range(cyclelen):
            print(f"Loading {EntityLetter}_{cycletype}_{n}...",end=' ')
            try:
                returnlist.append(pg.image.load(f".\Graphics\{EntityLetter}_{cycletype}_{n}.png"))
                print("Complete!")
            except pg.error: print("FAILED  <--"); pg.quit(); raise  # quit on error
        return returnlist
    else: return [pg.image.load(f".\Graphics\{EntityLetter}.png")]

def move(entity, x=0, y=0):  # change location of an entity
    # THIS function IS NOT FUNCTIONAL ==> USE MOVE_SCREENBOUND FOR NOW
    entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y
    entity.centerupdate()  # update entities center

def move_screenbound(entity, x=0, y=0):  # move the background sprite in opposite direction to fake movement
    entity.loc[0] = entity.loc[0] - x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] - y*settings.player_speed  # change y
    moved = True if (x,y) != (0,0) else False  # sets a variable to remember wether the move was succesfull
    if moved: entity.centerupdate()  # update entities center

    if (entity.loc[0] > 0) or (entity.loc[0] < -1*(entity.size[0]-settings.screen_size[0])):
        entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x back
        moved = False
    if (entity.loc[1] > 0) or (entity.loc[1] < -1*(entity.size[1]-settings.screen_size[1])):
        entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y back
        moved = False
    #print(f"moved: {moved}")
    if moved:
        if gob.game_world.frame == 3: player.cycle_update()  # update which sprite to render in animation cycle
    else: player.cycle_cur = 0  # reset animation cycle if player didn't move

def draw(): # frame drawing
    screen.fill((255,0,255))  # removes all drawings
    screen.blit(background.graphics[0],(background.loc[0], background.loc[1]))  # draws background sprites
    for layer in range(settings.drawlayers, 0, -1): # draw layers
        for ent in gob.entity_world:
            if ent.layer == layer:
                #pg.draw.rect(screen, (255,0,0), pg.Rect(ent.loc[0], ent.loc[1], 60, 90))
                screen.blit(ent.graphics[ent.cycle_cur], (ent.loc[0],ent.loc[1]))
    pg.display.update() # send update to screen


# window + program setup
pg.init()  # start pygame
gob.game_world.frame = 0  # add an attribute called 'frame' to the world, which keeps track on which point in the animation cycles the world is
screen = pg.display.set_mode(settings.screen_size)  # create the game's application screen, stored in the var 'screen'
player = gob.newentity('player', (800-72, 350+72), 1, graphics = loadsprite('P',"WC",9), graphics_size = (144,360)) # creates a new entity in the foreground
background = gob.newentity('background', (0,-350), 0, graphics = loadsprite('BG2'), graphics_size = (1600*2,1600*2))  # creates a background entity

# main loop
clock = pg.time.Clock()  # game clock, controls framerate
run = True  # controls wether the programs keeps running, or quits

while run:  # actual loop
    clock.tick(settings.fps) # run the loop at 'fps' times per second
    if gob.game_world.frame == settings.spritespeed: gob.game_world.frame = 0  # reset if >= animation speed
    gob.game_world.frame = gob.game_world.frame + 1  # increment the frame

    # events
    for event in pg.event.get():
        # quit button
        if event.type == pg.QUIT: run = False; print("Event: QUIT")
        # movement keys
        pressed_keys = pg.key.get_pressed() # list of all keys that are pressed
        if pressed_keys[pg.K_UP]:
            move_y = -1
            player.direction = "UP"
        elif pressed_keys[pg.K_DOWN]:
            move_y = 1
            player.direction = "UP"
        else: move_y = 0
        if pressed_keys[pg.K_LEFT]:
            move_x = -1
            player.direction = "LEFT"
        elif pressed_keys[pg.K_RIGHT]:
            move_x = 1
            player.direction = "RIGHT"
        else: move_x = 0
        if move_x == 0 and move_y == 0:
            player.direction = "UP"

    # entity calculating (movement, collisions, ect)
    move_screenbound(background, move_x, move_y)

    # screen update (clears prev draws, and draws the new data)
    draw()

pg.quit()
