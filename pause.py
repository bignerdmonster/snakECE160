import pygame as pg
import math
import random

BG = (14, 14, 18)
TEXT = (235, 235, 240)
MUTED = (150, 150, 160)
ACCENT = (0, 200, 90)
ACCENT_H = (0, 160, 70)
NEON = (0, 255, 165)
SHADOW = (8, 8, 12)

class Button:
    def __init__(self, txt, center, size=(320, 80)):
        self.txt = txt
        self.rect = pg.Rect(0, 0, *size)
        self.rect.center = center

    def draw(self, surf, font=None):
        if not pg.font.get_init():
            pg.font.init()

        font = font or pg.font.SysFont(None, 36)
        hovering = self.rect.collidepoint(pg.mouse.get_pos())

        shadow_rect = self.rect.copy()
        shadow_rect.y += 6
        pg.draw.rect(surf, SHADOW, shadow_rect, border_radius=18)

        if hovering:
            glow = pg.Surface(self.rect.size, pg.SRCALPHA)
            glow.fill((*NEON, 100))
            surf.blit(glow, self.rect.topleft)

        pg.draw.rect(surf, ACCENT_H if hovering else ACCENT, self.rect, border_radius=18, width=2)

        inner = self.rect.inflate(-12, -12)
        pg.draw.rect(surf, BG, inner, border_radius=14)

        label = font.render(self.txt, True, TEXT if hovering else MUTED)
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

        self.title_font = pg.font.SysFont(None, 110)
        self.small_font = pg.font.SysFont(None, 32)

        self.retry_btn = Button("Retry (R)", (win_w // 2, win_h // 2))
        self.menu_btn = Button("Main Menu (Enter)", (win_w // 2, win_h // 2 + 100))
        self.quit_btn = Button("Quit Game (Esc)", (win_w // 2, win_h // 2 + 200))

        self.stars = [(random.randint(0, win_w), random.randint(0, win_h), random.randint(1, 3)) for _ in range(140)]
        self.t = 0

        # ---- Screen Shake ----
        self.shake_timer = 20
        self.shake_intensity = 8


    def _draw_background(self):
        self.screen.fill(BG)

        for i, (x, y, s) in enumerate(self.stars):
            y += s
            if y > self.win_h:
                y = 0
                x = random.randint(0, self.win_w)
            self.stars[i] = (x, y, s)
            pg.draw.circle(self.screen, (35, 35, 45), (x, y), s)

        for y in range(0, self.win_h, 6):
            pg.draw.line(self.screen, (0, 0, 0, 35), (0, y), (self.win_w, y))


    def _draw(self):
        offset_x = 0
        offset_y = 0

        if self.shake_timer > 0:
            self.shake_timer -= 1
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

        self._draw_background()
        self.t += 1

        pulse = 10 + int(math.sin(self.t * 0.08) * 8)
        title_text = "G A M E   O V E R !"

        shadow = self.title_font.render(title_text, True, SHADOW)
        glow = self.title_font.render(title_text, True, NEON)
        title = self.title_font.render(title_text, True, TEXT)

        for i in range(3):
            self.screen.blit(
                glow,
                glow.get_rect(center=(self.win_w // 2 + offset_x, self.win_h // 2 - 160 + pulse + i + offset_y))
            )

        self.screen.blit(
            shadow,
            shadow.get_rect(center=(self.win_w // 2 + 6 + offset_x, self.win_h // 2 - 160 + 6 + offset_y))
        )

        self.screen.blit(
            title,
            title.get_rect(center=(self.win_w // 2 + offset_x, self.win_h // 2 - 160 + offset_y))
        )

        if self.score is not None:
            score_label = self.small_font.render(f"Score: {self.score}", True, TEXT)
            self.screen.blit(
                score_label,
                score_label.get_rect(center=(self.win_w // 2 + offset_x, self.win_h // 2 - 80 + offset_y))
            )

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
            self.clock.tick(60)
