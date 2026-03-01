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
                self.screen, (20, 35, 25), (bx - 5, y - 5, 280, 200), border_radius=5
            )
            self.screen.blit(
                self.fonts["big"].render("WAVE INTEL", True, (255, 100, 100)), (bx, y)
            )
            y += 35
            
            if env.wave_plan:
                threats = {}
                for e in env.wave_plan:
                    threats[e['level']] = threats.get(e['level'], 0) + 1
                for lv, count in sorted(threats.items()):
                    self.screen.blit(
                        self.fonts["norm"].render(f"Enemy Lv{lv} x {count}", True, (200, 200, 200)), (bx, y)
                    )
                    y += 25
            else:
                self.screen.blit(
                    self.fonts["norm"].render("Preparing...", True, (150, 150, 150)), (bx, y)
                )
                y += 25
                
            y = 300
            self.screen.blit(
                self.fonts["big"].render("SHOP / UPGRADES", True, (255, 215, 0)), (bx, y)
            )
            y += 35

            self.screen.blit(self.fonts["mid"].render("MELEE (L)", True, (255, 100, 100)), (bx, y))
            self.screen.blit(self.fonts["mid"].render("SNIPER (R)", True, (100, 255, 100)), (bx + 140, y))
            y += 25

            range_l = config.TOWER_TYPES["L"][1]["range"]
            range_r = config.TOWER_TYPES["R"][1]["range"]
            self.screen.blit(self.fonts["small"].render(f"Range: {range_l}", True, (180, 180, 180)), (bx, y))
            self.screen.blit(self.fonts["small"].render(f"Range: {range_r}", True, (180, 180, 180)), (bx + 140, y))
            y += 20

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

        else:
            self.screen.blit(
                self.fonts["big"].render("COMBAT IN PROGRESS", True, (255, 50, 50)), (bx, y)
            )
            y += 40

        y = config.WINDOW_HEIGHT - 200
        self.screen.blit(
            self.fonts["huge"].render(f"${env.gold}", True, (255, 215, 0)), (bx, y)
        )
        y += 60
        hp_color = (50, 255, 50) if env.base_hp > 2000 else (255, 50, 50)
        self.screen.blit(
            self.fonts["title"].render(f"HP: {env.base_hp}", True, hp_color), (bx, y)
        )

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
        txt_rect = txt_surf.get_rect(center=self.sell_btn_rect.center)
        self.screen.blit(txt_surf, txt_rect)
