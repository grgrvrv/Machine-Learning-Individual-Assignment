import math
import config


def process_combat(env):
    total_reward = 0
    for pos, tower in env.grid.items():
        if tower.cooldown > 0:
            tower.cooldown -= 1
            continue
        target = None
        for enemy in env.enemies:
            if enemy.hp <= 0:
                continue

            dist = _calculate_distance(tower.get_pos(), enemy.get_pos())
            if dist <= tower.range:
                target = enemy
                break
        if target:
            target.hp -= tower.damage
            tower.cooldown = tower.max_cooldown
            if target.hp <= 0:
                total_reward += target.reward
                env.gold += target.reward
    return total_reward


def _calculate_distance(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return math.sqrt((r1 - r2) ** 2 + (c1 - c2) ** 2)
