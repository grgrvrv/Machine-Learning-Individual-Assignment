import pygame
import math
import config


class RenderUtils:
    @staticmethod
    def draw_centered(screen, surface, y):
        x = config.WINDOW_WIDTH // 2 - surface.get_width() // 2
        screen.blit(surface, (x, y))

    @staticmethod
    def draw_star(screen, cx, cy, radius, color):
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = radius if i % 2 == 0 else radius * 0.4
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        pygame.draw.polygon(screen, color, points)

    @staticmethod
    def draw_tooltip(screen, font_big, font_mid, x, y, title, sub):
        w, h = 180, 60
        rx = x + 15 if x + 15 + w < config.WINDOW_WIDTH else x - 15 - w
        pygame.draw.rect(screen, (0, 0, 0), (rx, y, w, h))
        pygame.draw.rect(screen, (255, 255, 255), (rx, y, w, h), 2)
        screen.blit(font_big.render(title, True, (255, 200, 50)), (rx + 5, y + 5))
        screen.blit(font_mid.render(sub, True, (200, 200, 200)), (rx + 5, y + 30))

    @staticmethod
    def draw_enemy_shape(screen, cx, cy, level, color, enemy_obj=None):
        size = 14 + (level // 2)
        if level <= 2:
            pygame.draw.circle(screen, color, (int(cx), int(cy)), size)
        elif level <= 4:
            pygame.draw.rect(screen, color, (cx - size, cy - size, size * 2, size * 2))
        elif level <= 6:
            pts = [(cx, cy - size), (cx - size, cy + size), (cx + size, cy + size)]
            pygame.draw.polygon(screen, color, pts)
        else:
            pts = []
            for i in range(6):
                ang = math.radians(60 * i)
                pts.append((cx + size * math.cos(ang), cy + size * math.sin(ang)))
            pygame.draw.polygon(screen, color, pts)

        if enemy_obj:
            hp_pct = max(0, enemy_obj.hp / enemy_obj.max_hp)
            pygame.draw.rect(screen, (80, 0, 0), (cx - 20, cy - size - 8, 40, 4))
            pygame.draw.rect(
                screen, (0, 255, 0), (cx - 20, cy - size - 8, 40 * hp_pct, 4)
            )
