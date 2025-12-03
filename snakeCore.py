import pygame as pg
import random, os, sys
from menu import Menu

pg.init() #strict typing
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 720
COLUMN_COUNT, ROW_COUNT = 9, 5 ##d isgustingly out of fn. scope
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


class GameObject:
    objList = []
    def __init__(self, pos, sMat): ## how it feels to lazily assign pos to an actual strict value. idc.
        GameObject.objList.append(self) # keep track.
        self.pos = pos if pos else [0, 0] #yeah
        self.pos.append(0) if len(self.pos) == 2 else 1 ## 3d coordinates, from base.
        self.sMat = sMat # snake mat! 
        self.color = 'magenta' #if anything is magenta colored, that means it has been setup invalidly. warning color.
        self.rect = [CELL_LENGTH*self.pos[0], CELL_HEIGHT*self.pos[1], CELL_LENGTH, CELL_HEIGHT]
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
        super().__init__(initpos, sMat) #sets self.pos, self.sMat,
        self.color = 'green'
        self.bPos = [self.pos[:]] # bPos is an array containing all the positions where snake segments are. bPos[0] will always be the head, and segments get older as you progress through the array. 0, 1 0, 2 1 0, etc.
        self.direction = pg.Vector3(1,0,0) # three-dimensional movement possibilites. also start by moving right to avoid self collision at beginning
        self.specialFlags = {} # for custom controls-ish

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
    
    def collide(self, obj):
        #print(type(self),type(obj))
        if self.futurePos() == obj.pos:
            obj.collide(self)
        elif self.futurePos() in self.bPos:
            print("yo this should probably end the game")
            pass

    def move(self):
        self.pos = self.futurePos()[:]
        self.rect = [CELL_LENGTH*self.pos[0], CELL_HEIGHT*self.pos[1], CELL_LENGTH, CELL_HEIGHT] #rect
        self.bPos.insert(0, self.pos[:]) ## insert the new head position at the start of the list
        if len(self.bPos) > self.len:
            self.bPos.pop() ## remove tail if array is bigger than length
        
        if self.specialFlags.get("debugPrint", False): # we can actaully adapt this system for like a boost or whatever.
            print(self.bPos) 
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
    def render(self, screenV):
        super().render(screenV)

        for segment in self.bPos[1:]:
            pg.draw.rect(screenV, 'yellow', [CELL_LENGTH*segment[0], CELL_HEIGHT*segment[1], CELL_LENGTH, CELL_HEIGHT])
        pass

#funny fnaf music box
class musicBox():
    def __init__(self, time = 450):
        self.maxtime = time
        self.time = time
        self.mB = pg.Rect(random.randint(200, SCREEN_WIDTH - 200), random.randint(200, SCREEN_HEIGHT - 200), 150, 150)
        self.color = (0, 0, 255, 76)
        self.last_tick = pg.time.get_ticks()
    def explode(self):
        return self.time < 0
    def holding(self):
        # uh it ticked way too fast before so I'm using get_ticks to track time
        current_time = pg.time.get_ticks()
        if self.time < self.maxtime:
            if current_time - self.last_tick >= 100:
                self.time += 60
                self.last_tick = current_time
            if self.time > self.maxtime:
                self.time -= abs(self.time - self.maxtime)
    def tick(self):
        #uh it ticked way too fast before so I'm using get_ticks to track time
        current_time = pg.time.get_ticks()
        if current_time - self.last_tick >= 1000:
            self.time -= 60
            self.last_tick = current_time
    def render(self, screenV = screen):
        #I need this to be translucent lmao
        surf = pg.Surface((150, 150), pg.SRCALPHA)
        surf.fill(self.color)
        screenV.blit(surf, self.mB)

        # timer, if timer hit 0 they die idk
        font = pg.font.Font(None, 36)
        text = font.render(f"Time: {self.time // 60}", True, (255, 255, 255))
        screenV.blit(text, (self.mB.x + 10, self.mB.y + 10))

        #handles if they're winding it
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()
        if self.mB.collidepoint(mouse_x, mouse_y) and mouse_pressed[0]:
            self.holding() #adds 2 secs to da timer

class PopUps():
    def __init__(self, pos):
        self.pos = pos
        self.color = (255,255,255, 67)
        self.popup = pg.Rect(pos[0], pos[1], 400, 400)
        self.clicked = False
    def render(self):
        pg.draw.rect(screen, self.color, self.popup)
    def check(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()
        if self.popup.collidepoint(mouse_x, mouse_y) and mouse_pressed[0]:
            self.popup = pg.Rect(random.randint(400, SCREEN_WIDTH - 400), random.randint(400, SCREEN_HEIGHT - 400), 400, 400)
            return True
        else:
            return False
        

class Apple(GameObject):
    def __init__(self,pos,sMat):
        super().__init__(pos,sMat)
        self.color = (255,0,0)

    def collide(self, snake):
        snake.len += 1
        GameObject.objList.remove(self)
        Apple([random.randint(0, COLUMN_COUNT),random.randint(0,ROW_COUNT)], mainMat)

print("line 161")


SNAKE_EVENT = pg.USEREVENT + 1
pg.time.set_timer(SNAKE_EVENT, 67) # every 1 s, the snake allegedly moves.

print("Starting")
framerate = 60

def snakeGame(menu, snake): ## this is the actual main game loop function!! yay
    run = True
    #popup = PopUps([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)])
    while run:
        screen.fill('black')
        keysPressed = pg.key.get_pressed()
        """if popup.check():
            popup = PopUps([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)])"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            if event.type == SNAKE_EVENT:
                GameObject.Collide(snake) #check collision first
                snake.move() #main logic, operating one time per second. right now just moving.
                # musicBox.tick()
                # print(snake) ho brah no need this no more...
                if keysPressed[pg.K_RETURN]:
                    #print(GameObject.objList)
                    Apple([random.randint(0,COLUMN_COUNT-1),random.randint(0,ROW_COUNT-1)],snake.sMat) # make apple.
        if keysPressed[pg.K_ESCAPE]:
            run = False
            nextMenu = 1 # 1 for Pause menu
        elif keysPressed[pg.K_v]:
            print(0)
            os.execv(sys.argv[0])
        snake.steer(keysPressed)
        if snake.pos[0] < 0 or snake.pos[0] >= snake.sMat.cols or snake.pos[1] < 0 or snake.pos[1] >= snake.sMat.rows:
            screen.fill('yellow') ## this also shouldnt come up
        GameObject.Render(screen) # to be clear, renders all game objects.
        #musicbox stuff
        """musicBox.render(screen)
        popup.render()
        if musicBox.explode():
            run = False"""
        pg.display.flip()
        clock.tick()
    menu.notstop = True
    print("ho")





if __name__ == "__main__":
    
    mainMat = SnakeMat(COLUMN_COUNT,ROW_COUNT)
    mainSnake = Snake(mainMat)
    Apple([5,5], mainMat)
    clock = pg.time.Clock()
    musicBox = musicBox()

    framerate = 60
    mainMenu = Menu(screenInp=screen, clocked=clock,win_h=SCREEN_HEIGHT,win_w=SCREEN_WIDTH) #testing w/ start-game = none
    while True:
        mainMenu.run()
        snakeGame(mainMenu,mainSnake)
    
else:
    print("snakeCore imported, or YOU SHOULD RUN THIS WITH python3 snakeCore.py")