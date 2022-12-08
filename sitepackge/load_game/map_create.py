import pygame
from sitepackge.element.wall import StaticWall, DynamicWall
from sitepackge.element.food import Food
from sitepackge.load_game.load_resource import image_unit as unit
from sitepackge.element.tank import Player, Enemy
from sitepackge import config
from sitepackge.load_game import menu
import time
import random


# food 0复活队友 1渡河 2加移速 3加射速 4升级 5保护罩 6核弹 7子弹增强 8 生成小坦克 9加血
# def create_food_type():
#     seed = random.randint(0, 100)
#     random.seed(seed)
#     a = random.randint(0, 100)


# 通过预先设置的地图数据和图像字典，创建一个存有关卡map_index的Group
def load_map_group(preMapLst, image_dict, map_index):
    # blank 0 player1 1 player2 2 brick 20 river 21 ice 22 tree 23 iron 24 slime 25 base 30 startpoint 31
    stage = preMapLst[map_index]
    base_group = pygame.sprite.Group()
    brick_group = pygame.sprite.Group()
    iron_group = pygame.sprite.Group()
    river_group = pygame.sprite.Group()
    ice_group = pygame.sprite.Group()
    tree_group = pygame.sprite.Group()
    slime_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    mini_tank_group = pygame.sprite.Group()
    player_bullet_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    mini_tank_bullet_group = pygame.sprite.Group()
    boom_group = pygame.sprite.Group()
    start_point_group = pygame.sprite.Group()
    blood_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    score_group = pygame.sprite.Group()
    text_group = pygame.sprite.Group()
    tracking_bomb_group = pygame.sprite.Group()
    cover_group = pygame.sprite.Group()
    for y, line in enumerate(stage):
        for x, ele in enumerate(line):
            if type(ele) == list:
                if 20 in ele:
                    for i, sub_ele in enumerate(ele):
                        if sub_ele == 20:
                            brick_group.add(StaticWall(image_dict['brick'][0],
                                                       (x * unit + (i % 2) * unit / 2, y * unit + (i // 2) * unit / 2)))
                elif 24 in ele:
                    for i, sub_ele in enumerate(ele):
                        if sub_ele == 24:
                            iron_group.add(StaticWall(image_dict['iron'][0],
                                                      (x * unit + (i % 2) * unit / 2, y * unit + (i // 2) * unit / 2)))

            else:
                if ele == 21:
                    river_group.add(DynamicWall(image_dict['blank'][0], image_dict['river'], (x * unit, y * unit), 0.5))
                elif ele == 22:
                    ice_group.add(StaticWall(image_dict['ice'][0], (x * unit, y * unit)))
                elif ele == 23:
                    tree_group.add(StaticWall(image_dict['tree'][0], (x * unit, y * unit)))
                elif ele == 25:
                    slime_group.add(StaticWall(image_dict['slime'][0], (x * unit, y * unit)))
                elif ele == 30:
                    base_group.add(StaticWall(image_dict['base'][0], (x * unit, y * unit)))
                elif ele == 31:
                    start_point_group.add(DynamicWall(image_dict['blank'][0],
                                                      [image_dict['blank'][0]] + image_dict['start_point'],
                                                      (x * unit, y * unit),
                                                      0.2))
                elif ele == 1:
                    player_group.add(Player(image=image_dict['blank'][0],
                                            images=image_dict['player1'],
                                            initial_position=(x * unit, y * unit),
                                            player_index=1, ))
                elif ele == 2:
                    player_group.add(Player(image=image_dict['blank'][0],
                                            images=image_dict['player2'],
                                            initial_position=(x * unit, y * unit),
                                            player_index=2))
    stage_lst = {'brick_group': brick_group,
                 'iron_group': iron_group,
                 'river_group': river_group,
                 'ice_group': ice_group,
                 'slime_group': slime_group,
                 'start_point_group': start_point_group,
                 'player_bullet_group': player_bullet_group,
                 'enemy_bullet_group': enemy_bullet_group,
                 'mini_tank_bullet_group': mini_tank_bullet_group,
                 'food_group': food_group,
                 'enemy_group': enemy_group,
                 'player_group': player_group,
                 'mini_tank_group': mini_tank_group,
                 'cover_group': cover_group,
                 'tracking_bomb_group': tracking_bomb_group,
                 'tree_group': tree_group,
                 'base_group': base_group,
                 'blood_group': blood_group,
                 'score_group': score_group,
                 'boom_group': boom_group,
                 'text_group': text_group}
    return stage_lst


class Map:
    def __init__(self, screen):
        self.map_index = 0
        self.enemy_index = 0
        self.end_enemy_index = None
        self.end_map_index = len(config.Map_data)
        self.group_lst = None
        self.screen = screen
        self.born_time = time.time() - 0.2
        self.food_time = time.time()
        self.during_born = False

    def select_level(self, index):
        self.map_index = index
        self.enemy_index = 0
        self.group_lst = load_map_group(config.Map_data, config.image_dict, self.map_index)
        self.end_enemy_index = len(config.pre_enemy[self.map_index])

    def update(self):
        for river in self.group_lst['river_group']:
            river.updates()
        for boom in self.group_lst['boom_group']:
            boom.updates()
        for blood in self.group_lst['blood_group']:
            blood.updates()
        for food in self.group_lst['food_group']:
            food.updates()
        for score in self.group_lst['score_group']:
            score.updates()
        for cover in self.group_lst['cover_group']:
            cover.updates()

    def show(self):
        is_win = False
        self.update()
        self.food_born()
        self.prompt_show()

        if len(self.group_lst['enemy_group']) == 0:
            if self.enemy_index == self.end_enemy_index:
                is_win = True
            else:
                self.enemy_born()
        for group in self.group_lst.values():
            for sprite in group:
                self.screen.blit(sprite.image, sprite.rect)
        return self.screen, is_win

    def next_iterator(self):
        if self.map_index == self.end_map_index:
            return True
        self.map_index += 1
        self.enemy_index = 0
        self.group_lst = load_map_group(config.Map_data, config.image_dict, self.map_index)
        self.end_enemy_index = len(config.pre_enemy[self.map_index])
        self.born_time = time.time() - 0.2
        self.food_time = time.time()
        self.during_born = False

    def replay_stage(self):
        self.group_lst = load_map_group(config.Map_data, config.image_dict, self.map_index)
        self.enemy_index = 0
        self.born_time = time.time() - 0.2
        self.food_time = time.time()
        self.during_born = False

    def enemy_born(self):
        f = True
        now = time.time()
        if now - self.born_time < 0.2:
            return
        self.born_time = now
        for start_point in self.group_lst['start_point_group']:
            event = start_point.updates()  # 更新start_point的贴图，若动画结束则返回True
            if not event:
                return
            elif event != 'new':
                f = False
        if f:  # 若所有敌方出生点的动画都结束了，则f为True
            for enemy, start_point in zip(config.pre_enemy[self.map_index][self.enemy_index],
                                          self.group_lst['start_point_group']):
                self.group_lst['enemy_group'].add(Enemy(image=config.image_dict['blank'][0],
                                                        all_images=config.image_dict[enemy['enemy_type']],
                                                        initial_position=start_point.rect.topleft,
                                                        level=enemy['level'],
                                                        enemy_type=enemy['enemy_type']))
            self.enemy_index += 1

    def food_born(self):
        now = time.time()
        if now - self.food_time > 15:
            self.food_time = now
            while True:
                top = random.randint(0, 12 * unit)
                left = random.randint(0, 12 * unit)
                types = random.randint(0, 9)
                food = Food(images=[config.image_dict['blank'][0],
                                    config.image_dict['food'][types]],
                            initial_position=(left, top),
                            types=types)
                if pygame.sprite.spritecollide(food, self.group_lst['river_group'], False):
                    continue
                if pygame.sprite.spritecollide(food, self.group_lst['base_group'], False):
                    continue
                if pygame.sprite.spritecollide(food, self.group_lst['iron_group'], False):
                    continue
                break
            self.group_lst['food_group'].add(food)

    def prompt_show(self):
        my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(64 / 2))
        self.screen.blit(menu.get_text_surface(f"Level {self.map_index + 1}", (0, 0, 0), my_font),
                         (10 + unit * 13, 10))
        n_enemy = \
            (len(config.pre_enemy[self.map_index]) - self.enemy_index) * \
            len(config.pre_enemy[self.map_index][0]) + len(self.group_lst['enemy_group'])
        for i in range(n_enemy):
            self.screen.blit(config.image_dict['enemy_icon'][0], (10 + unit * 13 + 40 * (i % 6), 64 + 40 * (i // 6)))

        ip = pygame.transform.scale(config.image_dict['player_icon'][0], (32, 32))
        iip = pygame.transform.scale(config.image_dict['player_icon'][1], (32, 32))
        heart = pygame.transform.scale(config.image_dict['heart'][0], (22, 18))
        bomb = pygame.transform.scale(config.image_dict['bomb'][0], (32, 32))
        board = pygame.transform.scale(config.image_dict['food'][1], (32, 32))
        faster = pygame.transform.scale(config.image_dict['food'][2], (32, 32))
        shoot_faster = pygame.transform.scale(config.image_dict['food'][3], (32, 32))
        cover = pygame.transform.scale(config.image_dict['food'][5], (32, 32))
        strong = pygame.transform.scale(config.image_dict['food'][7], (32, 32))

        # ip
        ip_obj = self.group_lst['player_group'].sprites()[0]
        self.screen.blit(ip, (10 + unit * 13, 5 * unit))
        for i in range(ip_obj.HP):
            self.screen.blit(heart, (50 + unit * 13 + i * 30, 5 * unit + 7))
        for i in range(ip_obj.n_bomb):
            self.screen.blit(bomb, (10 + unit * 13 + i * 32, 7 * unit))
        if ip_obj.is_board:
            self.screen.blit(board, (10 + unit * 13, 6 * unit + 32))
        if ip_obj.is_faster:
            self.screen.blit(faster, (10 + unit * 13 + 32, 6 * unit + 32))
        if ip_obj.is_strong:
            self.screen.blit(strong, (10 + unit * 14, 6 * unit + 32))
        if ip_obj.is_shot_faster:
            self.screen.blit(shoot_faster, (10 + unit * 14 + 32, 6 * unit + 32))
        if ip_obj.cover_level:
            self.screen.blit(cover, (10 + unit * 15, 6 * unit + 32))
        menu.draw_text(f'score:', (0, 0, 0), config.font, (10 + unit * 13, 5 * unit + 32), self.screen, 1)
        menu.draw_text(f'{ip_obj.score}',
                       (255, 159, 56), config.font, (10 + unit * 14 + 32, 5 * unit + 32), self.screen, 1)
        menu.draw_text(f'kill enemy:', (0, 0, 0), config.font, (10 + unit * 13, 6 * unit), self.screen, 1)
        menu.draw_text(f'{ip_obj.enemy_kill}',
                       (255, 159, 56), config.font, (10 + unit * 15 + 32, 6 * unit), self.screen, 1)

        # iip
        if len(self.group_lst['player_group']) == 2:
            iip_obj = self.group_lst['player_group'].sprites()[1]
            self.screen.blit(iip, (10 + unit * 13, 9 * unit))
            for i in range(iip_obj.HP):
                self.screen.blit(heart, (50 + unit * 13 + i * 30, 9 * unit + 7))
            for i in range(iip_obj.n_bomb):
                self.screen.blit(bomb, (10 + unit * 13 + i * 32, 11 * unit))
            if iip_obj.is_board:
                self.screen.blit(board, (10 + unit * 13, 10 * unit + 32))
            if iip_obj.is_faster:
                self.screen.blit(faster, (10 + unit * 13 + 9, 10 * unit + 32))
            if iip_obj.is_strong:
                self.screen.blit(strong, (10 + unit * 14, 10 * unit + 32))
            if iip_obj.is_shot_faster:
                self.screen.blit(shoot_faster, (10 + unit * 14 + 32, 10 * unit + 32))
            if iip_obj.cover_level:
                self.screen.blit(cover, (10 + unit * 15, 10 * unit + 32))
            menu.draw_text(f'score:', (0, 0, 0), config.font, (10 + unit * 13, 9 * unit + 32), self.screen, 1)
            menu.draw_text(f'{iip_obj.score}',
                           (255, 159, 56), config.font, (10 + unit * 14 + 32, 9 * unit + 32), self.screen, 1)
            menu.draw_text(f'kill enemy:', (0, 0, 0), config.font, (10 + unit * 13, 10 * unit), self.screen, 1)
            menu.draw_text(f'{iip_obj.enemy_kill}',
                           (255, 159, 56), config.font, (10 + unit * 15 + 32, 10 * unit), self.screen, 1)


# 创建一个Map类，传参map_lst和screen
def map_init(screen):
    config.Maps = Map(screen)
