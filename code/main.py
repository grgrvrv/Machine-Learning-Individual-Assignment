import pygame
import sys
import config
from game_env import TowerDefenseEnv
from q_learning import MasterAI
from renderer import GameRenderer

pygame.init()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Tower Defense: Fixed Edition")
clock = pygame.time.Clock()

renderer = GameRenderer(screen)


def main():
    while True:
        mode = run_menu_loop()
        if mode == "QUIT":
            pygame.quit()
            sys.exit()

        while True:
            level = run_level_select_loop(mode)
            if level == "BACK": break

            while True:
                result = run_game_loop(mode, level)
                if result == "BACK": break
                elif result == "REPLAY": continue


def run_menu_loop():
    while True:
        renderer.draw_menu()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return "AI_UNTRAINED"
                if event.key == pygame.K_2: return "AI_EXPERT"
                if event.key == pygame.K_3: return "PLAYER"
                if event.key == pygame.K_4: run_intro_loop()
                if event.key == pygame.K_ESCAPE: return "QUIT"


def run_intro_loop():
    pygame.event.clear()
    while True:
        renderer.draw_intro_screen()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return


def run_level_select_loop(mode):
    pygame.time.wait(200); pygame.event.clear()
    while True:
        renderer.draw_level_select(mode)
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9: return event.key - pygame.K_0
                if event.key == pygame.K_0: return 10
                if event.key == pygame.K_ESCAPE: return "BACK"


def run_game_loop(mode, start_level):
    env = TowerDefenseEnv()
    env.reset(start_level)

    agent = None
    if "AI" in mode:
        if mode == "AI_EXPERT":
            epsilon, lr, use_h = 0.0, 0.0, True
        else:
            epsilon, lr, use_h = 0.4, 0.1, False
        
        agent = MasterAI(len(env.action_space), lr, 0.9, epsilon, use_h)

    sell_mode = False
    game_running = True

    while game_running:
        state, done = env.get_state(), False

        while not done:
            action = 0
            current_state_key = None
            
            if agent:
                current_state_key = agent.get_state_key(env)
                action = agent.choose_action(env)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "BACK"
                
                if mode == "PLAYER" and env.shopping_phase:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: action = 0
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if renderer.sell_btn_rect.collidepoint(mx, my) and event.button == 1:
                            sell_mode = not sell_mode
                        elif mx < config.GRID_SIZE * config.CELL_SIZE:
                            c, r = mx // config.CELL_SIZE, my // config.CELL_SIZE
                            if sell_mode:
                                if event.button == 1:
                                    success, _ = env.sell_tower(r, c)
                                    if success: sell_mode = False
                                elif event.button == 3: sell_mode = False
                            else:
                                grid_action = (r * config.GRID_SIZE + c) + 1
                                if event.button == 1: action = grid_action
                                elif event.button == 3: action = grid_action + 100

            if mode == "PLAYER" and env.shopping_phase:
                keys = pygame.key.get_pressed()
                if action == 0 and not keys[pygame.K_SPACE]:
                    renderer.draw_game_scene(env, agent, mode, sell_mode)
                    clock.tick(30)
                    continue

            next_env_state, reward, done = env.step(action)

            if agent:
                next_state_key = agent.get_state_key(env)
                agent.learn(env, current_state_key, action, reward, next_state_key)

                if mode == "AI_EXPERT" and reward < 0:
                    if current_state_key in agent.q_table:
                        agent.q_table[current_state_key][action] = -99999.0

            renderer.draw_game_scene(env, agent, mode, sell_mode)

            if agent: clock.tick(0) 
            else: clock.tick(30)

        is_win = env.base_hp > 0
        return run_result_loop(is_win, env.base_hp, config.BASE_MAX_HP)


def run_result_loop(is_win, final_hp, max_hp):
    pygame.event.clear()
    while True:
        renderer.draw_result_screen(is_win, final_hp, max_hp)
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4: return "REPLAY"
                if event.key == pygame.K_ESCAPE: return "BACK"


if __name__ == "__main__":
    main()