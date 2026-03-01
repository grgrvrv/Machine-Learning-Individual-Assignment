import config
from tower import Tower


class ActionHandler:
    def __init__(self, env):
        self.env = env

    def process_build(self, action):
        if action == 0:
            return 0

        target_type = "L" if action <= 100 else "R"
        grid_idx = (action - 1) if action <= 100 else (action - 101)
        r, c = divmod(grid_idx, config.GRID_SIZE)

        if (r, c) in config.BASES:
            return -1
        for path in config.PATHS:
            if (r, c) in path:
                return -1

        if (r, c) in self.env.grid:
            tower = self.env.grid[(r, c)]
            if tower.t_type == target_type and tower.level < 6:
                cost = config.TOWER_TYPES[tower.t_type][tower.level + 1]["cost"]
                if self.env.gold >= cost:
                    self.env.gold -= cost
                    tower.upgrade()
                    return 10
            return -1

        cost = config.TOWER_TYPES[target_type][1]["cost"]
        if self.env.gold >= cost:
            self.env.grid[(r, c)] = Tower(r, c, target_type, self.env.wave)
            self.env.gold -= cost
            return 5
        return -1

    def process_sell_action(self, action):
        grid_idx = action - 201
        r, c = divmod(grid_idx, config.GRID_SIZE)
        success, refund = self.sell_tower(r, c)
        if success:
            return 2
        return -5

    def sell_tower(self, r, c):
        if (r, c) in self.env.grid:
            tower = self.env.grid[(r, c)]

            if tower.creation_wave != self.env.wave:
                return False, 0

            current_cost = config.TOWER_TYPES[tower.t_type][tower.level]["cost"]
            refund = current_cost

            self.env.gold += refund
            del self.env.grid[(r, c)]
            return True, refund
        return False, 0
