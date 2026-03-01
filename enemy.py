import config
import random

class Enemy:
    def __init__(self, path_index, level):
        self.path_index = path_index 
        self.level = level
        self.path_step = 0 
        
        stats = config.ENEMY_TYPES.get(level, config.ENEMY_TYPES[1])
        
        self.hp = stats['hp']
        self.max_hp = stats['hp']
        self.damage = stats['dmg']
        self.color = stats['color']
        self.reward = stats['reward']
        self.move_cooldown = random.randint(1, 3) 
        self.move_timer = 0

        if path_index < len(config.PATHS) and len(config.PATHS[path_index]) > 0:
            self.pos = config.PATHS[path_index][0]
        else:
            self.pos = (0, 0)

    def move(self):
        self.move_timer += 1
        if self.move_timer < self.move_cooldown:
            return True 
        self.move_timer = 0
        
        current_path = config.PATHS[self.path_index]
        if self.path_step < len(current_path) - 1:
            self.path_step += 1
            self.pos = current_path[self.path_step]
            return True
        else:
            return False 

    def get_pos(self):
        return self.pos