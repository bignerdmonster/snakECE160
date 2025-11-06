import pygame as pg
from menu import Menu
import random


pg.init() #I hate strict typing.
screen = pg.display.set_mode((1080,720), pg.SCALED, vsync=1) # i mean, i'll leave function references to this variable, but really it can just be constant.


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

class GameObject:
    def __init__(self, pos = None, sMat = SnakeMat()): ## how it feels to lazily assign pos to an actual strict value. idc.
        self.pos = pos if pos else [0, 0]
        self.pos.append(0) if len(self.pos) == 2 else 1 ## 3d coordinates, from base.
        self.sMat = sMat
    def render(self, screenV=screen):
        pass # comment for unrelated commit test




class Snake(GameObject):
    soleSnake = ["how recursive do we have to get"]
    def __init__(self, sMat = SnakeMat(), **args): #PLEASE pass custompos as a 3 val array if it is being used.
        Snake.soleSnake[0]=self
        initpos = sMat.center[:] if (not ('startPos' in args)) else args['startPos']
        super().__init__(initpos) #sets self.pos, self.sMat,

        self.bPos = [self.pos[:]] # bPos is an array containing all the positions where snake segments are. bPos[0] will always be the head, and segments get older as you progress through the array. 0, 1 0, 2 1 0, etc.
        self.direction = pg.Vector3(0,0,0) # three-dimensional movement possibilites

        if 'controls' in args.keys(): # ALL OF THESE HAVE TO EXIST OR THE PROGRAM DIES.
            self.up = args['controls']['up'] 
            self.down = args['controls']['down']
            self.left = args['controls']['left']
            self.right = args['controls']['right']
            self.interact = args['controls']['interact']
        else: #default case... jacinthe's theme slaps so hard.
            self.up = pg.K_w
            self.down = pg.K_s
            self.left = pg.K_a
            self.right = pg.K_d
            self.interact = pg.K_e
        
        self.sMat = sMat
        sMat.mat[self.pos[0]][self.pos[1]] = 2 ## 2 is the snake's head. the AI is mimicking my style. this is black mirror to an extent which i find strange.
        self.len = 1  # length of snake; used to determine when to pop tail
        
    def move(self):
        self.pos[0] = (self.pos[0] + int(self.direction.x)) % self.sMat.cols; self.pos[1] = (self.pos[1] + int(self.direction.y)) % self.sMat.rows; self.pos[2] = (self.pos[2] + int(self.direction.z)) # %% self.sMat.z but we're not ready for that yet # increment head position by direction vector
        # modulo to keep the snake from throwing index errors
        self.bPos.insert(0, self.pos[:]) ## insert the new head position at the start of the list, allowing for head to remain constant... 0, 1 0, 2 1 0, etc
        if len(self.bPos) > self.len:
            self.bPos.pop() ## remove tail if array is bigger than length, basically... yeah!
            
    def steer(self, keys):
        if keys[self.up]:
            self.direction = pg.Vector3(0,-1,0)
        elif keys[self.down]:
            self.direction = pg.Vector3(0,1,0)
        elif keys[self.left]:
            self.direction = pg.Vector3(-1,0,0)
        elif keys[self.right]:
            self.direction = pg.Vector3(1,0,0)
        if keys[self.interact]:
            self.len += 1 # test snake increase, this works weirdly due to inputs being processed 24/7, but logic performing once per second
        else:
            pass # I think this is needed... try check
    def __str__(self):
       
        retStr = ""
        tempMat = [[0 for place in range(self.sMat.cols)] for row in range(self.sMat.rows)]
        for i, segment in enumerate(self.bPos):
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


SNAKE_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SNAKE_EVENT, 1000) # every 1 s, the snake allegedly moves.

#apple = Apple()
print("bkpoint")
def snakeGame(menu = Menu(screenInp=screen), snake=Snake(SnakeMat())): ## this is the actual main game loop function!! yay
    #apple_exist = False
    run = True
    while run:
        screen.fill('black')
        ## and Corbeau's theme slaps too zawg.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            if event.type == SNAKE_EVENT:
                snake.move() #main logic, operating one time per second. right now just moving.
                print(snake)
        keysPressed = pg.key.get_pressed()
        if keysPressed[pg.K_ESCAPE]:
            run=False
        snake.steer(keysPressed)

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