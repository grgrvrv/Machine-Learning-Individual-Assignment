import config
from enemy import Enemy


class WaveManager:
    def __init__(self, env):
        self.env = env

    def generate_wave_plan(self):
        """
        Creates the plan for the upcoming wave (Enemy types, HP, assigned paths).
        """
        progress = (self.env.wave - 1) / max(1, self.env.max_waves - 1)

        num_active = max(
            1,
            min(
                self.env.total_paths_count,
                1 + int(progress * self.env.total_paths_count),
            ),
        )

        self.env.active_path_indices = self.env.rng.sample(
            range(self.env.total_paths_count), num_active
        )
        self.env.active_path_indices.sort()

        evolution_stage = 1.0 + progress * (self.env.level_idx - 1)
        base_type = int(evolution_stage)
        next_type = min(10, base_type + 1)
        spawn_next_prob = evolution_stage - base_type

        hp_budget = 400 * (self.env.wave**1.3) * self.env.difficulty_multiplier

        self.env.wave_plan = []
        while hp_budget > 0:
            lv = next_type if self.env.rng.random() < spawn_next_prob else base_type
            lv = max(1, min(10, lv))

            enemy_hp = config.ENEMY_TYPES[lv]["hp"]
            if hp_budget < enemy_hp and lv > 1:
                lv = 1
                enemy_hp = config.ENEMY_TYPES[1]["hp"]

            if hp_budget < 50:
                break

            assigned_path = self.env.rng.choice(self.env.active_path_indices)

            self.env.wave_plan.append(
                {
                    "level": lv,
                    "hp": int(enemy_hp),
                    "color": config.ENEMY_TYPES[lv]["color"],
                    "path_idx": assigned_path,
                }
            )
            hp_budget -= enemy_hp

    def start_combat_wave(self):
        """
        Converts the wave plan into actual Enemy objects in the spawn queue.
        """
        self.env.ticks = 0
        for plan in self.env.wave_plan:
            e = Enemy(plan["path_idx"], plan["level"])
            e.hp = plan["hp"]
            e.max_hp = plan["hp"]
            self.env.spawn_queue.append(e)
        self.env.rng.shuffle(self.env.spawn_queue)
