# imports thingy things for Menu.py


import pygame as pg





BG = (18, 18, 20)
TEXT = (235, 235, 240)
MUTED = (150, 150, 160)
ACCENT = (0, 200, 90)
ACCENT_H = (0, 160, 70)

# ------------ UI ------------
class Button:
    def __init__(self, txt, center, size=(280, 72)):
        self.txt = txt
        self.rect = pg.Rect(0, 0, *size)
        self.rect.center = center

    def draw(self, surf, font=None):
        if not pg.font.get_init():
            pg.font.init()
        font = font or pg.font.SysFont(None, 36)
        hovering = self.rect.collidepoint(pg.mouse.get_pos())
        pg.draw.rect(surf, ACCENT_H if hovering else ACCENT, self.rect, border_radius=14)
        label = font.render(self.txt, True, (255, 255, 255))
        surf.blit(label, label.get_rect(center=self.rect.center))
        return hovering

    def clicked(self, event):
        return (
            event.type == pg.MOUSEBUTTONDOWN and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

class Menu:
    def __init__(self, screenInp=None, start_game=None, title="Stake (get it like start and snake lol)",clocked=pg.time.Clock(),win_w=1080, win_h=720):
        self.notstop = True
        self.screen = screenInp or pg.display.set_mode((win_w, win_h), pg.SCALED, vsync=1)
        pg.display.set_caption(title)
        self.clock = clocked
        self.win_w = win_w
        self.win_h = win_h
        self.title_font = pg.font.SysFont(None, 96)
        self.small_font = pg.font.SysFont(None, 28)

        #btns
        self.play_btn = Button("Play (Enter)", (self.win_w//2, self.win_h//2 + 20))
        self.howto_btn = Button("How to Play (H)", (self.win_w//2, self.win_h//2 + 110))
        self.quit_btn = Button("Quit (Esc)", (self.win_w//2, self.win_h//2 + 200))
        self.show_help = False
        self.lines = [
            "Use Arrow Keys or WASD to move.",
            "",
            "Press Esc to switch between this screen and the menu."
        ]
        

    def _draw_help(self):
        howPlay = self.title_font.render("How to Play", True, TEXT)
        self.screen.blit(howPlay, howPlay.get_rect(center=(self.win_w//2, 140)))
        for line in self.lines:
            label = self.small_font.render(line, True, TEXT)
            self.screen.blit(label, label.get_rect(center=(self.win_w//2, 240 + self.lines.index(line) * 40)))
    def _draw_main(self):
        title = self.title_font.render("snake", True, TEXT)
        self.screen.blit(title, title.get_rect(center=(self.win_w//2, self.win_h//2 - 120)))


        self.play_btn.draw(self.screen)
        self.howto_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)
    def _handle_event(self, event):
        if event.type == pg.QUIT:
            self._shutdown_and_exit()
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN and not self.show_help:
                self.notstop = False
            elif event.key == pg.K_h:
                self.show_help = True
            elif event.key == pg.K_ESCAPE:
                if self.show_help:
                    self.show_help = False
                else:
                    self._shutdown_and_exit()
        
        if self.play_btn.clicked(event) and not self.show_help:
            self.notstop = False
        if self.howto_btn.clicked(event):
            self.show_help = True
        if self.quit_btn.clicked(event):
            self._shutdown_and_exit()
    def _shutdown_and_exit(self):
        pg.quit()
        quit(0)
    def run(self):
        while self.notstop:
            for event in pg.event.get():
                self._handle_event(event)
            self.screen.fill(BG)

            if self.show_help:
                self._draw_help()
            else:
                self._draw_main()
            pg.display.flip()
            self.clock.tick(15)
        
        
