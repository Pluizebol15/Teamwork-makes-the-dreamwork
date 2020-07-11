'''
Game structure:
- The game state is saved in a 'world' class
    - world contains things like:
        - triggers
        - events
        - lighting (???)
        - globally needed atributes (eg. sprite states)
        - interactables information
    - world gets referenced if 2 entities need to interact with each other (outside collisions),
      or need information on each other, not obtainable otherwise.
- All things shown on screen are an 'entity'
    - Entities have attributes allowing them to be drawn
    - Entities may exist offscreen
    - Entities may have a lifetime, after which they may not be drawn again and
      will be removed
- All collidable entities are called 'collision objects'
    - collision objects belong to the 'collisob' class
    - collision objects collide with each other and the screen

Organisation:
- All entities are stored in 'entity_world', which is drawn to the screen, and
  updated every tick, sorted by age.
- All collision objects are stored in 'collision_world', which is updated and
checked for collisions every tick

'''

entity_world = []     # collection of all entities, sorted by age (descending)
collision_world = []  # collection of all collision objects, unsorted

# class that stores information needed for entity interactions and dependency
# NOTE: attributes are assigned as needed, and removed as needed, please manage this manually!
# NOTE2: only ONE instance of this class should exists: 'game_world'!!!!
class world:
    pass
game_world = world()
# class that contains neccecary information to draw something on the screen
class entity:
    def __init__(self, name, location, layer, graphics=[None], graphics_size=None, lifetime=None):
        if graphics and not graphics_size: raise ValueError ("graphics specified but no size was given!")
        self.name = name  # name of the entity
        self.loc = [location[0], location[1]]  # coördinates of the entity [x, y]
        self.direction = "UP"  # facing direction of the entity, defealt to up
        self.center = [location[0]+graphics_size[0]/2, location[1]+graphics_size[1]/2]  # center of the entity
        self.size = (graphics_size[0], graphics_size[1])  # size of the graphics images in forward position
        self.graphics = graphics  # optional list of spites for animation/drawing
        self.age = None # integer nr of frames since the object appeared on the screen
        self.cycle_cur = 0  # frame in an optional cycle that should be drawn
        self.cycle_len = 9  # length of the optional cycle that should be drawn (defealt 9)
        self.lifetime = lifetime # nr of maximum frames the object is allowed to appear
        self.layer = layer  # draw layer the sprite should be drawn to.

    def centerupdate(self):  # updates the center of image attribute of the entity
        self.center = [self.loc[0] + self.size[0]/2, self.loc[1] + self.size[1]/2]  # updates center of the entity

    def cycle_update(self):  # updates any cycles present in the entity attributes
        if self.cycle_cur+1 >= self.cycle_len: self.cycle_cur = 0
        else: self.cycle_cur = self.cycle_cur+1

# entity class that has collision bounds
class collisob(entity):
    def __init__(self, name, location, layer, size, graphics=None,graphics_size=None, lifetime=None):
        super.__init__(self, name, location, layer, graphics, lifetime)
        self.coll = [  # collision points for the object (corners, clockwise)
            self.loc,  # left upper corner (== coördinates)
            (self.loc[0]+size[0], self.loc[1]),  # right upper corner
            (self.loc[0]+size[0], self.loc[1]+size[1]),  # right lower corner
            (self.loc[0], self.loc[1]+size[1])  # left lower corner
        ]

def newentity(name, location, layer, graphics=[None], graphics_size=None, lifetime=None):
    global entity_world
    newitem = entity(name, location, layer, graphics, graphics_size, lifetime)  # create new entity
    entity_world.append(newitem)  # append entity to world
    return newitem

if __name__ == '__main__':
    ent1 = newentity('ent1',(0,0), 1)
    print(f"world: {entity_world}")
    for ent in entity_world:
        print(f"  {ent.name}  '{ent.age}'")
    ent1.age = 30
    ent2 = newentity('ent2',(30,0), 1)
    ent2.age = 20
    print(f"world: {entity_world}")
    for ent in entity_world:
        print(f"  {ent.name}  '{ent.age}'")
