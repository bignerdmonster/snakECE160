import pygame as pg
import math
import random

BG = (12, 12, 16)
TEXT = (240, 240, 255)
MUTED = (120, 120, 140)
ACCENT = (0, 255, 120)
ACCENT_H = (0, 200, 90)
NEON = (0, 255, 170)
SHADOW = (6, 6, 10)

# ------------ UI ------------
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
        pg.draw.rect(surf, SHADOW, shadow_rect, border_radius=20)

        if hovering:
            glow = pg.Surface(self.rect.size, pg.SRCALPHA)
            glow.fill((*NEON, 90))
            surf.blit(glow, self.rect.topleft)

        pg.draw.rect(surf, ACCENT_H if hovering else ACCENT, self.rect, border_radius=20, width=2)

        inner = self.rect.inflate(-12, -12)
        pg.draw.rect(surf, BG, inner, border_radius=16)

        label = font.render(self.txt, True, TEXT if hovering else MUTED)
        surf.blit(label, label.get_rect(center=self.rect.center))

        return hovering

    def clicked(self, event):
        return (
            event.type == pg.MOUSEBUTTONDOWN and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

class Menu:
    def __init__(self, screenInp=None, title="Stake (get it like start and snake lol)", clocked=pg.time.Clock(), win_w=1080, win_h=720):
        self.notstop = True
        self.screen = screenInp or pg.display.set_mode((win_w, win_h), pg.SCALED, vsync=1)
        pg.display.set_caption(title)
        self.clock = clocked
        self.win_w = win_w
        self.win_h = win_h

        self.title_font = pg.font.SysFont(None, 110)
        self.small_font = pg.font.SysFont(None, 30)
        self.btn_font = pg.font.SysFont(None, 36)

        self.play_btn = Button("Play (Enter)", (self.win_w//2, self.win_h//2 + 40))
        self.howto_btn = Button("How to Play (H)", (self.win_w//2, self.win_h//2 + 140))
        self.quit_btn = Button("Quit (Esc)", (self.win_w//2, self.win_h//2 + 240))

        self.show_help = False
        self.lines = [
            "Use Arrow Keys or WASD to move.",
            "",
            "Press Esc to switch between this screen and the menu."
        ]

        self.stars = [(random.randint(0, win_w), random.randint(0, win_h), random.randint(1, 3)) for _ in range(120)]
        self.t = 0

        # Background snake
        self.snake_points = []
        self.snake_length = 60
        self.snake_dir = random.choice([
            pg.Vector2(4, 0),
            pg.Vector2(-4, 0),
            pg.Vector2(0, 4),
            pg.Vector2(0, -4)
    ])

        self.snake_pos = pg.Vector2(
        random.randint(100, self.win_w - 100),
        random.randint(100, self.win_h - 100)
)


        # Animated Logo
        self.logo_hue = 0

    def _draw_arcade_background(self):
        self.screen.fill(BG)

        for i, (x, y, s) in enumerate(self.stars):
            y += s
            if y > self.win_h:
                y = 0
                x = random.randint(0, self.win_w)
            self.stars[i] = (x, y, s)
            pg.draw.circle(self.screen, (40, 40, 50), (x, y), s)

        for y in range(0, self.win_h, 6):
            pg.draw.line(self.screen, (0, 0, 0, 35), (0, y), (self.win_w, y))

        self._draw_background_snake()


    def _draw_glow_title(self):
        self.logo_hue = (self.logo_hue + 1) % 255
        pulse = 10 + int(math.sin(self.t * 0.05) * 8)

        color = pg.Color(0)
        color.hsva = (self.logo_hue, 90, 100, 100)

        title_text = "S n a k e !"

        shadow = self.title_font.render(title_text, True, SHADOW)
        glow = self.title_font.render(title_text, True, color)
        main = self.title_font.render(title_text, True, TEXT)

        for i in range(3):
            self.screen.blit(glow, glow.get_rect(center=(self.win_w//2, self.win_h//2 - 150 + pulse + i)))

        self.screen.blit(shadow, shadow.get_rect(center=(self.win_w//2 + 6, self.win_h//2 - 150 + 6)))
        self.screen.blit(main, main.get_rect(center=(self.win_w//2, self.win_h//2 - 150)))

    def _draw_help(self):
        self._draw_arcade_background()
        self._draw_glow_title()

        help_title = self.title_font.render("How to Play", True, TEXT)
        self.screen.blit(help_title, help_title.get_rect(center=(self.win_w//2, 180)))

        for i, line in enumerate(self.lines):
            label = self.small_font.render(line, True, TEXT)
            self.screen.blit(label, label.get_rect(center=(self.win_w//2, 280 + i * 42)))

    def _draw_main(self):
        self._draw_arcade_background()
        self._draw_glow_title()

        self.play_btn.draw(self.screen, self.btn_font)
        self.howto_btn.draw(self.screen, self.btn_font)
        self.quit_btn.draw(self.screen, self.btn_font)

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

    def _draw_background_snake(self):
        SPEED = 4
        self.snake_pos += self.snake_dir * (SPEED / 8)

        if not hasattr(self, "turn_cooldown"):
            self.turn_cooldown = 0

        if self.turn_cooldown > 0:
            self.turn_cooldown -= 1
        else:
            if random.random() < 0.08:
                possible_dirs = [
                    pg.Vector2(8, 0),
                    pg.Vector2(-8, 0),
                    pg.Vector2(0, 8),
                    pg.Vector2(0, -8)
                ]

                reverse = -self.snake_dir
                valid_dirs = [d for d in possible_dirs if d != reverse]

                if valid_dirs:
                    self.snake_dir = random.choice(valid_dirs)
                    self.turn_cooldown = 8

        if self.snake_pos.x < 0:
            self.snake_pos.x = self.win_w
        if self.snake_pos.x > self.win_w:
            self.snake_pos.x = 0
        if self.snake_pos.y < 0:
            self.snake_pos.y = self.win_h
        if self.snake_pos.y > self.win_h:
            self.snake_pos.y = 0

        self.snake_points.insert(0, (int(self.snake_pos.x), int(self.snake_pos.y)))
        if len(self.snake_points) > self.snake_length:
            self.snake_points.pop()

        BLOCK_SIZE = 12

        for i, (x, y) in enumerate(self.snake_points):
            green = min(255, 160 + i * 2)
            color = (0, green, 120)

            rect = pg.Rect(
                x - BLOCK_SIZE // 2,
                y - BLOCK_SIZE // 2,
                BLOCK_SIZE,
                BLOCK_SIZE
            )

            pg.draw.rect(self.screen, color, rect)




    def run(self):
        while self.notstop:
            self.t += 1
            for event in pg.event.get():
                self._handle_event(event)

            if self.show_help:
                self._draw_help()
            else:
                self._draw_main()

            pg.display.flip()
            self.clock.tick(60)

