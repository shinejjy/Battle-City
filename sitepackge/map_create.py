import pygame
from sitepackge.wall import Tree, Brick, River, Base, Startpoint, Iron, Ice, Slime
from sitepackge.food import Food
from sitepackge.image_init import image_unit
from sitepackge.tank import Player, Enemy
from sitepackge import config
import time
import random

unit = image_unit


# food 0复活队友 1渡河 2加移速 3加射速 4升级 5保护罩 6核弹 7子弹增强 8 9加血
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
                            brick_group.add(Brick(image_dict['brick'][0],
                                                  (x * unit + (i % 2) * unit / 2, y * unit + (i // 2) * unit / 2)))
                elif 24 in ele:
                    for i, sub_ele in enumerate(ele):
                        if sub_ele == 24:
                            iron_group.add(Iron(image_dict['iron'][0],
                                                (x * unit + (i % 2) * unit / 2, y * unit + (i // 2) * unit / 2)))

            else:
                if ele == 21:
                    river_group.add(River(image_dict['blank'][0], image_dict['river'], (x * unit, y * unit)))
                elif ele == 22:
                    ice_group.add(Ice(image_dict['ice'][0], (x * unit, y * unit)))
                elif ele == 23:
                    tree_group.add(Tree(image_dict['tree'][0], (x * unit, y * unit)))
                elif ele == 25:
                    slime_group.add(Slime(image_dict['slime'][0], (x * unit, y * unit)))
                elif ele == 30:
                    base_group.add(Base(image_dict['base'][0], (x * unit, y * unit)))
                elif ele == 31:
                    start_point_group.add(Startpoint(image_dict['blank'][0],
                                                     [image_dict['blank'][0]] + image_dict['start_point'],
                                                     (x * unit, y * unit)))
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
        self.pre_enemy_index = 0
        self.end_enemy_index = len(config.pre_enemy[self.map_index])
        self.group_lst = load_map_group(config.Map_data, config.image_dict, self.map_index)
        self.screen = screen
        self.born_time = time.time() - 0.2
        self.food_time = time.time()
        self.__during_born__ = False

    def __update__(self):
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

    def show(self, pause):
        if not pause:
            self.__update__()
            self.food_born()
        self.prompt_show()

        if len(self.group_lst['enemy_group']) == 0:
            if self.pre_enemy_index == self.end_enemy_index:
                self.next_iterator()
            else:
                self.enemy_born()
        for group in self.group_lst.values():
            for sprite in group:
                self.screen.blit(sprite.image, sprite.rect)
        return self.screen

    def next_iterator(self):
        self.map_index += 1
        self.pre_enemy_index = 0
        self.group_lst = load_map_group(config.Map_data, config.image_dict, self.map_index)
        self.end_enemy_index = len(config.pre_enemy[self.map_index])
        self.born_time = time.time() - 0.2
        self.food_time = time.time()
        self.__during_born__ = False

    def replay_stage(self):
        self.group_lst = load_map_group(config.Map_data, config.image_dict, self.map_index)
        self.pre_enemy_index = 0
        self.born_time = time.time() - 0.2
        self.food_time = time.time()
        self.__during_born__ = False

    def enemy_born(self):
        f = True
        now = time.time()
        if now - self.born_time < 0.2:
            return
        self.born_time = now
        for start_point in self.group_lst['start_point_group']:
            if not start_point.updates():  # 更新start_point的贴图，若动画结束则返回True
                f = False
        if f:  # 若所有敌方出生点的动画都结束了，则f为True
            for enemy, start_point in zip(config.pre_enemy[self.map_index][self.pre_enemy_index],
                                          self.group_lst['start_point_group']):
                self.group_lst['enemy_group'].add(Enemy(image=config.image_dict['blank'][0],
                                                        all_images=config.image_dict[enemy['enemy_type']],
                                                        initial_position=start_point.rect.topleft,
                                                        level=enemy['level'],
                                                        enemy_type=enemy['enemy_type']))
            self.pre_enemy_index += 1

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
        n_enemy = (len(config.pre_enemy[self.map_index]) - self.pre_enemy_index) * \
                  len(config.pre_enemy[self.map_index][0]) + len(self.group_lst['enemy_group'])
        for i in range(n_enemy):
            self.screen.blit(config.image_dict['enemy_icon'][0], (10 + unit * 13 + 40 * (i % 6), 10 + 40 * (i // 6)))

        ip = pygame.transform.scale(config.image_dict['player_icon'][0], (32, 32))
        iip = pygame.transform.scale(config.image_dict['player_icon'][1], (32, 32))
        heart = pygame.transform.scale(config.image_dict['heart'][0], (22, 18))
        self.screen.blit(ip, (10 + unit * 13, 11 * unit))
        for i in range(self.group_lst['player_group'].sprites()[0].HP):
            self.screen.blit(heart, (50 + unit * 13 + i * 30, 11 * unit + 7))

        if len(self.group_lst['player_group']) == 2:
            self.screen.blit(iip, (10 + unit * 13, 11 * unit + 32))
            for i in range(self.group_lst['player_group'].sprites()[1].HP):
                self.screen.blit(heart, (50 + unit * 13 + i * 30, 11 * unit + 32 + 7))

        bomb = pygame.transform.scale(config.image_dict['bomb'][0], (32, 32))
        for i, player in enumerate(self.group_lst['player_group']):
            for j in range(player.n_bomb):
                self.screen.blit(bomb, (10 + unit * 13 + j * 32, 12 * unit + i * 32))


# 创建一个Map类，传参map_lst和screen
def map_init(screen):
    config.Maps = Map(screen)
