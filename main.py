import pygame as pg
import settings
import game_objects as gob

# window + program setup
pg.init()  # start pygame
screen = pg.display.set_mode(settings.screen_size)
player = gob.newentity('player', (800-72, 350+72), 1, graphics = pg.image.load(r"./PS3.png"), graphics_size = (144,144)) # creates a new entity in the foreground
background = gob.newentity('background', (0,-350), 0, graphics = pg.image.load(r"./bg2.png"), graphics_size = (1600*2,1600*2))  # creates a background entity


# operation defenitions (like drawing frames, calculating movement, ect)

def move(entity, x=0, y=0):  # change location of an entity
    entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y
    entity.centerupdate()  # update entities center

def move_screenbound(entity, x=0, y=0):  # move the background sprite in opposite direction to fake movement
    entity.loc[0] = entity.loc[0] - x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] - y*settings.player_speed  # change y
    entity.centerupdate()  # update entities center
    if (entity.loc[0] > 0) or (entity.loc[0] < -1*(entity.size[0]-settings.screen_size[0])):
        entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x back
    if (entity.loc[1] > 0) or (entity.loc[1] < -1*(entity.size[1]-settings.screen_size[1])):
        entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y back

def draw(): # frame drawing
    screen.fill((255,0,255))  # removes all drawings
    screen.blit(background.graphics,(background.loc[0], background.loc[1]))  # draws background sprites
    for layer in range(settings.drawlayers, 0, -1): # draw layers
        for ent in gob.entity_world:
            if ent.layer == layer:
                #pg.draw.rect(screen, (255,0,0), pg.Rect(ent.loc[0], ent.loc[1], 60, 90))
                screen.blit(ent.graphics, (ent.loc[0],ent.loc[1]))
    pg.display.update() # send update to screen


# main loop
clock = pg.time.Clock()  # game clock, controls framerate
run = True  # controls wether the programs keeps running, or quits

while run:  # actual loop
    clock.tick(settings.fps) # run the loop at 'fps' times per second

    # events
    for event in pg.event.get():
        # quit button
        if event.type == pg.QUIT: run = False; print("Event: QUIT")
        # movement keys
        pressed_keys = pg.key.get_pressed() # list of all keys that are pressed
        if pressed_keys[pg.K_UP]:
            move_y = -1
        elif pressed_keys[pg.K_DOWN]:
            move_y = 1
        else: move_y = 0
        if pressed_keys[pg.K_LEFT]:
            move_x = -1
        elif pressed_keys[pg.K_RIGHT]:
            move_x = 1
        else: move_x = 0

    # entity calculating (movement, collisions, ect)
    move_screenbound(background, move_x, move_y)

    # screen update (clears prev draws, and draws the new data)
    draw()

pg.quit()
