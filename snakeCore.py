import pygame as pg
from menu import Menu
import random

#spawns apples randomly
class Apple:
    appleList = []
    def __init__(self):
        Apple.appleList.append(self)
        self.apple_size = 50
        self.x = random.randrange(0,980)
        self.y = random.randrange(0,620)
        self.color = (255,0,0)
        self.apple_but_rect = pg.Rect(self.x, self.y, self.apple_size, self.apple_size)
    
    def spawn(self, screen):
        pg.draw.rect(screen, self.color, self.apple_but_rect)
    #there's gotta be a better way to check collision
    def checkCollision(self, snake):
        snek = pg.Rect(snake.hPos[0] * 50, snake.hPos[1] * 50, 50, 50)
        return self.apple_but_rect.colliderect(snek)
    @classmethod 
    def appleBlit(cls, screen):
        for individuApple in Apple.appleList:
            individuApple.spawn(screen)



class SnakeMat:
    def __init__(self, cols=15, rows=11):
        ### initalize the matrix. kinda duh-doy type stuff, but important regardless.
        self.cols = cols
        self.rows = rows
        self.center = [(cols // 2), (rows // 2)]
        self.mat = [[0 for place in range(cols)] for row in range(rows)]
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
    soleSnake = ["how recursive do we have to get"]
    def __init__(self, sMat = SnakeMat(), **args): #PLEASE pass custompos as a 3 val array if it is being used.
        Snake.soleSnake[0]=self
        #basically, what if... ehh. how to 
        self.hPos = sMat.center[:] if (not ("startPos" in args.keys())) else args["startPos"] ## this is to create the POSSIBILITY of a third dimension
        self.hPos.append(0) if len(self.hPos) == 2 else 1
        self.pos = [self.hPos[:]] # what I want is for self.pos to work like this: first, it only has self.hPos (as that's the only position). Then, it has first the old self.hPos, then a new self.hPos incremented by the motion vector, so that the snake moves... hm 
       
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
        # tfw the team flare noveau STOP MAKING SNAKE PUNS CLANKER sigh theme slaps so hard
        self.sMat = sMat
        sMat.mat[self.hPos[0]][self.hPos[1]] = 2 ## 2 is the snake's head. the AI is mimicking my style. this is black mirror to an extent which i find strange.
        self.len = 1  # length of snake; used to determine when to pop tail
        # is that it?
    def move(self):
        self.hPos[0] = (self.hPos[0] + int(self.direction.x)) % self.sMat.cols; self.hPos[1] = (self.hPos[1] + int(self.direction.y)) % self.sMat.rows; self.hPos[2] += int(self.direction.z) # increment head position by direction vector
        # modulo to keep the snake from throwing index errors
        self.pos.insert(0, self.hPos[:]) ## insert the new head position at the start of the list, allowing for head to remain constant... 0, 1 0, 2 1 0, etc
        if len(self.pos) > self.len: # you can undertand this one
            self.pos.pop() ## remove tail 
            # simple enough!
    def steer(self, keys):
        if keys[self.up]:
            self.direction = pg.Vector3(0,-1,0)
        elif keys[self.down]:
            self.direction = pg.Vector3(0,1,0)
        elif keys[self.left]:
            self.direction = pg.Vector3(-1,0,0)
        elif keys[self.right]:
            self.direction = pg.Vector3(1,0,0)
        else:
            pass # I think this is needed... try check
    def printSnake(self):
        snek = pg.Rect(self.hPos[0] * 50, self.hPos[1] * 50, 50, 50)
        pg.draw.rect(screen, color=('Green'), rect=snek)

    def __str__(self):
       
        retStr = ""
        tempMat = [[0 for place in range(self.sMat.cols)] for row in range(self.sMat.rows)]
        for i, segment in enumerate(self.pos):
            print(segment)
            if i == 0:
                tempMat[segment[1]][segment[0]] = 2 # head
            else:
                tempMat[segment[1]][segment[0]] = 1 # body  
            # holy jank
        for row in tempMat:
            retStr += ' '.join([str(elem) for elem in row]) + "\n"
        return retStr



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
SNAKE_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SNAKE_EVENT, 1000) # every 1 ms, the snake allegedly moves.
screen = pg.display.set_mode((1080,720), pg.SCALED, vsync=1)
apple = Apple()
print("bkpoint")
def snakeGame(menu = Menu(screenInp=screen), snake=Snake(SnakeMat())): ## this is the actual main game loop function!! yay
    #apple_exist = False
    run = True
    while run:
        screen.fill('black')
        mainSnake.printSnake()
        ## and Corbeau's theme slaps too zawg.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            if event.type == SNAKE_EVENT:
                snake.move()
                print(snake)
        keysPressed = pg.key.get_pressed()
        if keysPressed[pg.K_ESCAPE]:
            run=False
        snake.steer(keysPressed)
        ##copilot my searest, why is this throwing an error?
        # response: 
        
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