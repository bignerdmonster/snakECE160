import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
running = True
framerate = 15 # so online vers no break
## this is where we'd put initalizer code

screen.fill('red')

## IMPORTANT: ON WEB IOS, ONLY ARROW KEYS AND NON-WORD KEYS WORK!!!
## even more important: I LIED!!!! BLAHAHAHAHAHHAHA! 
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                print("UP!!!")
                screen.fill("blue")
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                print("UPDWON!!!")
                screen.fill("red")
    print("work?")
    pg.display.flip()
    clock.tick(15)
pg.quit()