import pygame
import random
from sitepackge.element.effect import Bullet, Blood, TrackingBomb, Cover
from sitepackge import config
from sitepackge.load_game import load_resource
from sitepackge.load_game.load_resource import image_unit as unit
import time


def initial_positions(rect):
    return [
        ((rect.left + rect.right) / 2 - 6.5, rect.top),
        (rect.right - 9.5, (rect.top + rect.bottom) / 2 - 6.5),
        ((rect.left + rect.right) / 2 - 6.5, rect.bottom - 8.5),
        (rect.left, (rect.top + rect.bottom) / 2 - 6.5)
    ]


def optimize_collide(sprite1: pygame.sprite.Sprite, sprite2: pygame.sprite.Sprite):
    sprite3 = pygame.sprite.Sprite()
    sprite3.rect = pygame.Rect((sprite2.rect.left + 5, sprite2.rect.top + 5),
                               (sprite2.rect.width - 10, sprite2.rect.height - 10))
    return pygame.sprite.collide_rect(sprite1, sprite3)


class Tank(pygame.sprite.Sprite):
    def __init__(self, image, initial_position, fire_space, tank_type):
        super().__init__()
        self.initial_position = initial_position
        self.tank_type = tank_type
        self.rect = image.get_rect()
        self.rect.topleft = initial_position
        self.old_topleft = list(self.rect.topleft)
        self.dir = 0  # 0 U, 1 R, 2 D, 3 L
        self.dir_lst = [0, 0, 0, 0]
        self.fire_space = fire_space
        self.fire_time = time.time() - self.fire_space
        self.ice_faster = 0  # 是否冰块加速

        # food_effect
        self.now_faster_time = 0  # 此时的加速时间
        self.faster_time = 3  # 加速时间
        self.is_faster = 0  # 是否加速

        self.now_strong_time = 0  # 此时的强壮时间
        self.strong_time = 10  # 强壮时间
        self.is_strong = False  # 是否能打破iron/slime

        self.now_shot_faster_time = 0  # 此时射速时间
        self.shot_faster_time = 10  # 射速加快时间
        self.is_shot_faster = 0  # 是否加快射速

        self.now_board_time = 0  # 此时的可渡河时间
        self.board_time = 10  # 能够渡河时间
        self.is_board = False  # 是否能够渡河

        self.now_cover_time = 0  # 此时保护罩时间
        self.cover_time = 10  # 保护罩能够存在的时间
        self.cover_level = 0  # 现存保护罩的等级

    def collide(self, tank_type):
        for ice in config.Maps.group_lst['ice_group']:
            if pygame.sprite.collide_rect(ice, self):
                self.ice_faster = 4
                break
            else:
                self.ice_faster = 0
        if self.reset_collide_wall():
            return True
        for brick in config.Maps.group_lst['brick_group']:
            if optimize_collide(self, brick):
                return True
        if not self.is_board:
            for river in config.Maps.group_lst['river_group']:
                if optimize_collide(self, river):
                    self.smooth_collide(river)
                    return True
        for iron in config.Maps.group_lst['iron_group']:
            if optimize_collide(self, iron):
                self.smooth_collide(iron)
                return True
        for slime in config.Maps.group_lst['slime_group']:
            if optimize_collide(self, slime):
                self.smooth_collide(slime)
                return True

        if tank_type == 0:
            if pygame.sprite.spritecollideany(self, config.Maps.group_lst['tree_group']):
                if not self.tree_music:
                    pygame.mixer.music.load(config.audio_dict['tree'])
                    pygame.mixer.music.play()
                    self.tree_music = True
            else:
                self.tree_music = False

        if self.tank_type == 2:
            return False

        for start_point in config.Maps.group_lst['start_point_group']:
            if start_point.index != 0 and pygame.sprite.collide_rect(start_point, self):
                self.old_topleft = self.initial_position
                while True:
                    x = random.uniform(0, 12 * unit)
                    y = random.uniform(0, 12 * unit)
                    self.rect.topleft = (x, y)

                    if pygame.sprite.spritecollideany(self, config.Maps.group_lst['river_group']) or \
                            pygame.sprite.spritecollideany(self, config.Maps.group_lst['brick_group']) or \
                            pygame.sprite.spritecollideany(self, config.Maps.group_lst['iron_group']) or \
                            pygame.sprite.spritecollideany(self, config.Maps.group_lst['slime_group']) or \
                            pygame.sprite.spritecollideany(self, config.Maps.group_lst['base_group']) or \
                            pygame.sprite.spritecollideany(self, config.Maps.group_lst['enemy_group']) or \
                            len(pygame.sprite.spritecollide(self, config.Maps.group_lst['player_group'], False)) == 2:
                        continue
                    break

                return True
        for enemy in config.Maps.group_lst['enemy_group']:
            if tank_type == 0 or enemy != self:
                if pygame.sprite.collide_rect(enemy, self):
                    return True
        for player in config.Maps.group_lst['player_group']:
            if (tank_type == 1 or player != self) and player.HP > 0:
                if pygame.sprite.collide_rect(player, self):
                    return True
        return False

    def smooth_collide(self, other):
        if self.rect.bottom > other.rect.top > self.rect.top and self.dir == 2:
            self.old_topleft[1] = other.rect.top - load_resource.image_unit + 5
        elif self.rect.top < other.rect.bottom < self.rect.bottom and self.dir == 0:
            self.old_topleft[1] = other.rect.bottom - 5
        elif self.rect.left < other.rect.right < self.rect.right and self.dir == 3:
            self.old_topleft[0] = other.rect.right - 5
        elif self.rect.right > other.rect.left > self.rect.left and self.dir == 1:
            self.old_topleft[0] = other.rect.left - load_resource.image_unit + 5

    def reset_collide_wall(self):
        if self.rect.top < 0:
            self.old_topleft[1] = 0
            return True
        if self.rect.left < 0:
            self.old_topleft[0] = 0
            return True
        if self.rect.right > config.width:
            self.old_topleft[0] = config.width - 64
            return True
        if self.rect.bottom > config.height:
            self.old_topleft[1] = config.height - 64
            return True
        return False

    def eat(self):
        for food in config.Maps.group_lst['food_group']:
            if pygame.sprite.collide_rect(food, self):
                config.Maps.group_lst['food_group'].remove(food)
                food.effect(self)
                del food

    def __fire__(self):
        fire_time = time.time()
        if fire_time - self.fire_time < self.fire_space - self.is_shot_faster:
            return
        self.fire_time = fire_time
        initial_position = initial_positions(self.rect)
        bullet = Bullet(image=config.image_dict['blank'][self.dir % 2 + 1],
                        images=config.image_dict['bullet'],
                        initial_position=initial_position[self.dir],
                        dirs=self.dir,
                        types=self.tank_type,
                        from_tank=self.father_tank if self.tank_type == 2 else self)
        if self.tank_type == 0:
            config.Maps.group_lst['player_bullet_group'].add(bullet)
            pygame.mixer.music.load(config.audio_dict['fire'])
            pygame.mixer.music.play()
        elif self.tank_type == 1:
            config.Maps.group_lst['enemy_bullet_group'].add(bullet)
        elif self.tank_type == 2:
            config.Maps.group_lst['mini_tank_bullet_group'].add(bullet)

    def delay_faster(self, is_initial):
        if is_initial:
            self.is_faster = 4
            self.now_faster_time = time.time()
        else:
            if self.is_faster:
                now = time.time()
                if now - self.now_faster_time > self.faster_time:
                    self.now_faster_time = 0
                    self.is_faster = 0

    def delay_strong(self, is_initial):
        if is_initial:
            self.is_strong = True
            self.now_strong_time = time.time()
        else:
            if self.is_strong:
                now = time.time()
                if now - self.now_strong_time > self.strong_time:
                    self.now_strong_time = 0
                    self.is_strong = False

    def delay_shot_faster(self, is_initial):
        if is_initial:
            self.is_shot_faster = 0.1
            self.now_shot_faster_time = time.time()
        else:
            if self.is_shot_faster:
                now = time.time()
                if now - self.now_shot_faster_time > self.shot_faster_time:
                    self.now_shot_faster_time = 0
                    self.is_shot_faster = 0

    def delay_board(self, is_initial):
        if is_initial:
            self.is_board = True
            self.now_board_time = time.time()
        else:
            if self.is_board:
                now = time.time()
                if now - self.now_board_time > self.board_time:
                    self.now_board_time = 0
                    self.is_board = False
                    if pygame.sprite.spritecollideany(self, config.Maps.group_lst['river_group']):
                        while True:
                            x = random.uniform(0, 12 * unit)
                            y = random.uniform(0, 12 * unit)
                            self.rect.topleft = (x, y)
                            if pygame.sprite.spritecollideany(self, config.Maps.group_lst['river_group']) or \
                                    pygame.sprite.spritecollideany(self, config.Maps.group_lst['brick_group']) or \
                                    pygame.sprite.spritecollideany(self, config.Maps.group_lst['iron_group']) or \
                                    pygame.sprite.spritecollideany(self, config.Maps.group_lst['slime_group']) or \
                                    pygame.sprite.spritecollideany(self, config.Maps.group_lst['base_group']) or \
                                    pygame.sprite.spritecollideany(self, config.Maps.group_lst['enemy_group']) or \
                                    len(pygame.sprite.spritecollide(
                                        self, config.Maps.group_lst['player_group'], False)) == 2:
                                continue
                            for player in config.Maps.group_lst['player_group']:
                                if player != self and pygame.sprite.collide_rect(self, player):
                                    continue
                            for enemy in config.Maps.group_lst['enemy_group']:
                                if enemy != self and pygame.sprite.collide_rect(self, enemy):
                                    continue
                        self.old_topleft = self.rect.topleft

    def delay_cover(self, is_initial):
        if is_initial:
            self.cover_level = 1
            self.now_cover_time = time.time()
            config.Maps.group_lst['cover_group'].add(Cover(config.image_dict['cover'][self.cover_level],
                                                           self.rect.topleft,
                                                           self,
                                                           'normal'))
        else:
            if self.cover_level:
                now = time.time()
                if now - self.now_cover_time > self.cover_time:
                    self.now_cover_time = 0
                    self.cover_level = 0

    def food_delay(self):
        self.delay_faster(False)
        self.delay_strong(False)
        self.delay_shot_faster(False)
        self.delay_board(False)
        self.delay_cover(False)


class Player(Tank):
    def __init__(self, image, images, initial_position, player_index):
        self.level = 0
        super().__init__(image,
                         initial_position,
                         config.player_label[self.level]['fire_speed'],
                         0)
        self.all_images = images
        self.images = self.all_images[self.level]
        self.image = self.images[0][0]
        self.speed = config.player_label[self.level]['move_speed']
        self.HP = config.player_label[self.level]['HP']
        self.is_move = False
        self.player_index = player_index  # 存放玩家1还是玩家2
        self.score = 0
        self.enemy_kill = 0
        if player_index == 1:
            self.player_control = config.player_control[0]
        else:
            self.player_control = config.player_control[1]

        self.bomb = time.time() - 10
        self.n_bomb = 0

        # 受攻击无敌时间3秒
        self.invincible_time = 999999999999999999 if config.command else 3
        self.is_invincible = False
        self.now_invincible_time = 0

        self.tree_music = False

    def move(self):
        if self.HP == 0:
            return
        self.updates()
        key_list = pygame.key.get_pressed()
        # if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        if key_list[self.player_control[0]]:
            self.dir = 0
            self.rect.top = self.old_topleft[1] - (self.speed + self.ice_faster + self.is_faster)
            self.rect.left = self.old_topleft[0]
            self.is_move = True
        elif key_list[self.player_control[1]]:
            self.dir = 1
            self.rect.left = self.old_topleft[0] + (self.speed + self.ice_faster + self.is_faster)
            self.rect.top = self.old_topleft[1]
            self.is_move = True
        elif key_list[self.player_control[2]]:
            self.dir = 2
            self.rect.top = self.old_topleft[1] + (self.speed + self.ice_faster + self.is_faster)
            self.rect.left = self.old_topleft[0]
            self.is_move = True
        elif key_list[self.player_control[3]]:
            self.dir = 3
            self.rect.left = self.old_topleft[0] - (self.speed + self.ice_faster + self.is_faster)
            self.rect.top = self.old_topleft[1]
            self.is_move = True
        # if event.key == pygame.K_j:
        if key_list[self.player_control[4]]:
            self.__fire__()

        if key_list[self.player_control[5]]:
            self.tracking_bomb()

        if not [key_list[x] for x in self.player_control[:4]].count(True):
            self.is_move = False
            # self.speed = [0, 0]

        if self.collide(0):
            self.rect.topleft = tuple(self.old_topleft)
        self.old_topleft = list(self.rect.topleft)

        self.eat()
        self.invincible(False)
        self.food_delay()

    def updates(self):
        # if self.collide_wall():
        #     return
        # self.rect = self.rect.move(self.speed)
        self.image = self.images[self.dir][self.dir_lst[self.dir]]
        if self.is_move:
            self.dir_lst[self.dir] = 1 - self.dir_lst[self.dir]

    def upgrade(self):
        self.level = min(self.level + 1, 3)
        self.images = self.all_images[self.level]
        self.image = self.images[self.dir][self.dir_lst[self.dir]]
        self.speed = config.player_label[self.level]['move_speed']
        self.HP = config.player_label[self.level]['HP']
        self.fire_space = config.player_label[self.level]['fire_speed']

    def kills(self):
        self.HP = 0
        self.is_board = False
        self.is_faster = 0
        self.is_strong = False
        self.is_shot_faster = 0
        self.image = config.image_dict['blank'][0]

    def be_saved(self):
        self.HP = config.player_label[self.level]['HP']
        self.image = self.images[self.dir][self.dir_lst[self.dir]]
        self.old_topleft = self.initial_position
        self.rect.topleft = self.old_topleft
        for player in config.Maps.group_lst['player_group']:
            if player != self and pygame.sprite.collide_rect(player, self):
                self.old_topleft = player.initial_position
                self.rect.topleft = player.old_topleft

    def invincible(self, is_initial):
        if is_initial:
            self.is_invincible = True
            self.now_invincible_time = time.time()
            config.Maps.group_lst['cover_group'].add(Cover(config.image_dict['cover'][3],
                                                           self.rect.topleft,
                                                           self,
                                                           'special'))
        else:
            if self.is_invincible:
                now = time.time()
                if now - self.now_invincible_time > self.invincible_time:
                    self.now_invincible_time = 0
                    self.is_invincible = False

    def reduce_hp(self):
        self.HP -= 1

    def tracking_bomb(self):
        if not len(config.Maps.group_lst['enemy_group']):
            return
        if not self.n_bomb:
            return
        now = time.time()
        if now - self.bomb < 10:
            return
        self.n_bomb -= 1
        self.bomb = now
        config.Maps.group_lst['tracking_bomb_group'].add(
            TrackingBomb(config.image_dict['blank'][2],
                         config.image_dict['tracking_bomb'][0],
                         self.rect.center,
                         config.Maps.group_lst['enemy_group'].sprites()[0],
                         self)
        )

    def create_mini_tank(self):
        config.Maps.group_lst['mini_tank_group'].add(MiniTank(config.image_dict['blank'][4],
                                                              config.image_dict['mini_tank'],
                                                              self.rect.topleft,
                                                              self.fire_space - 0.1,
                                                              self.speed + 2,
                                                              self))


class Enemy(Tank):
    def __init__(self, image, all_images, initial_position, level, enemy_type):
        super().__init__(image,
                         initial_position,
                         config.enemy_label[enemy_type]['level' + str(level)]['fire_speed'],
                         1)
        self.images = all_images[level]  # 读取该等级的一系列图片
        self.image = self.images[0][0]  # 定义初始朝向
        self.all_images = all_images  # 存放该类型所有等级的坦克图片

        # 敌方坦克label
        self.initial_level = level
        self.level = level  # 存放等级
        self.enemy_type = enemy_type  # 存放坦克类型
        self.speed = config.enemy_label[self.enemy_type]['level' + str(self.level)]['move_speed']  # 初始化坦克速度
        self.initial_HP = config.enemy_label[self.enemy_type]['level' + str(self.level)]['HP']  # 存放该坦克类型该等级的总血量
        self.score = config.enemy_label[self.enemy_type]['level' + str(self.level)]['score']  # 存放该坦克被玩家击杀后的分数
        self.HP = self.initial_HP  # 初始化该坦克血量
        self.move_time = time.time() - 1  # 用于监控敌方强制自动改变朝向间隔

    # 敌方坦克移动
    def move(self):
        move_time = time.time()
        if move_time - self.move_time > random.uniform(3.0, 6.0):  # 随机产生强制转向间隔
            self.move_time = move_time
            self.dir = random.randint(0, 3)
        if self.dir == 0:
            self.rect.top = self.old_topleft[1] - (self.speed + self.ice_faster + self.is_faster)
            self.rect.left = self.old_topleft[0]
        elif self.dir == 1:
            self.rect.left = self.old_topleft[0] + (self.speed + self.ice_faster + self.is_faster)
            self.rect.top = self.old_topleft[1]
        elif self.dir == 2:
            self.rect.top = self.old_topleft[1] + (self.speed + self.ice_faster + self.is_faster)
            self.rect.left = self.old_topleft[0]
        else:
            self.rect.left = self.old_topleft[0] - (self.speed + self.ice_faster + self.is_faster)
            self.rect.top = self.old_topleft[1]
        self.image = self.images[self.dir][self.dir_lst[self.dir]]
        self.dir_lst[self.dir] = 1 - self.dir_lst[self.dir]
        self.__fire__()  # 敌方坦克开火

        if self.collide(1):  # 判断是否发生碰撞
            self.dir = (self.dir + random.randint(1, 3)) % 4
            self.rect.topleft = tuple(self.old_topleft)
        self.old_topleft = list(self.rect.topleft)  # 更新旧位置

        self.eat()
        self.food_delay()

    # 敌方坦克扣血/降级
    def reduce_hp(self):
        if self.HP == 1:
            self.level -= 1
            self.images = self.all_images[self.level]
            self.speed = config.enemy_label[self.enemy_type]['level' + str(self.level)]['move_speed']  # 初始化坦克速度
            self.initial_HP = config.enemy_label[self.enemy_type]['level' + str(self.level)]['HP']  # 存放该坦克类型该等级的总血量
            self.HP = self.initial_HP  # 初始化该坦克血量
            self.fire_space = config.enemy_label[self.enemy_type]['level' + str(self.level)]['fire_speed']  # 存放开火间隔
        else:
            self.HP -= 1
            left = self.rect.left - 10
            top = self.rect.top - 10
            if top < 0:
                top = self.rect.bottom + 10
            config.Maps.group_lst['blood_group'].add(Blood((left, top),
                                                           self.HP,
                                                           self.initial_HP))


class MiniTank(Tank):
    def __init__(self, image, images, initial_position, fire_space, move_speed, father_tank):
        super().__init__(image, initial_position, fire_space, 2)
        self.images = images
        self.image = self.images[0][0]
        self.speed = move_speed
        self.move_time = time.time() - 1
        self.father_tank = father_tank

    def move(self):
        move_time = time.time()
        if move_time - self.move_time > random.uniform(3.0, 6.0):  # 随机产生强制转向间隔
            self.move_time = move_time
            self.dir = random.randint(0, 3)
        if self.dir == 0:
            self.rect.top = self.old_topleft[1] - (self.speed + self.ice_faster)
            self.rect.left = self.old_topleft[0]
        elif self.dir == 1:
            self.rect.left = self.old_topleft[0] + (self.speed + self.ice_faster)
            self.rect.top = self.old_topleft[1]
        elif self.dir == 2:
            self.rect.top = self.old_topleft[1] + (self.speed + self.ice_faster)
            self.rect.left = self.old_topleft[0]
        else:
            self.rect.left = self.old_topleft[0] - (self.speed + self.ice_faster)
            self.rect.top = self.old_topleft[1]
        self.image = self.images[self.dir][self.dir_lst[self.dir]]
        self.dir_lst[self.dir] = 1 - self.dir_lst[self.dir]
        self.__fire__()  # 敌方坦克开火

        if self.collide(0):  # 判断是否发生碰撞
            self.dir = (self.dir + random.randint(1, 3)) % 4
            self.rect.topleft = tuple(self.old_topleft)
        self.old_topleft = list(self.rect.topleft)  # 更新旧位置
