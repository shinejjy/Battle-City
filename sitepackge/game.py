import time
import pygame
from pygame.locals import FULLSCREEN
from sitepackge import image_init, map_create, config
from sitepackge.menu import Menu, Button, Text, Image, Gif, DisplayButton
from PIL import Image as Img
from sitepackge.pic_process import MyGaussianBlur
import sys
from decimal import Decimal
from sitepackge.load_menu import load_menu


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
        pygame.init()  # 初始化pygame
        pygame.font.init()
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
        config.font = self.my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], 32)
        image_init.load_image()
        self.load_gif_images = []
        for index in range(121):  # 入场动画gif的每一帧图片
            self.load_gif_images.append(pygame.image.load(f"./image/loading_png/gif{index}.png"))
        self.win_gif_images = []
        for index in range(26):
            self.win_gif_images.append(pygame.image.load(f"./image/win_png/gif{index}.png"))

    def init_game(self):
        info_object = pygame.display.Info()  # 读取display信息，获取不同电脑的分辨率大小不同，更具有兼容性
        self.full_width, self.full_height = info_object.current_w, info_object.current_h  # 定义初始显示屏为比屏幕分辨率略小
        self.width, self.height = self.full_width - 100, self.full_height - 100
        if self.width // 17 > self.height // 13:  # 为了适应17：13的长宽比
            self.width, self.height = (self.height // 13) * 17, (self.height // 13) * 13
        else:
            self.width, self.height = (self.width // 17) * 17, (self.width // 17) * 13
        # self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE, 32)
        self.screen = pygame.display.set_mode((self.width, self.height))
        load_menu(self.screen)
        self.now_width, self.now_height = self.width, self.height  # 纪录当前的屏幕大小
        pygame.display.set_caption('BattleCity')  # 设置屏幕的标题
        game_icon = pygame.image.load('image/icon.png')
        pygame.display.set_icon(game_icon)  # 设置屏幕的图标
        map_create.map_init(pygame.Surface(self.size))  # 传入与原始尺寸相同的surface
        self.Maps = config.Maps

    def loading_movie(self):
        for index in range(121):
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.load_gif_images[index], ((self.now_width - 750) / 2, (self.now_height - 750) / 2))
            pygame.display.update()
            self.fclock.tick(config.fps)  # 控制刷新的时间
        self.screen.fill((0, 0, 0))
        pygame.event.clear()

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
        now_screen = pre_screen.copy()
        pre_screen = pygame.Surface(now_screen.get_size())

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            pre_screen.fill((0, 0, 0))
            pre_screen.blit(now_screen, (0, 0))
            button_event = config.lose_stage_menu.draw(pre_screen)
            if button_event == 'restart':
                return
            elif button_event == 'quit':
                pygame.quit()
                exit(0)
            self.screen.fill((0, 0, 0))
            self.screen.blit(pre_screen, ((self.now_width - width) / 2, (self.now_height - height) / 2))
            pygame.display.update()
            self.fclock.tick(60)  # 控制刷新的时间

    def win_stage(self):
        index = 0
        unit = self.now_width / 17
        width = self.win_gif_images[0].get_width()
        win_stage_menu = Menu()
        win_stage_menu.add_button(Button(
            text='Next Stage',
            position=(2 * unit, 10.5 * unit),
            color=(39, 165, 176),
            font=self.my_font,
            scale=2,
            event='next stage'
        ))
        win_stage_menu.add_button(Button(
            text='Quit',
            position=(12 * unit, 10.5 * unit),
            color=(224, 80, 1),
            font=self.my_font,
            scale=2,
            event='quit'
        ))
        win_stage_menu.add_text(Text('Win', (255, 0, 0), self.my_font, (self.now_width / 6, unit * 1), 3))
        win_stage_menu.add_text(Text('Game', (255, 0, 0), self.my_font, (self.now_width / 7 * 5, unit * 1), 3))
        win_stage_menu.add_text(Text('Player', (255, 255, 255), self.my_font, (self.now_width / 6, unit * 5), 1.5))
        win_stage_menu.add_text(Text('Score', (255, 255, 255), self.my_font, (self.now_width / 6, unit * 7), 1.5))
        win_stage_menu.add_text(Text('Kill Enemy', (255, 255, 255), self.my_font, (self.now_width / 6, unit * 9), 1.5))
        win_stage_menu.add_text(Text('P1', (127, 127, 127), self.my_font, (self.now_width / 2, unit * 5), 1.5))
        win_stage_menu.add_text(Text(
            str(self.Maps.group_lst['player_group'].sprites()[0].score),
            (127, 127, 127),
            self.my_font,
            (self.now_width / 2, unit * 7),
            1.5
        ))
        win_stage_menu.add_text(Text(
            str(self.Maps.group_lst['player_group'].sprites()[0].enemy_kill),
            (127, 127, 127),
            self.my_font,
            (self.now_width / 2, unit * 9),
            1.5
        ))
        if len(self.Maps.group_lst['player_group']) == 2:
            win_stage_menu.add_text(Text('P2', (0, 168, 69), self.my_font, (self.now_width / 7 * 5, unit * 5), 1.5))
            win_stage_menu.add_text(Text(
                str(self.Maps.group_lst['player_group'].sprites()[1].score),
                (0, 168, 69),
                self.my_font,
                (self.now_width / 7 * 5, unit * 7),
                1.5
            ))
            win_stage_menu.add_text(Text(
                str(self.Maps.group_lst['player_group'].sprites()[1].enemy_kill),
                (0, 168, 69),
                self.my_font,
                (self.now_width / 7 * 5, unit * 9),
                1.5
            ))
        win_stage_menu.add_gif(Gif(self.win_gif_images, ((self.now_width - width) / 2, unit * 0.5), 1))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill((0, 0, 0))

            button_event = win_stage_menu.draw(self.screen)
            if button_event == 'next stage':
                return
            elif button_event == 'quit':
                pygame.quit()
                exit(0)
            pygame.display.update()
            self.fclock.tick(30)  # 控制刷新的时间
            index = (index + 1) % 26

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

    def enemy_menu(self, bk, menu_image):
        width, height = bk.get_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((0, 0, 0))
            self.screen.blit(bk, (0, 0))
            self.screen.blit(menu_image, (width / 34, height / 26))
            gif = config.enemy_menu.draw(self.screen)
            if gif:
                gif.draw(self.screen)
            pygame.display.update()
            self.fclock.tick(20)  # 控制刷新的时间

    def food_menu(self, bk, menu_image):
        width, height = bk.get_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((0, 0, 0))
            self.screen.blit(bk, (0, 0))
            self.screen.blit(menu_image, (width / 34, height / 26))
            content = config.food_menu.draw(self.screen)
            if content:
                for inside in content:
                    inside.draw(self.screen)
            pygame.display.update()
            self.fclock.tick(10)  # 控制刷新的时间

    def player_menu(self, bk, menu_image):
        width, height = bk.get_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((0, 0, 0))
            self.screen.blit(bk, (0, 0))
            self.screen.blit(menu_image, (width / 34, height / 26))
            content = config.player_menu.draw(self.screen)
            if content:
                for inside in content:
                    inside.draw(self.screen)
            pygame.display.update()
            self.fclock.tick(10)  # 控制刷新的时间

    def help_menu(self, bk, menu_image):
        width, height = bk.get_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((0, 0, 0))
            self.screen.blit(bk, (0, 0))
            self.screen.blit(menu_image, (width / 34, height / 26))
            menu_event = config.help_menu.draw(self.screen)
            if menu_event == 'food':
                self.food_menu(bk, menu_image)
            elif menu_event == 'enemy':
                self.enemy_menu(bk, menu_image)
            elif menu_event == 'player':
                self.player_menu(bk, menu_image)
            pygame.display.update()
            self.fclock.tick(config.fps)  # 控制刷新的时间

    def esc_menu(self):
        pause_time = time.time()
        bk = self.screen.copy()
        width, height = bk.get_size()
        pygame.image.save(bk, './buffer/tmp.png')
        image = Img.open('./buffer/tmp.png')
        image = image.filter(MyGaussianBlur(radius=5))
        image.save('./buffer/tmp.png')
        bk = pygame.image.load('./buffer/tmp.png')
        menu_image = pygame.Surface((int(width / 17 * 16), int(height / 13 * 12)))
        menu_image.fill((150, 150, 150))
        menu_image.set_alpha(120)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            self.screen.fill((0, 0, 0))
            self.screen.blit(bk, (0, 0))
            self.screen.blit(menu_image, (width / 34, height / 26))
            menu_event = config.esc_menu.draw(self.screen)
            if menu_event == 'resume':
                self.Maps.replay_stage()
                return
            elif menu_event == 'help':
                self.help_menu(bk, menu_image)
            elif menu_event == 'back to game':
                self.Maps.food_time += time.time() - pause_time
                return
            elif menu_event == 'quit game':
                pass
            elif menu_event == 'exit to desktop':
                pygame.quit()
                exit(0)
            pygame.display.update()
            self.fclock.tick(config.fps)  # 控制刷新的时间

    def run_game(self):
        while True:
            self.loading_movie()
            is_lose = False
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
                            self.esc_menu()
                        elif event.key == pygame.K_SPACE:
                            self.pause_game()
                        elif event.key == pygame.K_r:
                            self.Maps.replay_stage()

                if self.sprites_run():
                    is_lose = True

                now_screen, is_win = self.show_game()

                if [x.HP for x in config.Maps.group_lst['player_group']].count(0) == len(
                        config.Maps.group_lst['player_group']):
                    is_lose = True

                if is_lose or is_win:
                    break
            if is_lose:
                self.lose_stage(now_screen)
                self.Maps.replay_stage()
            elif is_win:
                self.win_stage()
                self.Maps.next_iterator()

    def show_game(self):
        clear(self.Maps.screen)
        pre_screen, is_win = self.Maps.show()
        show_line(pre_screen)
        # self.now_width, self.now_height = self.screen.get_size()
        pre_screen = resize(pre_screen, self.now_width, self.now_height)
        width, height = pre_screen.get_size()
        self.screen.fill((0, 0, 0))
        self.screen.blit(pre_screen, ((self.now_width - width) / 2, (self.now_height - height) / 2))

        pygame.display.update()
        self.fclock.tick(config.fps)  # 控制刷新的时间
        return pre_screen.copy(), is_win

    def pause_game(self):
        pause_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.Maps.food_time += time.time() - pause_time
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

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            event = config.main_menu.draw(self.screen)
            pygame.display.update()
            self.fclock.tick(config.fps)  # 控制刷新的时间
