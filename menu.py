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

        self.title_font = pg.font.Font("media/billo.ttf", 110)
        self.small_font = pg.font.SysFont(None, 30)
        self.btn_font = pg.font.Font("media/billo.ttf", 36)

        self.play_btn = Button("Play - Enter", (self.win_w//2, self.win_h//2 + 40))
        self.howto_btn = Button("How to Play - H", (self.win_w//2, self.win_h//2 + 140))
        self.quit_btn = Button("Quit - Esc", (self.win_w//2, self.win_h//2 + 240))

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
        self.snake_dir = pg.Vector2(2, 0)
        self.snake_pos = pg.Vector2(-200, self.win_h // 2)

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
        self.snake_pos += self.snake_dir

        if self.snake_pos.x > self.win_w + 200:
            self.snake_pos.x = -200
            self.snake_pos.y = random.randint(100, self.win_h - 100)

        wave = math.sin(self.t * 0.08) * 40

        self.snake_points.insert(0, (self.snake_pos.x, self.snake_pos.y + wave))
        if len(self.snake_points) > self.snake_length:
            self.snake_points.pop()

        for i, p in enumerate(self.snake_points):
            size = max(2, 8 - i // 6)

        # ✅ Clamp green channel to valid range (0–255)
            green = min(255, 160 + i * 2)
            color = (0, green, 120)

            pg.draw.circle(self.screen, color, (int(p[0]), int(p[1])), size)


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

class GameOverScreen:
    def __init__(self, screen, clock, len=None, win_w=1080, win_h=720, *args, **kwargs):
        self.screen = screen
        self.clock = clock
        self.win_w = win_w
        self.win_h = win_h
        self.score = len

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

        self.menu_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)


    def _handle_event(self, event):
        if event.type == pg.QUIT:
            return "quit_game"

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return "main_menu"
            elif event.key == pg.K_ESCAPE:
                return "quit_game"

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