import pygame
import config
from renderer_utils import RenderUtils


class SidebarRenderer:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        bx = config.GRID_SIZE * config.CELL_SIZE + 15
        btn_y = config.WINDOW_HEIGHT - 85
        self.sell_btn_rect = pygame.Rect(bx, btn_y, 250, 45)

    def draw_sidebar(self, env, agent, mode, sell_mode):
        bx = config.GRID_SIZE * config.CELL_SIZE + 15

        self.screen.blit(
            self.fonts["big"].render(f"MODE: {mode}", True, (100, 200, 255)), (bx, 10)
        )
        self.screen.blit(
            self.fonts["title"].render(f"LEVEL: {env.level_idx}", True, (255, 215, 0)),
            (bx, 35),
        )

        y = 85
        if env.shopping_phase:
            pygame.draw.rect(
                self.screen, (20, 35, 25), (bx - 5, y - 5, 280, 240), border_radius=5
            )
            self.screen.blit(
                self.fonts["big"].render("WAVE INTEL", True, (100, 255, 100)), (bx, y)
            )
            y += 35

            path_intel = {}
            for p in env.wave_plan:
                pid = p.get("path_idx", 0)
                lv = p["level"]
                if pid not in path_intel:
                    path_intel[pid] = {}
                if lv not in path_intel[pid]:
                    path_intel[pid][lv] = 0
                path_intel[pid][lv] += 1

            for p_idx in sorted(path_intel.keys()):
                c = config.PATH_COLORS[p_idx % len(config.PATH_COLORS)]
                pygame.draw.rect(self.screen, c, (bx, y + 8, 10, 10))

                current_x = bx + 25

                for lv in sorted(path_intel[p_idx].keys()):
                    count = path_intel[p_idx][lv]
                    e_stats = config.ENEMY_TYPES[lv]
                    e_color = e_stats["color"]

                    cx, cy = current_x, y + 13
                    RenderUtils.draw_enemy_shape(self.screen, cx, cy, lv, e_color)

                    r, g, b = e_color
                    luminance = 0.299 * r + 0.587 * g + 0.114 * b
                    text_color = (0, 0, 0) if luminance > 128 else (255, 255, 255)

                    lvl_surf = self.fonts["small"].render(str(lv), True, text_color)
                    lx = cx - lvl_surf.get_width() // 2
                    ly = cy - lvl_surf.get_height() // 2
                    self.screen.blit(lvl_surf, (lx, ly))

                    txt = self.fonts["small"].render(f"x{count}", True, (220, 220, 220))
                    self.screen.blit(txt, (current_x + 15, y + 5))

                    current_x += 50

                y += 30

            y = 330
            sub = "AI: THINKING..." if mode == "AI" else "[SPACE] Start Wave"
            self.screen.blit(
                self.fonts["mid"].render(sub, True, (200, 200, 200)), (bx, y)
            )
        else:
            self.screen.blit(
                self.fonts["big"].render("COMBAT PHASE", True, (255, 50, 50)), (bx, y)
            )
            y += 35
            self.screen.blit(
                self.fonts["mid"].render("Defending Routes:", True, (200, 200, 200)),
                (bx, y),
            )
            y += 25

            start_x = bx
            for p_idx in env.active_path_indices:
                c = config.PATH_COLORS[p_idx % len(config.PATH_COLORS)]
                pygame.draw.rect(self.screen, c, (start_x, y, 20, 10))
                start_x += 25

            y += 40
            self.screen.blit(
                self.fonts["mid"].render("Engaging...", True, (150, 150, 150)), (bx, y)
            )

        y = 380
        self.screen.blit(
            self.fonts["mid"].render(
                f"Wave: {env.wave}/{env.max_waves}", True, (255, 255, 255)
            ),
            (bx, y),
        )
        y += 25
        self.screen.blit(
            self.fonts["mid"].render(f"Base HP: {env.base_hp}", True, (255, 255, 255)),
            (bx, y),
        )
        y += 25
        self.screen.blit(
            self.fonts["mid"].render(f"Gold: {env.gold}", True, (255, 215, 0)), (bx, y)
        )

        y += 35
        pygame.draw.line(self.screen, (100, 100, 100), (bx, y), (bx + 250, y), 2)
        y += 10
        self.screen.blit(
            self.fonts["mid"].render("L-TOWER", True, (100, 200, 255)), (bx, y)
        )
        self.screen.blit(
            self.fonts["mid"].render("R-TOWER", True, (255, 100, 255)),
            (bx + 140, y),
        )
        y += 25

        for lv in range(1, 7):
            c = (255, 255, 255) if env.shopping_phase else (150, 150, 150)
            if lv in config.TOWER_TYPES["L"]:
                l = config.TOWER_TYPES["L"][lv]
                r = config.TOWER_TYPES["R"][lv]

                self.screen.blit(
                    self.fonts["price"].render(f"Lv{lv}: ${l['cost']}", True, c),
                    (bx, y),
                )
                self.screen.blit(
                    self.fonts["price"].render(f"Lv{lv}: ${r['cost']}", True, c),
                    (bx + 140, y),
                )

                y += 30

        if sell_mode:
            btn_color, btn_txt = (220, 50, 50), "CANCEL SELL"
        else:
            btn_color, btn_txt = (60, 60, 80), "SELL MODE"
        pygame.draw.rect(self.screen, btn_color, self.sell_btn_rect, border_radius=5)
        pygame.draw.rect(
            self.screen,
            (255, 255, 255) if env.shopping_phase else (100, 100, 100),
            self.sell_btn_rect,
            2,
            border_radius=5,
        )

        txt_surf = self.fonts["big"].render(btn_txt, True, (255, 255, 255))
        self.screen.blit(
            txt_surf,
            (
                self.sell_btn_rect.centerx - txt_surf.get_width() // 2,
                self.sell_btn_rect.centery - txt_surf.get_height() // 2,
            ),
        )
        self.screen.blit(
            self.fonts["mid"].render("[ESC] Back", True, (100, 100, 100)),
            (bx, config.WINDOW_HEIGHT - 30),
        )
