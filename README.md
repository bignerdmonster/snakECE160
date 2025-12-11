# [snakECE160](https://github.com/bignerdmonster/snakECE160) – Final Project Overview

This repository contains a Pygame-based reimagining of the classic Snake arcade game. It adds an animated neon-styled menu, unlockable mid-game events, multiple backgrounds, music cues, and quick-time mini-events to keep runs dynamic. Use this README as the required project handout that accompanies the presentation, zip submission, and demo.

## Program Summary
- **Goal:** Deliver a visual, interactive Python game that showcases event-driven programming, state management, and creative UI polish suitable for a 15–20 minute final presentation.
- **Gameplay:** Guide a continuously moving snake across a 61×61 grid, collect apples to grow, and survive as long as possible while optional quick-time events (QTEs), pop-up messages, and music boxes appear as milestones are reached.
- **Visuals & Audio:** Animated starfield menu with glowing buttons, parallax backgrounds that change as the score increases, and sound effects/music for apple collection, game start/over, and special events.
- **Key Files:**
  - `snakeCore.py` – main game loop, snake mechanics, progression triggers, and asset loading.
  - `menu.py` – animated main menu, help screen, and game-over screen UI components.
  - `images/` & `media/` – art, music, and fonts used by the game.

## Setup & Run Instructions
1. **Install Python 3.14.x** and ensure `pip` is available. -- https://python.org/downloads
2. **Install dependencies:**
   ```bash
   pip install pygame-ce
   ```
3. **Run the game:**
   ```bash
   python snakeCore.py
   ```
4. **Controls in-game:**
   - Move: **W/A/S/D** or arrow keys (head cannot reverse direction instantly).
   - Toggle quick testing aids: `Enter` spawns an apple, `\` spawns a pop-up, `]` grows the snake, `Right Shift` forces a QTE.
   - Pause/quit to menu: **Esc** during gameplay. Close window to exit completely.
5. **Menu navigation:**
   - **Enter** or click **Play** to start, **H** or **How to Play** for instructions, **Esc/Quit** to leave.
6. **Assets:** Keep the `images/` and `media/` folders alongside the Python files so that fonts, sprites, and audio load correctly.

## Main Features to Highlight During Presentation
- Animated neon main menu with hover states, starfield parallax, and an instructional overlay.
- Modular UI components (`Button`, `Menu`, `GameOverScreen`) that handle both mouse and keyboard input.
- Grid-based snake movement with wrap-around edges, growth tracking, and tail rendering.
- Progression system that unlocks extras at specific lengths (pop-ups, music box, QTE challenges, golden/poison apples).
- Background cycling tied to score milestones and a dedicated game-over experience with shake effects.

## Team Member Contributions
"List each teammate and the module or feature they owned so grading aligns with individual presentations."
- **Felix (bignerdmonster/flexi b):** Core snake logic, overall game loop integration, and GameObject manager.
- **Alan (ToastPixel):** Visual polish (background swaps, neon aesthetic), quick-time event implementation, and QTE/milestone tuning.
- **Achilles (akj7-debug):** Bug fixes, testing assists, and supporting tweaks to controls or timers.

## Troubleshooting
- If fonts/audio fail to load, confirm working directory is the repository root so relative paths to `images/` and `media/` resolve correctly.
- For performance issues, lower the window size in `snakeCore.py` by adjusting `SCREEN_WIDTH`/`SCREEN_HEIGHT`, or disable `vsync` in the display creation (**NOT RECCOMENDED**)
