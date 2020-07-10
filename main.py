import pygame as pg
import settings
import game_objects as gob
from os import getcwd

# operation defenitions (like drawing frames, calculating movement, ect)

def loadsprite(EntityPreFx, direction, cycletype=None, cyclelen=None):
    # loadsprite loads images to use, and groups them for animation-cycles
    # return either one image in list, or a tuple with the direction and image sequence
    if cyclelen and cycletype:
        returnlist = []  # list with loaded images to return
        for n in range(cyclelen):
            print(f"Loading {EntityPreFx}_{cycletype}_{direction}_{n}...",end='')
            try:
                returnlist.append(pg.image.load(f".\{EntityPreFx}_{cycletype}_{direction}_{n}.png"))
                print("Complete!")
            except pg.error: print("FAILED"); pg.quit(); raise  # quit on error
        return (direction, returnlist)
    else: return ("UP", [pg.image.load(f".\{EntityPreFx}_{direction}.png")])

def move(entity, x=0, y=0):  # change location of an entity
    entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y
    entity.centerupdate()  # update entities center

def move_screenbound(entity, x=0, y=0):  # move the background sprite in opposite direction to fake movement
    entity.loc[0] = entity.loc[0] - x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] - y*settings.player_speed  # change y
    moved = True  # sets a variable to remember wether the move was succesfull
    entity.centerupdate()  # update entities center

    if (entity.loc[0] > 0) or (entity.loc[0] < -1*(entity.size[0]-settings.screen_size[0])):
        entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x back
        moved = False
    if (entity.loc[1] > 0) or (entity.loc[1] < -1*(entity.size[1]-settings.screen_size[1])):
        entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y back
        moved = False

    if moved: player.cycle_update()  # update which sprite to render in animation cycle
    else: player.cycle_cur = 0  # reset animation cycle if player didn't move

def draw(): # frame drawing
    screen.fill((255,0,255))  # removes all drawings
    screen.blit(background.graphics["UP"][0],(background.loc[0], background.loc[1]))  # draws background sprites
    for layer in range(settings.drawlayers, 0, -1): # draw layers
        for ent in gob.entity_world:
            if ent.layer == layer:
                #pg.draw.rect(screen, (255,0,0), pg.Rect(ent.loc[0], ent.loc[1], 60, 90))
                screen.blit(ent.graphics[ent.direction][ent.cycle_cur], (ent.loc[0],ent.loc[1]))
    pg.display.update() # send update to screen


# window + program setup
pg.init()  # start pygame
screen = pg.display.set_mode(settings.screen_size)
player = gob.newentity('player', (800-72, 350+72), 1, graphics_size = (144,360)) # creates a new entity in the foreground
for indx, direction in enumerate(player.graphics.keys()):
    print(f"assigning images to direction: graphics[{indx}]: {direction}...",end='')
    player.graphics[direction] = loadsprite('P',direction,"WC",player.cycle_len)[1]
    print("Complete!")

print(player.graphics)
background = gob.newentity('background', (0,-350), 0, graphics_size = (1600*2,1600*2))  # creates a background entity
background.graphics["UP"] = loadsprite('BG2', "UP")[1]  # loads the singe sprite list into the 'up' graphics slot

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
        if move_x == 0 and move_y == 0: player.direction = "UP"

    # entity calculating (movement, collisions, ect)
    move_screenbound(background, move_x, move_y)

    # screen update (clears prev draws, and draws the new data)
    draw()

pg.quit()
