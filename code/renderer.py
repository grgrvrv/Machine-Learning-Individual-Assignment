import pygame
import config
from renderer_ui import UIRenderer
from renderer_game import GameplayRenderer
from renderer_sidebar import SidebarRenderer


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen

        s = config.CELL_SIZE / 60
        self.fonts = {
            "small": pygame.font.SysFont("Arial", int(14 * s)),
            "norm": pygame.font.SysFont("Arial", int(18 * s)),
            "mid": pygame.font.SysFont("Arial", int(22 * s)),
            "big": pygame.font.SysFont("Arial", int(26 * s), bold=True),
            "title": pygame.font.SysFont("Arial", int(42 * s), bold=True),
            "huge": pygame.font.SysFont("Arial", int(60 * s), bold=True),
            "price": pygame.font.SysFont("Arial", int(20 * s), bold=True),
        }

        self.ui = UIRenderer(screen, self.fonts)
        self.game = GameplayRenderer(screen, self.fonts)
        self.sidebar = SidebarRenderer(screen, self.fonts)

    @property
    def sell_btn_rect(self):
        return self.sidebar.sell_btn_rect

    def draw_menu(self):
        self.ui.draw_menu()

    def draw_level_select(self, mode):
        self.ui.draw_level_select(mode)

    def draw_intro_screen(self):
        self.ui.draw_intro_screen()

    def draw_result_screen(self, is_win, final_hp, max_hp):
        self.ui.draw_result_screen(is_win, final_hp, max_hp)

    def draw_game_scene(self, env, agent, mode, sell_mode=False):
        self.screen.fill((20, 20, 20))

        self.game.draw_grid_background(env)
        self.game.draw_path_lines(env)
        self.game.draw_towers(env)

        if sell_mode:
            self.game.draw_sell_selection(env)

        self.game.draw_enemies(env)

        self.game.draw_hover_info(env, mode)

        self.sidebar.draw_sidebar(env, agent, mode, sell_mode)

        pygame.display.flip()
