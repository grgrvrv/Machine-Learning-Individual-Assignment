import pygame
import config
from renderer_utils import RenderUtils


class UIRenderer:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

    def draw_menu(self):
        self.screen.fill((20, 20, 30))
        title = self.fonts["title"].render("Tower Defense RL", True, (255, 215, 0))
        RenderUtils.draw_centered(self.screen, title, 80)

        txt1 = self.fonts["big"].render("1. AI (Untrained / Learning)", True, (150, 150, 255))
        txt2 = self.fonts["big"].render("2. AI (Pre-trained / Expert)", True, (100, 255, 100))
        txt3 = self.fonts["big"].render("3. Player Manual", True, (255, 200, 100))
        txt4 = self.fonts["big"].render("4. Game Database & Info", True, (255, 255, 100))

        RenderUtils.draw_centered(self.screen, txt1, 200)
        RenderUtils.draw_centered(self.screen, txt2, 260)
        RenderUtils.draw_centered(self.screen, txt3, 320)
        RenderUtils.draw_centered(self.screen, txt4, 380)

        hint = self.fonts["norm"].render("[ESC] Quit Game", True, (150, 150, 150))
        RenderUtils.draw_centered(self.screen, hint, 520)
        pygame.display.flip()

    def draw_level_select(self, mode):
        self.screen.fill((15, 15, 25))
        title = self.fonts["title"].render(f"SELECT LEVEL ({mode})", True, (255, 255, 255))
        RenderUtils.draw_centered(self.screen, title, 30)
        start_y = 100
        for i in range(1, 11):
            key_name = str(i) if i < 10 else "0"
            settings = config.LEVEL_SETTINGS.get(i, config.LEVEL_SETTINGS[10])
            paths_count = settings["paths"]
            diff_color = (255, max(100, 255 - i * 20), max(100, 255 - i * 20))

            text = f"[{key_name}] Lv{i} | Waves: {settings['waves']} | Paths: {paths_count}"
            label = self.fonts["mid"].render(text, True, diff_color)

            col = 0 if i <= 5 else 1
            row = (i - 1) % 5
            x = 80 + col * 450
            y = start_y + row * 70

            pygame.draw.rect(self.screen, (50, 50, 60), (x - 10, y - 10, 420, 50))
            self.screen.blit(label, (x, y + 12))

        hint = self.fonts["mid"].render("[1-9, 0] Start  |  [ESC] Back to Menu", True, (255, 215, 0))
        RenderUtils.draw_centered(self.screen, hint, 500)
        pygame.display.flip()

    def draw_intro_screen(self):
        self.screen.fill((15, 20, 25))
        title = self.fonts["title"].render("GAME DATABASE & RL INFO", True, (255, 215, 0))
        RenderUtils.draw_centered(self.screen, title, 30)

        lines = [
            "--- PROJECT OVERVIEW ---",
            "This is a Q-Learning based Tower Defense simulation.",
            "Objective: Defend the base from enemy waves using limited gold.",
            "",
            "--- AI MODES ---",
            "[1] Untrained Agent: High exploration. The agent learns from scratch",
            "    via trial and error, adjusting its Q-table based on penalties.",
            "[2] Expert Agent: Zero exploration. Uses an optimized Q-table injected",
            "    with heuristics (ROI and terrain coverage) for perfect defense.",
            "",
            "--- WEAPON ARSENAL ---",
            "> MELEE TOWER (L-Tower):",
            "  - Range: 1.5 Grids",
            "  - Trait: High Damage. Optimal for choke points and path intersections.",
            "> SNIPER TOWER (R-Tower):",
            "  - Range: 3.0 Grids",
            "  - Trait: Broad Coverage. Lower damage but hits enemies from afar.",
            "",
            "--- CONTROLS (PLAYER MODE) ---",
            "Left Click: Build / Upgrade (L-Tower)  |  Right Click: Build Sniper (R-Tower)",
            "Spacebar: Start Combat Wave            |  ESC: Back / Quit"
        ]

        start_y = 100
        for i, text in enumerate(lines):
            color = (200, 200, 200)
            if text.startswith("---"):
                color = (100, 200, 255)
            elif text.startswith(">"):
                color = (255, 100, 100) if "MELEE" in text else (100, 255, 100)

            surf = self.fonts["norm"].render(text, True, color)
            self.screen.blit(surf, (80, start_y + i * 28))

        footer = self.fonts["big"].render("PRESS [ESC] TO RETURN TO MENU", True, (150, 150, 150))
        RenderUtils.draw_centered(self.screen, footer, 740)
        pygame.display.flip()

    def draw_result_screen(self, is_win, final_hp, max_hp):
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        if is_win:
            txt = self.fonts["huge"].render("VICTORY", True, (255, 215, 0))
        else:
            txt = self.fonts["huge"].render("DEFEAT", True, (255, 50, 50))

        RenderUtils.draw_centered(self.screen, txt, 100)

        stars = 0
        if is_win:
            pct = final_hp / max_hp
            stars = 3 if pct >= 1.0 else (2 if pct >= 0.5 else 1)
            cx = config.WINDOW_WIDTH // 2
            for i in range(3):
                offset = (i - 1) * 100
                color = (255, 215, 0) if i < stars else (50, 50, 50)
                RenderUtils.draw_star(self.screen, cx + offset, 200, 40, color)

            eval_txt = ["", "SURVIVOR", "EXCELLENT", "PERFECT"][stars]
            RenderUtils.draw_centered(self.screen, self.fonts["big"].render(eval_txt, True, (200, 200, 255)), 280)

        hint = self.fonts["big"].render("Press [4] Replay | [ESC] Menu", True, (255, 255, 255))
        RenderUtils.draw_centered(self.screen, hint, 400)
        pygame.display.flip()