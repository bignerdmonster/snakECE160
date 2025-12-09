import pygame as pg
import random
from menu import Menu

pg.init() #strict typing
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720 ## IDEAL
COLUMN_COUNT, ROW_COUNT = 41, 41 ## disgustingly out of fn. scope
#logic to figure out square height & stuff
CELL_LENGTH = SCREEN_WIDTH // COLUMN_COUNT
CELL_HEIGHT = SCREEN_HEIGHT // ROW_COUNT ## #honestly who cares if they're square.
CELL_DIMS = (CELL_LENGTH, CELL_HEIGHT) ## Too lazy to implement properly
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.SCALED | pg.RESIZABLE , vsync = 1) # i mean, i'll leave function references to this variable, but really it can just be constant.


font = pg.font.SysFont('papyrus', 36)
popUpColor = pg.color.Color(255,255,255,67)

class Progression():
    def __init__(self):
        self.lvls = {
            3: "popup",
            1: "music_box"
        }
        self.unlocked = []
        self.activated = []

    def check(self, length):
        newly_unlocked = []

        for n, f in self.lvls.items():
            if length >= n:
                if not self.unlocked.__contains__(f):
                    print(f"unlocked {f}")
                    self.unlocked.append(f)
                    self.activated.append(f)
                newly_unlocked.append(f)
        return newly_unlocked
    def contain(self, name):
        if name in self.unlocked and name in self.activated:
            self.activated.remove(name)
            return True
        else:
            return False

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
    objList = []
    def __init__(self, pos): ## how it feels to lazily assign pos to an actual strict value. idc.
        if type(self) not in (PopUps, musicBox):
            GameObject.objList.insert(0, self)
        else:
            GameObject.objList.append(self) ## popup needs to render last, and we can guarentee that by adding it into the last
        self.pos = pos if pos else [0, 0] #yeah
        self.pos.append(0) if len(self.pos) == 2 else 0 ## 3d coordinates, from base.
        self.color = 'magenta' #if anything is magenta colored, that means it has been setup invalidly. warning color.
        self.rect = pg.rect.Rect(CELL_LENGTH*self.pos[0], CELL_HEIGHT*self.pos[1], CELL_LENGTH, CELL_HEIGHT)
    def render(self, screenV=screen):
        #print(self.color)
        pg.draw.rect(screenV, self.color, self.rect)
    
    def collide(self, snake):
        print(self.__class__, "collided with snake!")


    @classmethod
    def Render(cls, screenV=screen):
        for obj in cls.objList:
            obj.render(screenV) #and we're back to the team flare noveau theme being so goated...
    @classmethod
    def Collide(cls, snake):
        for obj in [x for x in cls.objList if x != snake]:
            #print(type(obj), obj)
            snake.collide(obj)
    @classmethod
    def Reset(cls): ## works for each class extends GameObject (ex. Snake, Apple, PopUps, )
        for i in [x for x in GameObject.objList if type(x)==cls]:
            GameObject.objList.remove(i)

class Clickable(GameObject):
    def clicked(self):
        return self.rect.collidepoint(pg.mouse.get_pos()) and (pg.mouse.get_pressed())[0]

class Snake(GameObject):
    _instance = None ## ok frankly this was done by ai. I have YET to understand this chunk, but it will come soon.
    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            cls._instance.__del__()  # Clean up old instance from GameObject.objList
        cls._instance = super().__new__(cls)
        return cls._instance
        # ai code over
    def __init__(self, sMat, **args): #PLEASE pass custompos as a 3 val array if it is being used.
        initpos = sMat.center[:] if (not ('startPos' in args)) else args['startPos']
        super().__init__(initpos) #sets self.pos
        self.cols,self.rows = sMat.cols, sMat.rows # begrudging.
        self.color = 'green'

        self.direction = pg.Vector3(1,0,0) # three-dimensional movement possibilites. also start by moving right to avoid self collision at beginning
        self.specialFlags = {} # for custom controls-ish

        if 'controls' in args.keys(): # ALL OF THESE HAVE TO EXIST OR THE PROGRAM DIES.
            self.up = args['controls']['up'] 
            self.down = args['controls']['down']
            self.left = args['controls']['left']
            self.right = args['controls']['right']
            self.interact = args['controls']['interact']
            self.accel = args['controls']['accel']
            self.decel = args['controls']['decel']
        else: #default case... jacinthe's theme slaps so hard.
            self.up = pg.K_w
            self.down = pg.K_s
            self.left = pg.K_a
            self.right = pg.K_d
            self.interact = pg.K_e
        

        self.len = 1  # length of snake; used to determine when to pop tail

    def futurePos(self):
        ##  basically, this returns coordinates. It's the movement function, but doesn't update the movement 
        return [((self.pos[0] + int(self.direction.x)) % self.cols),
                ((self.pos[1] + int(self.direction.y)) % self.rows),
                (self.pos[2] + int(self.direction.z))]
    
    def collide(self, obj):
        #print(type(self),type(obj))
        if self.futurePos() == obj.pos:
            obj.collide(self)

    def move(self):
        self.pos = self.futurePos()[:]
        self.rect[0], self.rect[1] = (CELL_LENGTH*self.pos[0]), (CELL_HEIGHT*self.pos[1])#rect updater
        SnakeTail.tailList.insert(0, SnakeTail(self.pos[:])) ## insert the new head position at the start of the list
        if len(SnakeTail.tailList) > self.len:

            SnakeTail.Sever() ## remove tail if array is bigger than length
            ## todo: figure out triple collision!?!?!? update: it doesn't matter, we just can ignore it for now
        
        if self.specialFlags.get("debugPrint", False): # we can actaully adapt this system for like a boost or whatever.
            Apple.Reset()
            self.specialFlags["debugPrint"] = False # since inputs are processed 24/7, this allows a certain action to be queued, then happen when the snake moves. Works well!
         
    def steer(self, keys):
        if keys[self.up]:
            self.direction = pg.Vector3(0,-1,0) if self.direction.y != 1 else self.direction
        elif keys[self.down]:
            self.direction = pg.Vector3(0,1,0) if self.direction.y != -1 else self.direction
        elif keys[self.left]:
            self.direction = pg.Vector3(-1,0,0) if self.direction.x != 1 else self.direction
        elif keys[self.right]:
            self.direction = pg.Vector3(1,0,0) if self.direction.x != -1 else self.direction
        if keys[self.interact]:
            self.specialFlags["debugPrint"] = True # removed length increase cuz jank, did i mess up array?
        else:
            pass # I think this is needed... try check

class SnakeTail(GameObject):
    tailList = []
    def __init__(self, pos=[0,0,0]):
        super().__init__(pos)
        self.color = 'yellow'

    def collide(self, snake):
        print("Achilles' stage manager should throw something out for this")
        self.color = 'blue'

    @classmethod
    def Sever(cls):
        GameObject.objList.remove(cls.tailList.pop())



#funny music box
class musicBox(Clickable):
    maxTime = 1200
    def __init__(self, pos=[((COLUMN_COUNT//2)+(COLUMN_COUNT//4)),((ROW_COUNT//2)+(ROW_COUNT//4)),0]):
        super().__init__(pos)
        self.rect.scale_by_ip(9,7)
        self.time = musicBox.maxTime
        self.color = pg.color.Color(0, 0, 255, 76)
        self.last_tick = pg.time.get_ticks()
    def render(self, screenV = screen):
        #I need this to be translucent lmao
        current_time = pg.time.get_ticks()
        if (current_time - self.last_tick >= 1000) and not self.clicked():
            self.time -= 60 ## tick down by a second, only when not clicked tho
            self.last_tick = current_time
        super().render(screenV) # render box to screen

        text = font.render(f"Time: {self.time // 60}", True, (255, 255, 255))
        screenV.blit(text, (self.rect.x + 10, self.rect.y + 15)) # render text to screen

        if self.clicked() and self.time < musicBox.maxTime:
            self.time += 2 #sloow wind. 
        

class PopUps(Clickable):
    def __init__(self, pos=None):
        super().__init__((pos or [random.randint(0,COLUMN_COUNT),random.randint(0,ROW_COUNT)]))
        self.color = popUpColor
        self.rect.scale_by_ip(3.7,3.7)

    def render(self, screenV=screen):
        if self.clicked():
            GameObject.objList.remove(self)
            PopUps()
        super().render(screenV)
        
class QTE(GameObject):
    def __init__(self, pos=None):
        super().__init__(pos or  [random.randint(0,COLUMN_COUNT),random.randint(0,ROW_COUNT)])


class Apple(GameObject):
    def __init__(self,pos=None):
        super().__init__(pos or [random.randint(0,COLUMN_COUNT-1),random.randint(0,ROW_COUNT-1)])
        self.color = (255,0,0)

    def collide(self, snake):
        snake.len += 1
        GameObject.objList.remove(self)
        Apple()


print("line 161") ## this will stay here forever, as a memory to days long gone


SNAKE_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SNAKE_EVENT, 67) # every 1 s, the snake allegedly moves.

print("Starting")

framerate = 60

def snakeGame(menu, snake, progress): ## this is the actual main game loop function!! yay
    run = True
    
    while run:
        progress.check(snake.len)
        screen.fill('black')
        keysPressed = pg.key.get_pressed()

        if keysPressed[pg.K_ESCAPE]: ## this is up here to break before anything else
            run = False
            nextMenu = 1 # 1 for Pause menu

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            if event.type == SNAKE_EVENT:
                GameObject.Collide(snake) #check collision first

                snake.move() #main aaaaalogic, operating one time per second. right now just moving.
                # musicBox.tick()

                if keysPressed[pg.K_RETURN]:
                    #print(GameObject.objList)
                    Apple() # make apple.
                    
                if progress.contain("popup"):
                    PopUps()
                if progress.contain("music_box"):
                    musicBox()
        if keysPressed[pg.K_ESCAPE]:
            run = False
            nextMenu = 1 # 1 for Pause menu
        snake.steer(keysPressed)

        GameObject.Render(screen) # to be clear, renders all game objects.
        pg.display.flip()
        clock.tick()
    menu.notstop = True
    print("ho")





if __name__ == "__main__":
    
    mainMat = SnakeMat(COLUMN_COUNT,ROW_COUNT)
    mainSnake = Snake(mainMat)
    Apple()
    clock = pg.time.Clock()

    framerate = 60
    mainMenu = Menu(screenInp=screen, clocked=clock,win_h=SCREEN_HEIGHT,win_w=SCREEN_WIDTH) #testing w/ start-game = none
    while True:
        mainMenu.run()
        snakeGame(mainMenu,mainSnake, Progression())
    
else:
    print("snakeCore imported, or YOU SHOULD RUN THIS WITH python3 snakeCore.py")