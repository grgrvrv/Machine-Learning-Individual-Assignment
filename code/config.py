# --- Basic Settings ---
GRID_SIZE = 10
CELL_SIZE = 80
SIDEBAR = 300
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE + SIDEBAR
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE

# --- Economy & Rules ---
GOLD_START = 650
BASE_MAX_HP = 5000
BASES = []

# --- Reward Parameters ---
REWARD_KILL = 0
REWARD_BUILD = 5
REWARD_UPGRADE = 5
REWARD_BASE_HIT = -50
REWARD_WIN = 2000
REWARD_INVALID = -5

# --- Path Containers ---
PATHS = []
PATH_COLORS = [
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (50, 255, 50),
    (255, 165, 0),
    (147, 112, 219),
]

# --- Level Configuration Table ---
LEVEL_SETTINGS = {
    1: {"waves": 10, "paths": 2, "hp_mod": 0.6, "bases": 1},
    2: {"waves": 15, "paths": 3, "hp_mod": 0.7, "bases": 1},
    3: {"waves": 20, "paths": 4, "hp_mod": 0.8, "bases": 1},
    4: {"waves": 25, "paths": 5, "hp_mod": 1.0, "bases": 1},
    5: {"waves": 30, "paths": 6, "hp_mod": 1.2, "bases": 1},
    6: {"waves": 35, "paths": 6, "hp_mod": 1.4, "bases": 2},
    7: {"waves": 40, "paths": 6, "hp_mod": 1.6, "bases": 2},
    8: {"waves": 45, "paths": 6, "hp_mod": 1.8, "bases": 2},
    9: {"waves": 50, "paths": 6, "hp_mod": 2.0, "bases": 2},
    10: {"waves": 50, "paths": 6, "hp_mod": 2.5, "bases": 2},
}

# --- 10 Enemy Types ---
ENEMY_TYPES = {
    1: {"hp": 40, "reward": 15, "dmg": 10, "color": (200, 200, 200)},
    2: {"hp": 100, "reward": 25, "dmg": 20, "color": (100, 200, 255)},
    3: {"hp": 250, "reward": 40, "dmg": 40, "color": (100, 255, 100)},
    4: {"hp": 600, "reward": 60, "dmg": 60, "color": (0, 150, 0)},
    5: {"hp": 1400, "reward": 100, "dmg": 100, "color": (255, 255, 100)},
    6: {"hp": 3000, "reward": 200, "dmg": 150, "color": (255, 165, 0)},
    7: {"hp": 7000, "reward": 400, "dmg": 250, "color": (255, 100, 100)},
    8: {"hp": 15000, "reward": 800, "dmg": 400, "color": (200, 0, 0)},
    9: {"hp": 35000, "reward": 1500, "dmg": 800, "color": (150, 0, 150)},
    10: {"hp": 100000, "reward": 5000, "dmg": 9999, "color": (0, 0, 0)},
}

# --- Dual Weapon Balance System ---
TOWER_TYPES = {
    "L": {
        1: {"name": "Melee I", "cost": 50, "dmg": 50, "range": 1.5},
        2: {"name": "Melee II", "cost": 120, "dmg": 130, "range": 1.5},
        3: {"name": "Melee III", "cost": 300, "dmg": 350, "range": 1.5},
        4: {"name": "Melee IV", "cost": 800, "dmg": 950, "range": 1.5},
        5: {"name": "Melee V", "cost": 2200, "dmg": 2600, "range": 1.5},
        6: {"name": "Melee VI", "cost": 5500, "dmg": 7000, "range": 1.5},
    },
    "R": {
        1: {"name": "Sniper I", "cost": 70, "dmg": 40, "range": 3.0},
        2: {"name": "Sniper II", "cost": 160, "dmg": 100, "range": 3.0},
        3: {"name": "Sniper III", "cost": 350, "dmg": 280, "range": 3.0},
        4: {"name": "Sniper IV", "cost": 850, "dmg": 650, "range": 3.0},
        5: {"name": "Sniper V", "cost": 2400, "dmg": 1800, "range": 3.0},
        6: {"name": "Sniper VI", "cost": 5800, "dmg": 5000, "range": 3.0},
    },
}
