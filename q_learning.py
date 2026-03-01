import config
import math
import random
from collections import defaultdict


class MasterAI:
    def __init__(
        self, action_size, learning_rate=0.1, discount_factor=0.99, epsilon=0.05, use_heuristics=True
    ):
        self.action_size = action_size
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.use_heuristics = use_heuristics

        self.q_table = {}
        self.terrain_cache = {}
        self._analyze_static_terrain()

    def _analyze_static_terrain(self):
        range_l = config.TOWER_TYPES["L"][1]["range"]
        range_r = config.TOWER_TYPES["R"][1]["range"]

        for r in range(config.GRID_SIZE):
            for c in range(config.GRID_SIZE):
                if (r, c) in config.BASES:
                    continue
                is_path = False
                for p in config.PATHS:
                    if (r, c) in p:
                        is_path = True
                        break
                if is_path:
                    continue

                cov_l = {}
                for p_idx, path in enumerate(config.PATHS):
                    hits = 0
                    for pr, pc in path:
                        if math.sqrt((r - pr) ** 2 + (c - pc) ** 2) <= (range_l - 0.1):
                            hits += 1
                    if hits > 0:
                        cov_l[p_idx] = hits

                cov_r = {}
                for p_idx, path in enumerate(config.PATHS):
                    hits = 0
                    for pr, pc in path:
                        if math.sqrt((r - pr) ** 2 + (c - pc) ** 2) <= (range_r - 0.1):
                            hits += 1
                    if hits > 0:
                        cov_r[p_idx] = hits

                min_dist = 999
                for br, bc in config.BASES:
                    d = math.sqrt((r - br) ** 2 + (c - bc) ** 2)
                    min_dist = min(min_dist, d)

                self.terrain_cache[(r, c)] = {
                    "coverage_l": cov_l,
                    "coverage_r": cov_r,
                    "dist_to_base": min_dist,
                    "is_guard": (min_dist <= 2.5),
                    "is_corner": (sum(cov_l.values()) >= 3),
                }

    def get_state_key(self, env):
        if not env.shopping_phase:
            return None
        active_paths = tuple(sorted(env.active_path_indices))
        if env.gold < 50: gb = 0
        elif env.gold < 150: gb = 1
        elif env.gold < 400: gb = 2
        elif env.gold < 1000: gb = 3
        else: gb = 4
        return (active_paths, gb)

    def _init_q_values(self, env, state):
        if self.use_heuristics:
            return self._calculate_perfect_q_values(env)
        else:
            q = {a: 10.0 for a in range(self.action_size)}
            q[0] = 5.0
            return q

    def choose_action(self, env):
        if not env.shopping_phase:
            return 0

        state = self.get_state_key(env)
        if state is None: return 0

        if state not in self.q_table:
            self.q_table[state] = self._init_q_values(env, state)

        if random.random() < self.epsilon:
            if env.gold >= 50:
                return random.randint(1, self.action_size - 1)
            return random.randint(0, self.action_size - 1)
        else:
            action_values = self.q_table[state]
            return max(action_values, key=action_values.get)

    def learn(self, env, state, action, reward, next_state):
        if state is None or next_state is None: return
        if state not in self.q_table: self.q_table[state] = self._init_q_values(env, state)
        if next_state not in self.q_table: self.q_table[next_state] = self._init_q_values(env, next_state)

        current_q = self.q_table[state].get(action, 0.0)
        next_max_q = max(self.q_table[next_state].values())

        new_q = current_q + self.lr * (reward + self.gamma * next_max_q - current_q)
        self.q_table[state][action] = new_q

    def _calculate_perfect_q_values(self, env):
        q_values = {a: -99999.0 for a in range(self.action_size)}
        q_values[0] = 1.0 

        path_threats = defaultdict(int)
        if env.wave_plan:
            for enemy_info in env.wave_plan:
                path_threats[enemy_info.get("path_idx", 0)] += enemy_info["hp"]

        total_threat = sum(path_threats.values())
        if total_threat == 0: return q_values

        def calculate_score(dmg, cost, weighted_hits, dist, is_guard):
            roi = dmg / max(1, cost)
            urgency = 1.0 + (15.0 / (dist + 1.0))
            if is_guard: urgency *= 3.0
            return roi * weighted_hits * urgency

        max_buy_score = 0
        for pos, terrain in self.terrain_cache.items():
            dist = terrain["dist_to_base"]
            is_guard = terrain["is_guard"]

            if pos in env.grid: 
                tower = env.grid[pos]
                if tower.level < 6:
                    cov = terrain["coverage_l"] if tower.t_type == "L" else terrain["coverage_r"]
                    current_hits = sum([hits * path_threats[p] for p, hits in cov.items() if path_threats[p] > 0])
                    if current_hits > 0:
                        nxt = config.TOWER_TYPES[tower.t_type][tower.level + 1]
                        if env.gold >= nxt["cost"]:
                            score = calculate_score(nxt["dmg"] - tower.damage, nxt["cost"], current_hits, dist, is_guard)
                            score *= 3.0
                            aid = (pos[0] * config.GRID_SIZE + pos[1]) + 1 + (100 if tower.t_type == "R" else 0)
                            q_values[aid] = 1000.0 + score
                            max_buy_score = max(max_buy_score, score)
            else: 
                for t_type, offset in [("L", 0), ("R", 100)]:
                    cov = terrain["coverage_l"] if t_type == "L" else terrain["coverage_r"]
                    hits_val = sum([hits * path_threats[p] for p, hits in cov.items() if path_threats[p] > 0])
                    if hits_val > 0:
                        cfg = config.TOWER_TYPES[t_type][1]
                        if env.gold >= cfg["cost"]:
                            score = calculate_score(cfg["dmg"], cfg["cost"], hits_val, dist, is_guard)
                            if is_guard and t_type == "L": score *= 2.0
                            elif t_type == "R" and hits_val < 5: score *= 0.5 
                            aid = (pos[0] * config.GRID_SIZE + pos[1]) + 1 + offset
                            q_values[aid] = 1000.0 + score
                            max_buy_score = max(max_buy_score, score)

        if max_buy_score > 0.1:
            q_values[0] = -99999.0

        return q_values