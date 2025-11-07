import pygame as pg
from menu import Menu
import random
pg.init() #strict typing
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 720
COLUMN_COUNT, ROW_COUNT = 15, 11 #disgustingly out of fn. scope
#logic to figure out square height & stuff
CELL_LENGTH = SCREEN_WIDTH // COLUMN_COUNT
CELL_HEIGHT = SCREEN_HEIGHT // ROW_COUNT ## #honestly who cares if they're square.
CELL_DIMS = (CELL_LENGTH, CELL_HEIGHT) ## Too lazy to implement properly
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.SCALED, vsync=1) # i mean, i'll leave function references to this variable, but really it can just be constant.




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

print("line 29")
class GameObject:
    objList = []
    def __init__(self, pos = None, sMat = SnakeMat()): ## how it feels to lazily assign pos to an actual strict value. idc.
        print("I'm being created!", type(self))
        GameObject.objList.append(self)
        self.pos = pos if pos else [0, 0]
        self.pos.append(0) if len(self.pos) == 2 else 1 ## 3d coordinates, from base.
        self.sMat = sMat
        self.color = 'pink'
        self.rect = [CELL_LENGTH*self.pos[0], CELL_HEIGHT*self.pos[1], CELL_LENGTH, CELL_HEIGHT]
    def render(self, screenV=screen):
        #print(self.color)
        pg.draw.rect(screenV, self.color, self.rect)
    
    def collide(self, snake):
        quit()

    def __del__(self):
        GameObject.objList.remove(self)

    @classmethod
    def Render(cls, screenV=screen):
        for obj in cls.objList:
            obj.render(screenV) #and we're back to the team flare noveau theme being so goated...
    @classmethod
    def Collide(cls, snake):
        for obj in [x for x in cls.objList if x != snake]:
            #print(type(obj), obj)
            snake.collide(obj)




class Snake(GameObject):
    _instance = None ## ok frankly this was done by ai. I have YET to understand this chunk, but it will come soon.
    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            cls._instance.__del__()  # Clean up old instance from GameObject.objList
        cls._instance = super().__new__(cls)
        return cls._instance
        # ai code over
    def __init__(self, sMat = SnakeMat(), **args): #PLEASE pass custompos as a 3 val array if it is being used.
        initpos = sMat.center[:] if (not ('startPos' in args)) else args['startPos']
        super().__init__(initpos, sMat) #sets self.pos, self.sMat,
        self.color = 'green'
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

    def futurePos(self):
        ##  basically, this returns coordinates. It's the movement function, but doesn't update the movement 
        return [((self.pos[0] + int(self.direction.x)) % self.sMat.cols), 
                ((self.pos[1] + int(self.direction.y)) % self.sMat.rows), 
                (self.pos[2] + int(self.direction.z))]
    
    def collide(self, obj=GameObject()):
        #print(type(self),type(obj))
        if self.futurePos() == obj.pos:
            obj.collide(self)
        elif self.futurePos() in self.bPos:
            ## snake hits tail... just going to ignore for now
            pass

    def move(self):
        self.pos = self.futurePos()[:]
        self.rect = [CELL_LENGTH*self.pos[0], CELL_HEIGHT*self.pos[1], CELL_LENGTH, CELL_HEIGHT] #rect
        
        self.bPos.insert(0, self.pos[:]) ## insert the new head position at the start of the list
        if len(self.bPos) > self.len:
            self.bPos.pop() ## remove tail if array is bigger than length
            
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
    def render(self, screenV=screen):
        super().render(screenV)
        for segment in self.bPos[1:]:
            pg.draw.rect(screenV, 'yellow', [CELL_LENGTH*segment[0], CELL_HEIGHT*segment[1], CELL_LENGTH, CELL_HEIGHT])
        pass

class Apple(GameObject):
    def __init__(self,pos=[0,0],sMat=SnakeMat()):
        super().__init__(pos,sMat)
        self.color = (255,0,0)
    

    def collide(self, snake):
        snake.len += 1
        GameObject.objList.remove(self)
    
print("line 161")


SNAKE_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SNAKE_EVENT, 1000) # every 1 s, the snake allegedly moves.

print("Starting")
framerate = 15
def snakeGame(menu = Menu(screenInp=screen), snake=Snake(SnakeMat())): ## this is the actual main game loop function!! yay
    run = True
    while run:
        screen.fill('black')
        keysPressed = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            if event.type == SNAKE_EVENT:
                GameObject.Collide(snake) #check collision first
                snake.move() #main logic, operating one time per second. right now just moving.
                print(snake)
                if keysPressed[pg.K_RETURN]:
                    print(GameObject.objList)
                    Apple([random.randint(0,14),random.randint(0,10)],snake.sMat) # make apple.
                    
        if keysPressed[pg.K_ESCAPE]:
            run=False
        snake.steer(keysPressed)

        GameObject.Render(screen)
        pg.display.flip()
        clock.tick(framerate)
    menu.notstop = True




if __name__ == "__main__":

    mainMat = SnakeMat()
    mainSnake = Snake(mainMat)
    Apple([5,5], mainMat)
    clock = pg.time.Clock()

    framerate = 15
    mainMenu = Menu(screenInp=screen, start_game=None, clocked=clock) #testing w/ start-game = none
    while True:
        mainMenu.run()
        snakeGame(mainMenu,mainSnake)
else:
    print("snakeCore imported, or YOU SHOULD RUN THIS WITH python3 snakeCore.py")