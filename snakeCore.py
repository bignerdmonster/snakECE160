import pygame as pg
from menu import Menu
import random

#spawns apples randomly
class Apple:
    appleList = []
    def __init__(self):
        Apple.appleList.append(self)
        self.apple_size = 67
        self.x = random.randrange(0,980)
        self.y = random.randrange(0,620)
        self.color = (255,0,0)
        self.apple_but_rect = pg.Rect(self.x, self.y, self.apple_size, self.apple_size)
    
    def spawn(self, screen):
        pg.draw.rect(screen, self.color, self.apple_but_rect)
    
    @classmethod 
    def appleBlit(cls, screen):
        for individuApple in Apple.appleList:
            individuApple.spawn(screen)



class SnakeMat:
    def __init__(self, cols=15, rows=10):
        ### initalize the matrix. kinda duh-doy type stuff, but important regardless.
        self.center = [((cols + 1) // 2), ((rows + 1) // 2)]
        self.mat = [[None for place in range(cols)] for row in range(rows)]
    def __str__(self): # for debugging of doom and gloom
        retStr = ""
        for row in self.mat:
            retStr += ' '.join([str(elem) for elem in row]) + "\n"
        return retStr.strip()
    # i am dizzy. i will rest now. (ai told me to rest, i am "OBEYING" LAUGHING MY ASS OFF WTF) ### jacinthe's battle theme is REALLY good. 
    ## ok lets get real. Do I A: convert snakemat to pygame objects in the main game loop, or B: convert to printables et all in a fn., which is then called from the gameloop? I think the latter. also this theme SLAPS
    #def pgRender(self):
        ## ok so we want each value of the snakemat to be converted, but only valid ones. 
        

class Snake:
    def __init__(self, mat = SnakeMat(), **args): #PLEASE pass custompos as a 3 val array if it is being used.
        #basically, what if... ehh. how to 
        self.pos = mat.center[:].append(0) if (not ("startPos" in args.keys())) else args["startPos"] ## this is to create the POSSIBILITY of a third dimension
        self.direction = pg.Vector3(0,0,0) ##again, third dimension! because I want it. don't touch it tho.
        # ok how do I do this efficiently? 
        ## args for controls will be in the form controls = {'up': pg.K_UP, 'down': pg.K_DOWN, etc etc}
        if 'controls' in args.keys():
            self.up = args['controls']['up'] 
            self.down = args['controls']['down']
            self.left = args['controls']['left']
            self.right = args['controls']['right']
        else:
            self.up = pg.K_w
            self.down = pg.K_s
            self.left = pg.K_a
            self.right = pg.K_d

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

pg.init()
screen = pg.display.set_mode((1080,720), pg.SCALED, vsync=1)
apple = Apple()
print("bkpoint")
def snakeGame(menu = Menu(screenInp=screen)): ## this is the actual main game loop function!! yay
    #apple_exist = False
    run = True
    while run:
        screen.fill('black')
        ## and Corbeau's theme slaps too zawg.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            Apple()
        if keys[pg.K_s]:
            Apple.appleList.clear()
        if keys[pg.K_ESCAPE]:
            run=False
        #if not apple_exist:
        #    Apple()
        #    apple_exist = True 
        Apple.appleBlit(screen)
       
        
        
        pg.display.flip()
        clock.tick(framerate)
    menu.notstop = True




if __name__ == "__main__":

    mainMat = SnakeMat()
    mainSnake = Snake(mainMat)
    apple = Apple()
    clock = pg.time.Clock()

    framerate = 15
    mainMenu = Menu(screenInp=screen, start_game=None, clocked=clock) #testing w/ start-game = none
    while True:
        mainMenu.run()
        snakeGame(mainMenu)
else:
    print("snakeCore imported, or YOU SHOULD RUN THIS WITH python3 snakeCore.py")