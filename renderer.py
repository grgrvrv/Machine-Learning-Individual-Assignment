import pygame
import config
from renderer_ui import UIRenderer
from renderer_game import GameplayRenderer
from renderer_sidebar import SidebarRenderer


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen

        s = config.CELL_SIZE / 60

        def get_font(size, bold=False):
            f = pygame.font.Font(None, size)
            if bold:
                f.set_bold(True)
            return f

        self.fonts = {
            "small": get_font(int(14 * s)),
            "norm": get_font(int(18 * s)),
            "mid": get_font(int(22 * s)),
            "big": get_font(int(26 * s), bold=True),
            "title": get_font(int(42 * s), bold=True),
            "huge": get_font(int(60 * s), bold=True),
            "price": get_font(int(20 * s), bold=True),
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
