import random
import config
import game_logic
from env_map_gen import MapGenerator
from env_wave_manager import WaveManager
from env_action_handler import ActionHandler


class TowerDefenseEnv:
    def __init__(self):
        self.action_space = list(range(301))
        self.level_idx = 1

        self.map_gen = MapGenerator(self)
        self.wave_mgr = WaveManager(self)
        self.action_handler = ActionHandler(self)

    def reset(self, level_idx=1):
        self.level_idx = level_idx
        self.rng = random.Random(level_idx)

        settings = config.LEVEL_SETTINGS.get(level_idx, config.LEVEL_SETTINGS[10])
        self.max_waves = settings["waves"]
        self.difficulty_multiplier = settings["hp_mod"]
        self.total_paths_count = settings["paths"]
        num_bases = settings["bases"]

        if num_bases == 1:
            config.BASES = [(5, 5)]
        else:
            config.BASES = [(2, 2), (7, 7)]

        self.map_gen.generate_spread_map(self.total_paths_count)

        self.grid = {}
        self.enemies = []
        self.gold = config.GOLD_START
        self.base_hp = config.BASE_MAX_HP
        self.wave = 1
        self.shopping_phase = True
        self.spawn_queue = []
        self.ticks = 0
        self.active_path_indices = []
        self.wave_plan = []

        self.wave_mgr.generate_wave_plan()

        print(f"--- Level {level_idx} Start (Seed: {level_idx}) ---")
        return self.get_state()

    def step(self, action):
        reward = 0
        done = False

        if self.shopping_phase:
            if action == 0:
                self.shopping_phase = False
                self.wave_mgr.start_combat_wave()
            elif action <= 200:
                reward = self.action_handler.process_build(action)
            else:
                reward = self.action_handler.process_sell_action(action)
        else:
            reward += game_logic.process_combat(self)

            alive_enemies = []
            for e in self.enemies:
                if e.hp > 0:
                    move_status = e.move()
                    if not move_status:
                        self.base_hp -= e.damage
                        reward -= 50
                    else:
                        alive_enemies.append(e)
            self.enemies = alive_enemies

            if self.spawn_queue and self.ticks % 5 == 0:
                self.enemies.append(self.spawn_queue.pop(0))
            self.ticks += 1

            if not self.spawn_queue and not self.enemies:
                if self.wave < self.max_waves:
                    self.wave += 1
                    self.shopping_phase = True
                    self.gold += 100 + (self.level_idx * 20)
                    self.wave_mgr.generate_wave_plan()
                else:
                    done = True
                    reward += 2000

        if self.base_hp <= 0:
            done = True
        return self.get_state(), reward, done

    def sell_tower(self, r, c):
        return self.action_handler.sell_tower(r, c)

    def get_state(self):
        phase_flag = 1 if self.shopping_phase else 0
        return (self.wave, self.gold, self.base_hp, len(self.enemies), phase_flag)
