import time
import pygame
from pygame.locals import FULLSCREEN
from sitepackge import image_init, map_create, config
import sys
from decimal import Decimal


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


class Game:
    def __init__(self):
        self.now_width, self.now_height = None, None
        self.full_width, self.full_height = None, None
        self.width, self.height = None, None
        self.Maps = None
        self.unit = image_init.image_unit
        self.fclock = pygame.time.Clock()
        self.screen = None
        self.size = config.size
        self.unit = image_init.unit
        self.is_fullscreen = False
        image_init.load_image()
        self.gif_images = []
        for index in range(121):  # 入场动画gif的每一帧图片
            self.gif_images.append(pygame.image.load(f"./image/loading_png/gif{index}.png"))

    def init_game(self):
        pygame.init()  # 初始化pygame
        info_object = pygame.display.Info()  # 读取display信息，获取不同电脑的分辨率大小不同，更具有兼容性
        self.full_width, self.full_height = info_object.current_w, info_object.current_h  # 定义初始显示屏为比屏幕分辨率略小
        self.width, self.height = self.full_width - 100, self.full_height - 100
        if self.width // 17 > self.height // 13:  # 为了适应17：13的长宽比
            self.width, self.height = (self.height // 13) * 17, (self.height // 13) * 13
        else:
            self.width, self.height = (self.width // 17) * 17, (self.width // 17) * 13
        # self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE, 32)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.now_width, self.now_height = self.width, self.height
        pygame.display.set_caption('Tank')  # 设置屏幕的标题
        game_icon = pygame.image.load('image/icon.png')
        pygame.display.set_icon(game_icon)  # 设置屏幕的图标
        map_create.map_init(pygame.Surface(self.size))  # 传入与原始尺寸相同的surface
        self.Maps = config.Maps

    def before_game(self):
        for index in range(121):
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.gif_images[index], ((1088 - 750) / 2, (832 - 750) / 2))
            pygame.display.update()
            self.fclock.tick(config.fps)  # 控制刷新的时间
        self.screen.fill((0, 0, 0))

    def lose_stage(self, now_screen):
        width, height = now_screen.get_size()
        unit = Decimal(width // 17)
        gameover = config.image_dict['gameover'][0].copy()
        gameover = pygame.transform.scale(gameover, (unit * Decimal(2.0), unit))
        start_x, start_y, end_x, end_y = Decimal(7.5), Decimal(6.0), Decimal(4.5), Decimal(1.0)
        dx, dy = (Decimal(4.5) - Decimal(7.5)) / Decimal(100.0), (Decimal(1.0) - Decimal(6.0)) / Decimal(100.0)
        start_size, end_size = [unit * Decimal(2.0), unit], [unit * Decimal(8.0), unit * Decimal(4.0)]
        dsize_x, dsize_y = (Decimal(8.0) - Decimal(2.0)) / Decimal(100.0), \
                           (Decimal(4.0) - Decimal(1.0)) / Decimal(100.0)
        d_alpha = 255.0 / 100.0
        x, y, size, alpha = start_x, start_y, start_size, 255
        pre_screen = pygame.Surface(now_screen.get_size())
        while x > end_x:
            now_screen.set_alpha(alpha)
            gameovers = pygame.transform.scale(gameover, tuple(size))
            pre_screen.fill((0, 0, 0))
            pre_screen.blit(now_screen, (0, 0))
            pre_screen.blit(gameovers, (x * unit, y * unit))
            self.screen.fill((0, 0, 0))
            self.screen.blit(pre_screen, ((self.now_width - width) / 2, (self.now_height - height) / 2))
            pygame.display.update()
            self.fclock.tick(60)  # 控制刷新的时间
            x += dx
            y += dy
            size = [Decimal(size[0]) + Decimal(dsize_x) * Decimal(unit),
                    Decimal(size[1]) + Decimal(dsize_y) * Decimal(unit)]
            alpha -= d_alpha
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

    def win_stage(self):
        pass

    @staticmethod
    def sprites_run():
        for tank in \
                config.Maps.group_lst['player_group'].sprites() + \
                config.Maps.group_lst['enemy_group'].sprites() + \
                config.Maps.group_lst['mini_tank_group'].sprites():
            tank.move()
        for bullet in \
                config.Maps.group_lst['enemy_bullet_group'].sprites() + \
                config.Maps.group_lst['player_bullet_group'].sprites() + \
                config.Maps.group_lst['mini_tank_bullet_group'].sprites():
            if bullet.move():
                return True
        for bomb in config.Maps.group_lst['tracking_bomb_group']:
            bomb.move()

    def run_game(self):
        while True:
            # self.before_game()
            is_lose = False
            is_win = False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F11:
                            if not self.is_fullscreen:
                                self.screen = pygame.display.set_mode(
                                    (self.full_width, self.full_height),
                                    FULLSCREEN, 32)
                                self.now_width, self.now_height = self.full_width, self.full_height
                                self.is_fullscreen = True
                            else:
                                # self.screen = pygame.display.set_mode((self.width, self.height),
                                #                                       RESIZABLE, 32)
                                # self.screen = pygame.display.set_mode((self.width, self.height),
                                #                                       RESIZABLE, 32)
                                self.screen = pygame.display.set_mode((self.width, self.height))
                                self.now_width, self.now_height = self.width, self.height
                                self.is_fullscreen = False
                        elif event.key == pygame.K_ESCAPE:
                            sys.exit()
                        elif event.key == pygame.K_SPACE:
                            self.pause_game()
                        elif event.key == pygame.K_r:
                            self.Maps.replay_stage()

                if self.sprites_run():
                    is_lose = True

                now_screen = self.show_game(False)

                if [x.HP for x in config.Maps.group_lst['player_group']].count(0) == len(
                        config.Maps.group_lst['player_group']):
                    is_lose = True

                if is_lose:
                    break
            if is_lose:
                self.lose_stage(now_screen)
            elif is_win:
                self.win_stage()

    def show_game(self, pause):
        clear(self.Maps.screen)
        pre_screen = self.Maps.show(pause)
        show_line(pre_screen)
        pre_screen = resize(pre_screen, self.now_width, self.now_height)
        width, height = pre_screen.get_size()
        self.screen.fill((0, 0, 0))
        self.screen.blit(pre_screen, ((self.now_width - width) / 2, (self.now_height - height) / 2))

        pygame.display.update()
        self.fclock.tick(config.fps)  # 控制刷新的时间
        return pre_screen.copy()

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
                                (self.full_width, self.full_height),
                                FULLSCREEN, 32)
                            self.now_width, self.now_height = self.full_width, self.full_height
                            self.is_fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode((self.width, self.height))
                            self.now_width, self.now_height = self.width, self.height
                            self.is_fullscreen = False
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.show_game(True)
