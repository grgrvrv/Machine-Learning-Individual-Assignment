import config


class MapGenerator:
    def __init__(self, env):
        self.env = env

    def generate_spread_map(self, count):

        new_paths = []
        spread_starts = [(0, 5), (5, 0), (9, 5), (5, 9), (0, 0), (0, 9), (9, 0), (9, 9)]

        targets = []
        if len(config.BASES) == 1:
            targets = [config.BASES[0]] * count
        else:
            for i in range(count):
                targets.append(config.BASES[i % 2])

        for i in range(count):
            path = []
            curr_r, curr_c = spread_starts[i % len(spread_starts)]
            tr, tc = targets[i]
            path.append((curr_r, curr_c))

            while (curr_r != tr) or (curr_c != tc):
                moves = []
                if curr_r < tr:
                    moves.append((1, 0))
                elif curr_r > tr:
                    moves.append((-1, 0))
                if curr_c < tc:
                    moves.append((0, 1))
                elif curr_c > tc:
                    moves.append((0, -1))

                if not moves:
                    break
                dr, dc = self.env.rng.choice(moves)
                curr_r += dr
                curr_c += dc
                path.append((curr_r, curr_c))
            new_paths.append(path)

        config.PATHS = new_paths
