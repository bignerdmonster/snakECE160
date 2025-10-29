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
    keys = pg.key.get_pressed()
    print("done")
    print(keys)
    print("next")
    pg.display.flip()
    clock.tick(0.1)
pg.quit()