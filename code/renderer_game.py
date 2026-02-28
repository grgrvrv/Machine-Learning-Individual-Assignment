import pygame
import config
import math
from renderer_utils import RenderUtils


class GameplayRenderer:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts

    def draw_grid_background(self, env):
        for r in range(config.GRID_SIZE):
            for c in range(config.GRID_SIZE):
                rect = pygame.Rect(
                    c * config.CELL_SIZE,
                    r * config.CELL_SIZE,
                    config.CELL_SIZE - 1,
                    config.CELL_SIZE - 1,
                )
                if (r, c) in config.BASES:
                    pygame.draw.rect(self.screen, (30, 144, 255), rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)
                    cx, cy = rect.centerx, rect.centery
                    pygame.draw.polygon(
                        self.screen,
                        (200, 200, 255),
                        [(cx, cy - 20), (cx - 20, cy), (cx + 20, cy)],
                    )
                    pygame.draw.rect(
                        self.screen, (150, 150, 200), (cx - 15, cy, 30, 20)
                    )
                else:
                    is_active = False
                    is_path = False
                    for idx, path in enumerate(config.PATHS):
                        if (r, c) in path:
                            is_path = True
                            if idx in env.active_path_indices:
                                is_active = True
                                break

                    color = (
                        (60, 30, 30)
                        if is_active
                        else ((40, 40, 40) if is_path else (25, 25, 25))
                    )
                    pygame.draw.rect(self.screen, color, rect)

    def draw_path_lines(self, env):
        if env.shopping_phase or len(env.enemies) > 0:
            for p_idx in env.active_path_indices:
                if p_idx < len(config.PATHS):
                    path = config.PATHS[p_idx]
                    color = config.PATH_COLORS[p_idx % len(config.PATH_COLORS)]
                    points = [
                        (
                            c * config.CELL_SIZE + config.CELL_SIZE // 2,
                            r * config.CELL_SIZE + config.CELL_SIZE // 2,
                        )
                        for r, c in path
                    ]
                    if len(points) > 1:
                        pygame.draw.lines(self.screen, color, False, points, 4)
                        pygame.draw.circle(self.screen, color, points[0], 8)

    def draw_towers(self, env):
        for pos, tower in env.grid.items():
            r, c = pos
            cx = c * config.CELL_SIZE + config.CELL_SIZE // 2
            cy = r * config.CELL_SIZE + config.CELL_SIZE // 2
            self._draw_tower_icon(tower, cx, cy)

    def _draw_tower_icon(self, tower, cx, cy):
        level = tower.level
        if tower.t_type == "L":
            base_color = (50, 100, 200 + level * 8)
            spike_color = (180, 220, 255)
            pygame.draw.circle(self.screen, base_color, (cx, cy), 16)
            num_spikes = 2 + level
            spike_len = 16
            for i in range(num_spikes):
                ang = math.radians(360 / num_spikes * i)
                tx, ty = cx + math.cos(ang) * (spike_len + 4), cy + math.sin(ang) * (
                    spike_len + 4
                )
                pygame.draw.line(self.screen, spike_color, (cx, cy), (tx, ty), 3)
        else:
            base_color = (150 + level * 15, 50, 150)
            pygame.draw.rect(self.screen, base_color, (cx - 12, cy - 12, 24, 24))
            barrel_len = 22
            for i in range(level):
                ang = math.radians(360 / level * i - 90)
                ex, ey = (
                    cx + math.cos(ang) * barrel_len,
                    cy + math.sin(ang) * barrel_len,
                )
                pygame.draw.line(self.screen, (255, 100, 200), (cx, cy), (ex, ey), 4)

        label = self.fonts["norm"].render(str(level), True, (0, 0, 0))
        self.screen.blit(
            label, (cx - label.get_width() // 2, cy - label.get_height() // 2)
        )

    def draw_enemies(self, env):
        for e in env.enemies:
            cx = e.pos[1] * config.CELL_SIZE + 30
            cy = e.pos[0] * config.CELL_SIZE + 30
            RenderUtils.draw_enemy_shape(self.screen, cx, cy, e.level, e.color, e)

    def draw_sell_selection(self, env):
        mx, my = pygame.mouse.get_pos()
        if mx < config.GRID_SIZE * config.CELL_SIZE:
            c, r = mx // config.CELL_SIZE, my // config.CELL_SIZE
            if (r, c) in env.grid:
                tower = env.grid[(r, c)]
                rect = pygame.Rect(
                    c * config.CELL_SIZE,
                    r * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE,
                )

                if tower.creation_wave == env.wave:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect, 3)

    def draw_hover_info(self, env, mode):
        mx, my = pygame.mouse.get_pos()
        if (
            mx < config.GRID_SIZE * config.CELL_SIZE
            and my < config.GRID_SIZE * config.CELL_SIZE
        ):
            c = mx // config.CELL_SIZE
            r = my // config.CELL_SIZE

            draw_range = 0
            is_existing = False

            if (r, c) in env.grid:
                t = env.grid[(r, c)]
                draw_range = t.range
                is_existing = True

                sell_status = (
                    "[SELLABLE]" if t.creation_wave == env.wave else "[LOCKED]"
                )

                RenderUtils.draw_tooltip(
                    self.screen,
                    self.fonts["big"],
                    self.fonts["mid"],
                    mx,
                    my,
                    f"Lv{t.level} {config.TOWER_TYPES[t.t_type][t.level]['name']}",
                    f"Rng:{t.range} {sell_status}",
                )

            if is_existing:
                cx = c * config.CELL_SIZE + config.CELL_SIZE // 2
                cy = r * config.CELL_SIZE + config.CELL_SIZE // 2
                pixel_radius = int(draw_range * config.CELL_SIZE)
                surf = pygame.Surface(
                    (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA
                )
                pygame.draw.circle(surf, (255, 255, 255, 40), (cx, cy), pixel_radius)
                pygame.draw.circle(surf, (255, 255, 255, 80), (cx, cy), pixel_radius, 1)

                range_int = int(draw_range) + 1
                for dr in range(-range_int, range_int + 1):
                    for dc in range(-range_int, range_int + 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < config.GRID_SIZE and 0 <= nc < config.GRID_SIZE:
                            dist = math.sqrt(dr**2 + dc**2)
                            if dist <= draw_range:
                                hl_rect = pygame.Rect(
                                    nc * config.CELL_SIZE,
                                    nr * config.CELL_SIZE,
                                    config.CELL_SIZE,
                                    config.CELL_SIZE,
                                )
                                pygame.draw.rect(surf, (100, 255, 100, 50), hl_rect)
                                pygame.draw.rect(surf, (100, 255, 100, 100), hl_rect, 1)
                self.screen.blit(surf, (0, 0))
