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

# spawn a small sprite at the parents origin, and adds the sprite to the collection
def particle_spawn(parent, collection):
    newpart = gob.Entity(f"arrow",parent.loc, 1, collection, graphics=loadsprite('ARF','F',4),graphics_size=(111,19),lifetime = 24)
    newpart.cycle_len = 4

# moves entities (or entire collections of) according to a specific curve, along a specified direction
def particle_move(collection = "MAIN", curve_coefficient = 0, direction = "UP"):
    if (collection not in gob.Entity.collections) and (len(gob.Entity.collections) != 1): raise ValueError (f"Unknown collection '{collection}'")
    if direction not in ["UP","DOWN","LEFT","RIGHT"]: raise ValueError (f"Unknown direction '{direction}'")
    if curve_coefficient not in range(3): raise ValueError (f"Invalid curve_coefficient '{curve_coefficient}', should be 0, 1 or 2")

    for part in gob.entity_world:
        if (part.collection != collection) and (collection != "MAIN"): continue  # check the collection if required

        # so... turn out... the arrow sprite's are oriented like 'if they were shooting to the right'
        # thats an issue, cuz the rotation function assumes a 'if they were looking up' rotation as defealt
        # so we need to map the actual orientation of the sprite's head, to the expected orientation of the sprite's head
        # this means transform tables... yay... We should agree upon these kind of things, or coce a permanent, elagent solution for it...
        rot_dir_transform = {"UP":"LEFT", "DOWN":"RIGHT","LEFT":"DOWN","RIGHT":"UP"}
        rot_dir = rot_dir_transform[direction]
        rotate(part, rot_dir)
        if direction == "UP":
            move(part, x = 0, y = -2)
        if direction == "DOWN":
            move(part, x = 0, y = 2)
        if direction == "LEFT":
            move(part, x = -2, y = 0)
        if direction == "RIGHT":
            move(part, x = 2, y = 0)

def getgloballoc(entity):
    print(result)
    result = (entity.loc[0], entity.loc[1])
    return result

def move(entity, x=0, y=0):  # change location of an entity in direction of the movement keys, NOT bound by the screen edge
    entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y
    moved = True if (x,y) != (0,0) else False  # sets a variable to remember wether the move was succesfull

    if moved: entity.centerupdate()  # update entities center
    reset = True if not moved else False  # define wether to reset the animation cycle
    #print(f"move_screenbound: reset = {reset}")
    return (entity, reset)

def move_screenbound(entity, x=0, y=0):  # move the sprite opposite to the movement direction key, bound by screen bounds
    entity.loc[0] = entity.loc[0] - x*settings.player_speed  # change x
    entity.loc[1] = entity.loc[1] - y*settings.player_speed  # change y
    moved = True if (x,y) != (0,0) else False  # sets a variable to remember wether the move was succesfull

    # limit the movement to the screen size
    if (entity.loc[0] > 0) or (entity.loc[0] < -1*(entity.size[0]-settings.screen_size[0])):
        entity.loc[0] = entity.loc[0] + x*settings.player_speed  # change x back
        moved = False
    if (entity.loc[1] > 0) or (entity.loc[1] < -1*(entity.size[1]-settings.screen_size[1])):
        entity.loc[1] = entity.loc[1] + y*settings.player_speed  # change y back
        moved = False

    if moved: entity.centerupdate()  # update entities center
    reset = True if not moved else False  # define wether to reset the animation cycle
    #print(f"move_screenbound: reset = {reset}")
    return (entity, reset)

def rotate(entity, newdirection):
    angles = {"UP" : 0, "RIGHT" : -90, "DOWN" : 180, "LEFT" : 90}  # angle of the sprite, clockwise
    angle_start = angles[entity.direction]  # store the current direction as angle
    entity.direction = newdirection  # updtate the direction
    angle_new = angles[entity.direction]  # store the new direction as angle
    angle_dif = angle_new - angle_start  # compute the angle to rotate over, by computing the angle difference in direction
    if angle_dif == 0: return  # don't rotate if there is no direction change
    print(f"rotate: angle = {angle_dif}")
    for indx, sprite in enumerate(entity.graphics):
        #print(f"\trotating sprite {indx}. {sprite} ",end='...')
        entity.graphics[indx] = pg.transform.rotate(sprite, angle_dif)  # rotate the sprite to match new orientation
        #print("Complete!")

def draw(): # frame drawing
    screen.fill((255,0,255))  # removes all drawings
    screen.blit(background.graphics[0],(background.loc[0], background.loc[1]))  # draws background sprites
    for layer in range(settings.drawlayers, 0, -1): # draw layers
        for ent in gob.entity_world:
            if ent.layer == layer:
                #pg.draw.rect(screen, (255,0,0), pg.Rect(ent.loc[0], ent.loc[1], 60, 90))
                screen.blit(ent.graphics[ent.cycle_cur], (ent.loc[0],ent.loc[1]))
    pg.display.update() # send update to screen

def worldsprite_update(reset_ent = None):  # globally updates which sprite of cycles should be loaded
    # age cycle updates
    for ent in gob.entity_world:
        ent.age = ent.age+1  # increment age counter of all sprites
        if ent.lifetime:
            if ent.age > ent.lifetime: gob.entity_world.remove(ent)  # remove over aged sprites, I dont like old cheeses!

    # animation cycle updates
    if gob.game_world.frame == settings.spritespeed:
            for ent in gob.entity_world:
                if reset_ent:
                    #print(f"wsu:\n\tresetarg:{reset_ent}",end='\n')
                    reset = True if (reset_ent[0].name == ent.name) and reset_ent[1] else False
                ent.cycle_update(reset)

# (800-180, 350) < this works... but really shouldn't
# (800-72, 350-180) < this somehow doesnt work... but it should...

# window + program setup
pg.init()  # start pygame
screen = pg.display.set_mode(settings.screen_size)  # create the game's application screen, stored in the var 'screen'
player = gob.Entity('player', (800-180, 350), 1, "MAIN", graphics = loadsprite('WZ',"WC",7), graphics_size = (144,360)) # creates a new entity in the foreground
background = gob.Entity('background', (0,-350), 0, "MAIN", graphics = loadsprite('BG2'), graphics_size = (1600*2,1600*2))  # creates a background entity

# main loop
clock = pg.time.Clock()  # game clock, controls framerate
run = True  # controls wether the programs keeps running, or quits

while run:  # actual loop
    clock.tick(settings.fps) # run the loop at 'fps' times per second
    if gob.game_world.frame == settings.spritespeed: gob.game_world.frame = 0  # reset if >= animation speed
    gob.game_world.frame = gob.game_world.frame + 1  # increment the frame

    # events
    for event in pg.event.get():
        # quit button handling
        if event.type == pg.QUIT: run = False; print("Event: QUIT")
        # movement key handling
        pressed_keys = pg.key.get_pressed() # list of all keys that are pressed
        if pressed_keys[pg.K_UP]:  # checks wether up arrow was pressed
            move_y = -1  # set vertical movement sign to be negative (resulting in upward movement)
            rotate(player, "UP")  # rotate the player sprites to face up
        elif pressed_keys[pg.K_DOWN]:  # checks wether down arrow was pressed
            move_y = 1  # set vertical movement sign to be positive (== downward movement)
            rotate(player, "DOWN")  # rotate player sprites to face down
        else: move_y = 0  # if no vertical movement keys were pressed, multipy vertical movement by 0, so don't move up or down
        if pressed_keys[pg.K_LEFT]:  # checks wether left arrow was pressed
            move_x = -1
            rotate(player, "LEFT")
        elif pressed_keys[pg.K_RIGHT]:  # check wether right arrow was pressed
            move_x = 1
            rotate(player, "RIGHT")
        else: move_x = 0
        if move_x == 0 and move_y == 0:  # if the player is not moving...
            rotate(player, "UP")  # ...rotate the player to face up
        # mouse click handling
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if player.shoot():  # trigger the spawn of a projectile
                particle_spawn(player, "ARROW")
            player.fliptrigger()  # make sure that you can only fire once per mouseclick
        if event.type == pg.MOUSEBUTTONUP:
            player.fliptrigger()  # make sure that you can only fire once per mouseclick

    # entity calculating (movement, collisions, ect)
    worldsprite_update((player, move_screenbound(background, move_x, move_y)[1]))
    particle_move(collection = "ARROW", direction = player.direction)

    # screen update (clears prev draws, and draws the new data)
    draw()

pg.quit()
