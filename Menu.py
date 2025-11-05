# imports thingy things for Menu.py
import sys
import subprocess
import pygame as pg
from pathlib import Path

# ------------ Config ------------
GAME_FILE = "snakeCore.py" ## <=== don't change this unless you change the main file name
WIN_W, WIN_H = 1080, 720
FPS = 60

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

    def draw(self, surf, font):
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

def run_game():
    # Closes the game before running if need be for like restarts
    pg.display.quit()
    pg.quit()

    try:
        subprocess.call([sys.executable, GAME_FILE])
    finally:
        # Re-init pygame after the game exits
        pg.init()
        pg.display.set_caption("Snake — Start Menu")
        pg.display.set_mode((WIN_W, WIN_H))
        pg.mouse.set_visible(True)

def main():
    # Checks
    if not Path(GAME_FILE).exists():
        print(f"Could not find {GAME_FILE}. Put menu.py in the same folder as {GAME_FILE}.")
        sys.exit(1)

    pg.init()
    pg.display.set_caption("Snake — Start Menu")
    screen = pg.display.set_mode((WIN_W, WIN_H))
    clock = pg.time.Clock()

    # Fonts
    title_font = pg.font.SysFont(None, 96)
    btn_font   = pg.font.SysFont(None, 42)
    small_font = pg.font.SysFont(None, 28)

    # Buttons
    play_btn = Button("Play", (WIN_W//2, WIN_H//2 + 20))
    howto_btn = Button("How to Play", (WIN_W//2, WIN_H//2 + 110))
    #maybe a settings button for this later on? Suggestions welcome
    quit_btn = Button("Quit", (WIN_W//2, WIN_H//2 + 200))

    show_help = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); sys.exit(0)

            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_RETURN, pg.K_SPACE) and not show_help:
                    run_game()
                elif event.key == pg.K_i:
                    show_help = True
                elif event.key in (pg.K_ESCAPE, pg.K_q):
                    if show_help:
                        show_help = False
                    else:
                        pg.quit(); sys.exit(0)

            if not show_help:
                if play_btn.clicked(event):
                    run_game()
                if howto_btn.clicked(event):
                    show_help = True
                if quit_btn.clicked(event):
                    pg.quit(); sys.exit(0)

        # Draw
        screen.fill(BG)

        if show_help:
            hdr = title_font.render("How to Play", True, TEXT)
            screen.blit(hdr, hdr.get_rect(center=(WIN_W//2, 140)))

            lines = [
                "• Use Arrow Keys or WASD to move.",
                "• Eat food to grow. Avoid walls and your own body.",
                "• Press Esc in the game to quit back here.",
                "",
                "Press Esc to return to the menu."
            ]
            y = 240
            for line in lines:
                label = small_font.render(line, True, TEXT if line else MUTED)
                screen.blit(label, label.get_rect(center=(WIN_W//2, y)))
                y += 40
        else:
            title = title_font.render("S N A K E", True, TEXT)
            screen.blit(title, title.get_rect(center=(WIN_W//2, WIN_H//2 - 120)))
            hint = small_font.render("Enter = Play   •   I = How to Play   •   Esc = Quit", True, MUTED)
            screen.blit(hint, hint.get_rect(center=(WIN_W//2, WIN_H//2 - 60)))

            play_btn.draw(screen, btn_font)
            howto_btn.draw(screen, btn_font)
            quit_btn.draw(screen, btn_font)

        footer = small_font.render("Launcher runs Snake.", True, MUTED)
        screen.blit(footer, (12, WIN_H - 30))

        pg.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
