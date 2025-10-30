import pygame as pg
pg.init()
screen = pg.display.set_mode((1080,720), pg.SCALED, vsync=1)
clock = pg.time.Clock()
framerate = 15
running = True

class SnakeMat:
    def __init__(self, cols=15, rows=10):
        ### initalize the matrix. kinda duh-doy type stuff, but important regardless.
        self.center = [((cols + 1) // 2), ((rows + 1) // 2)]
        self.mat = [[0 for place in range(cols)] for row in range(rows)]
        

class Snake:
    def __init__(self, mat = SnakeMat(), **args): #PLEASE pass custompos as a 3 val array if it is being used.
        #basically, what if... ehh. how to 
        self.pos = mat.center[:].append(0) if (not args["startPos"]) else args["startPos"] ## this is to create the POSSIBILITY of a third dimension
        self.direction = pg.Vector3(0,0,0) ##again, third dimension! because I want it. don't touch it tho.
        # ok how do I do this efficiently? 
        ## args for controls will be in the form controls = {'up': pg.K_UP, 'down': pg.K_DOWN, etc etc}
        if args['controls']:
            self.up = args['controls']['up'] 
            self.down = args['controls']['down']
            self.left = args['controls']['left']
            self.right = args['controls']['right']
        else:
            self.up = pg.K_UP
            self.down = pg.K_DOWN
            self.left = pg.K_LEFT
            self.right = pg.K_RIGHT
#print(snakeMat) -- i could make this a class... ehhhhh 
            
## ok how to snake it --
### what we're gonna do is define the surface as a like 15x10 grid of things
### then have the player start at the center of it, and go... right??? ok 
### so like lets do that first -- done as of 8:04 pm 10/29
## OK
### NOW WE MAKE CONTROLS
#### so basically like i want these guys to have custom controls. -- done
### now, i should really make the actual snake OR ANYTHING THAT WORKS. buuuuuuut
### ok some psuedocode to figure out logic:

## for the first stage, we just need to make basic snake. that means 4 cardinal directions,
## and you shouldn't be able to like... go in the oppisite direction. but that has more logic to it
### OH IS THIS IMPLEMENTED IN PYGAME ALREADY -- it IS 
mainMat = SnakeMat()
mainSnake = Snake(mainMat)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill('black')
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        screen.fill('yellow')
    pg.display.flip()
    clock.tick(framerate)