import pygame as pg

BG = (18, 18, 20)
TEXT = (235, 235, 240)
MUTED = (150, 150, 160)
ACCENT = (0, 200, 90)
ACCENT_H = (0, 160, 70)


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


class GameOverScreen:
    def __init__(self, screen, clock, score=None, win_w=1080, win_h=720):
        self.screen = screen
        self.clock = clock
        self.win_w = win_w
        self.win_h = win_h
        self.score = score

        self.running = True

        # fonts
        self.title_font = pg.font.SysFont(None, 96)
        self.small_font = pg.font.SysFont(None, 32)

        # buttons
        self.retry_btn = Button("Retry (R)", (win_w // 2, win_h // 2))
        self.menu_btn = Button("Main Menu (Enter)", (win_w // 2, win_h // 2 + 90))
        self.quit_btn = Button("Quit Game (Esc)", (win_w // 2, win_h // 2 + 180))

    def _draw(self):
        self.screen.fill(BG)

        # Game Over title
        title = self.title_font.render("G A M E   O V E R !", True, TEXT)
        self.screen.blit(title, title.get_rect(center=(self.win_w // 2, self.win_h // 2 - 150)))

        # Buttons
        self.retry_btn.draw(self.screen)
        self.menu_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)

    def _handle_event(self, event):
        if event.type == pg.QUIT:
            return "quit_game"

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                return "retry"
            elif event.key == pg.K_RETURN:
                return "main_menu"
            elif event.key == pg.K_ESCAPE:
                return "quit_game"

        if self.retry_btn.clicked(event):
            return "retry"
        if self.menu_btn.clicked(event):
            return "main_menu"
        if self.quit_btn.clicked(event):
            return "quit_game"

        return None

    def run(self):
        while self.running:
            for event in pg.event.get():
                action = self._handle_event(event)
                if action:
                    return action

            self._draw()
            pg.display.flip()
            self.clock.tick(15)
