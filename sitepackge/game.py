import time
import pygame
from pygame.locals import RESIZABLE, FULLSCREEN
from sitepackge import image_init, map_create, config
import sys


def resize(pre_screen, screen_width, screen_height):
    if screen_width // 17 > screen_height // 13:
        pre_screen = pygame.transform.scale(pre_screen, ((screen_height // 13) * 17, (screen_height // 13) * 13))
    else:
        pre_screen = pygame.transform.scale(pre_screen, ((screen_width // 17) * 17, (screen_width // 17) * 13))
    return pre_screen


def clear(screen):
    pygame.draw.polygon(screen, (0, 0, 0), ((0, 0), (13 * 64, 0), (13 * 64, 13 * 64), (0, 13 * 64)))
    pygame.draw.polygon(screen, (255, 255, 255), ((13 * 64, 0), (17 * 64, 0), (17 * 64, 13 * 64), (13 * 64, 13 * 64)))


def show_line(screen):
    pygame.draw.line(screen, (255, 0, 0), (13 * 64, 0), (13 * 64, 13 * 64), width=3)
    pygame.draw.line(screen, (255, 0, 0), (17 * 64 - 1, 0), (17 * 64 - 1, 13 * 64), width=3)
    pygame.draw.line(screen, (255, 0, 0), (0, 0), (17 * 64, 0), width=3)
    pygame.draw.line(screen, (255, 0, 0), (0, 0), (0, 13 * 64), width=3)
    pygame.draw.line(screen, (255, 0, 0), (0, 13 * 64 - 1), (17 * 64, 13 * 64 - 1), width=3)


def sprites_run():
    for player in config.Maps.group_lst['player_group']:
        player.move()
    for bullet in config.Maps.group_lst['enemy_bullet_group']:
        bullet.move()
    for bullet in config.Maps.group_lst['player_bullet_group']:
        bullet.move()
    for bomb in config.Maps.group_lst['tracking_bomb_group']:
        bomb.move()
    for enemy in config.Maps.group_lst['enemy_group']:
        enemy.move()
    for mini_tank in config.Maps.group_lst['mini_tank_group']:
        mini_tank.move()
    for bullet in config.Maps.group_lst['mini_tank_bullet_group']:
        bullet.move()


class Game:
    def __init__(self):
        self.Maps = None
        self.unit = image_init.image_unit
        self.width = None
        self.height = None
        self.info_object = None
        self.fclock = pygame.time.Clock()
        self.screen = None
        self.size = config.size
        self.unit = image_init.unit
        self.is_fullscreen = False
        image_init.load_image()
        self.gif_images = []
        for index in range(121):
            self.gif_images.append(pygame.image.load(f"./image/loading_png/gif{index}.png"))

    def init_game(self):
        pygame.init()
        self.info_object = pygame.display.Info()
        self.width, self.height = self.info_object.current_w - 100, self.info_object.current_h - 100
        if self.width // 17 > self.height // 13:
            self.width, self.height = (self.height // 13) * 17, (self.height // 13) * 13
        else:
            self.width, self.height = (self.width // 17) * 17, (self.width // 17) * 13
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE, 32)
        pygame.display.set_caption('Tank')
        game_icon = pygame.image.load('image/icon.png')
        pygame.display.set_icon(game_icon)
        map_create.map_init(pygame.Surface(self.size))
        self.Maps = config.Maps

    def before_game(self):
        for index in range(121):
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.gif_images[index], ((1088 - 750) / 2, (832 - 750) / 2))
            pygame.display.update()
            self.fclock.tick(config.fps)  # 控制刷新的时间
        self.screen.fill((0, 0, 0))

    def lose_stage(self):
        pass

    def run_game(self):
        self.before_game()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if not self.is_fullscreen:
                            self.screen = pygame.display.set_mode(
                                (self.info_object.current_w, self.info_object.current_h),
                                FULLSCREEN, 32)
                            self.is_fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode((self.width, self.height),
                                                                  RESIZABLE, 32)
                            self.screen = pygame.display.set_mode((self.width, self.height),
                                                                  RESIZABLE, 32)
                            self.is_fullscreen = False
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.pause_game()
                    elif event.key == pygame.K_r:
                        self.Maps.replay_stage()

            sprites_run()
            self.show_game(False)

            if [x.HP for x in config.Maps.group_lst['player_group']].count(0) == len(
                    config.Maps.group_lst['player_group']):
                exit(0)

    def show_game(self, pause):
        clear(config.Maps.screen)
        pre_screen = config.Maps.show(pause)
        show_line(pre_screen)
        screen_width, screen_height = self.screen.get_size()
        pre_screen = resize(pre_screen, screen_width, screen_height)
        width, height = pre_screen.get_size()

        self.screen.fill((0, 0, 0))
        self.screen.blit(pre_screen, ((screen_width - width) / 2, (screen_height - height) / 2))

        pygame.display.update()
        self.fclock.tick(config.fps)  # 控制刷新的时间

    def pause_game(self):
        config.Maps.food_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_F11:
                        if not self.is_fullscreen:
                            self.screen = pygame.display.set_mode(
                                (self.info_object.current_w, self.info_object.current_h),
                                FULLSCREEN, 32)
                            self.is_fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode((self.width, self.height),
                                                                  RESIZABLE, 32)
                            self.is_fullscreen = False
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.show_game(True)
