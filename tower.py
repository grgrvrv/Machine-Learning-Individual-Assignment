import config

class Tower:
    def __init__(self, r, c, t_type, creation_wave):
        self.r = r
        self.c = c
        self.t_type = t_type 
        self.level = 1
        self.creation_wave = creation_wave 
        
        self._update_stats()
        
        self.cooldown = 0
        self.max_cooldown = 2 

    def _update_stats(self):
        attr = config.TOWER_TYPES[self.t_type][self.level]
        self.damage = attr['dmg']
        self.range = attr['range']

    def upgrade(self):
        if self.level < 6:
            self.level += 1
            self._update_stats()

    def get_pos(self):
        return (self.r, self.c)