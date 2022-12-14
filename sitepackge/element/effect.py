import math
import time

import pygame

from sitepackge import config


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, images, initial_position, dirs, types, from_tank):
        super().__init__()
        self.dirs = dirs
        self.images = images
        self.image = self.images[self.dirs]
        self.rect = image.get_rect()
        self.rect.topleft = initial_position
        self.rebounds = 4
        speed = config.bullet_speed
        if dirs == 0:
            self.speed = [0, -speed]
        elif dirs == 1:
            self.speed = [speed, 0]
        elif dirs == 2:
            self.speed = [0, speed]
        else:
            self.speed = [-speed, 0]
        # __type__ 0 表示己方 1 表示敌方
        self.type = types
        self.from_tank = from_tank  # 表示tank来源

    def move(self):
        self.rect = self.rect.move(self.speed)
        self.kills()
        if self.type == 0 or self.type == 2:
            self.hit_enemy_tank()
            self.hit_enemy_bullet()
        elif self.type == 1:
            self.hit_player_tank()
            self.hit_mini_tank()
            self.hit_player_or_mini_tank_bullet()
        if self.type == 0 or self.type == 1:
            self.hit_wall()
            if self.game_over():
                return True
        elif self.type == 2:
            self.mini_hit_wall()

    def hit_enemy_tank(self):
        for enemy in config.Maps.group_lst['enemy_group']:
            if pygame.sprite.collide_rect(enemy, self):
                config.Maps.group_lst['player_bullet_group'].remove(self)
                if enemy.cover_level != 0:  # 如果敌方坦克有保护罩
                    enemy.now_cover_time = time.time() - enemy.cover_time
                else:  # 如果敌方坦克无保护罩
                    if enemy.level == 0 and enemy.HP == 1:  # 如果敌方坦克等级为0且血量为1，则死亡
                        config.audio_dict['boom'].play()
                        config.Maps.group_lst['enemy_group'].remove(enemy)
                        boom = Boom(image=config.image_dict['blank'][0],
                                    images=config.image_dict['boom'],
                                    initial_position=enemy.rect.center,
                                    score=enemy.score // 100 - 1,
                                    end=2)
                        config.Maps.group_lst['boom_group'].add(boom)
                        self.from_tank.score += enemy.score
                        self.from_tank.enemy_kill += 1
                        del enemy
                    else:  # 否则，扣血
                        enemy.reduce_hp()
                del self
                return

    def hit_player_tank(self):
        for player in config.Maps.group_lst['player_group']:
            if player.HP > 0 and pygame.sprite.collide_rect(player, self):
                config.Maps.group_lst['enemy_bullet_group'].remove(self)
                if player.cover_level != 0:  # 如果玩家有保护罩
                    player.now_cover_time = time.time() - player.cover_time
                elif not player.is_invincible:  # 如果玩家无保护罩且无被攻击保护
                    if player.HP > 1:  # 如果玩家血量大于1，扣血
                        player.reduce_hp()
                        player.invincible(True)
                    else:
                        player.kills()  # 如果玩家血量等于1，死亡
                        boom = Boom(config.image_dict['blank'][0], config.image_dict['boom'], player.rect.center, -1, 2)
                        config.Maps.group_lst['boom_group'].add(boom)
                del self
                return

    def hit_mini_tank(self):
        for mini_tank in config.Maps.group_lst['mini_tank_group']:
            if pygame.sprite.collide_rect(mini_tank, self):
                config.Maps.group_lst['enemy_bullet_group'].remove(self)
                config.Maps.group_lst['mini_tank_group'].remove(mini_tank)
                del mini_tank
                del self
                return

    def hit_enemy_bullet(self):
        for enemy_bullet in config.Maps.group_lst['enemy_bullet_group']:
            if pygame.sprite.collide_rect(enemy_bullet, self):
                config.Maps.group_lst['enemy_bullet_group'].remove(enemy_bullet)
                config.Maps.group_lst['player_bullet_group'].remove(self)
                del enemy_bullet
                del self
                return

    def hit_player_or_mini_tank_bullet(self):
        for player_bullet in config.Maps.group_lst['player_bullet_group']:
            if pygame.sprite.collide_rect(player_bullet, self):
                config.Maps.group_lst['player_bullet_group'].remove(player_bullet)
                config.Maps.group_lst['enemy_bullet_group'].remove(self)
                del player_bullet
                del self
                return
        for mini_tank_bullet in config.Maps.group_lst['mini_tank_bullet_group']:
            if pygame.sprite.collide_rect(mini_tank_bullet, self):
                config.Maps.group_lst['mini_tank_bullet_group'].remove(mini_tank_bullet)
                config.Maps.group_lst['enemy_bullet_group'].remove(self)
                del mini_tank_bullet
                del self
                return

    def game_over(self):
        for base in config.Maps.group_lst['base_group']:
            if pygame.sprite.collide_rect(base, self):
                return True

    def hit_wall(self):
        f = False
        for brick in config.Maps.group_lst['brick_group']:
            if pygame.sprite.collide_rect(brick, self):
                config.Maps.group_lst['brick_group'].remove(brick)
                if self.type == 0:
                    config.Maps.group_lst['player_bullet_group'].remove(self)
                else:
                    config.Maps.group_lst['enemy_bullet_group'].remove(self)
                del brick
                f = True

        for iron in config.Maps.group_lst['iron_group']:
            if pygame.sprite.collide_rect(iron, self):
                if self.from_tank.is_strong:
                    config.Maps.group_lst['iron_group'].remove(iron)
                elif not self.from_tank.is_strong and self.type == 0:
                    config.audio_dict['hit-iron'].play()
                if self.type == 0:
                    config.Maps.group_lst['player_bullet_group'].remove(self)
                else:
                    config.Maps.group_lst['enemy_bullet_group'].remove(self)
                del iron
                f = True

        for slime in config.Maps.group_lst['slime_group']:
            if pygame.sprite.collide_rect(slime, self):
                if self.from_tank.is_strong:
                    if self.type == 0:
                        config.Maps.group_lst['player_bullet_group'].remove(self)
                    else:
                        config.Maps.group_lst['enemy_bullet_group'].remove(self)
                    config.Maps.group_lst['slime_group'].remove(slime)
                    f = True
                    break
                elif not self.from_tank.is_strong and self.type == 0:
                    config.audio_dict['slime'].play()
                if self.rebounds == 0:
                    if self.type == 0:
                        config.Maps.group_lst['player_bullet_group'].remove(self)
                    else:
                        config.Maps.group_lst['enemy_bullet_group'].remove(self)
                    break
                # if self.type == 0:
                # config.audio_dict['slime'])
                # pygame.mixer.music.play()
                self.dirs = (self.dirs + 2) % 4
                self.updates()
                while pygame.sprite.collide_rect(slime, self):
                    if 1 <= self.dirs <= 2:
                        if self.dirs % 2 == 0:
                            self.rect.top += 1
                        else:
                            self.rect.left += 1
                    else:
                        if self.dirs % 2 == 0:
                            self.rect.top -= 1
                        else:
                            self.rect.left -= 1
                self.rebounds -= 1
                break
        if f:
            del self

    def mini_hit_wall(self):
        for item in config.Maps.group_lst['brick_group'].sprites() + config.Maps.group_lst['iron_group'].sprites() + \
                    config.Maps.group_lst['base_group'].sprites() + config.Maps.group_lst['slime_group'].sprites():
            if pygame.sprite.collide_rect(item, self):
                config.Maps.group_lst['mini_tank_bullet_group'].remove(self)
                del self
                return

    def kills(self):
        if self.rect.left < 0 \
                or self.rect.right > config.width \
                or self.rect.top < 0 \
                or self.rect.bottom > config.height:
            if self.type == 0:
                config.Maps.group_lst['player_bullet_group'].remove(self)
            elif self.type == 1:
                config.Maps.group_lst['enemy_bullet_group'].remove(self)
            elif self.type == 2:
                config.Maps.group_lst['mini_tank_bullet_group'].remove(self)
            del self

    def updates(self):
        speed = config.bullet_speed
        if self.dirs == 0:
            self.speed = [0, -speed]
        elif self.dirs == 1:
            self.speed = [speed, 0]
        elif self.dirs == 2:
            self.speed = [0, speed]
        else:
            self.speed = [-speed, 0]
        self.image = self.images[self.dirs]


class TrackingBomb(pygame.sprite.Sprite):
    def __init__(self, image, initial_image, initial_position, to_tank, from_tank):
        super().__init__()
        self.rect = image.get_rect()
        self.rect.center = initial_position
        self.image = initial_image
        self.initial_image = initial_image
        self.to_tank = to_tank
        self.from_tank = from_tank
        self.move()

    def move(self):
        self.collide()
        x1, y1 = self.rect.center
        x, y = self.to_tank.rect.center
        dis = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        sin_a = (y1 - y) / dis
        cos_a = (x - x1) / dis
        angle = math.atan(sin_a / cos_a) / math.pi * 180 if cos_a else 90
        if angle < 0 and cos_a < 0:
            angle += 180
        elif cos_a < 0 < angle:
            angle -= 180
        self.image = pygame.transform.rotate(self.initial_image, angle)
        self.rect = self.image.get_rect(center=(x1 + 6 * cos_a, y1 - 18 * sin_a))

    def collide(self):
        if pygame.sprite.collide_rect(self, self.to_tank):
            config.audio_dict['boom'].play()
            config.Maps.group_lst['tracking_bomb_group'].remove(self)
            config.Maps.group_lst['enemy_group'].remove(self.to_tank)
            boom = Boom(image=config.image_dict['blank'][3],
                        images=config.image_dict['boom'],
                        initial_position=self.to_tank.rect.center,
                        score=self.to_tank.score // 100 - 1,
                        end=4)
            config.Maps.group_lst['boom_group'].add(boom)
            self.from_tank.score += self.to_tank.score
            self.from_tank.enemy_kill += 1
            del self


class Boom(pygame.sprite.Sprite):
    def __init__(self, image, images, initial_position, score, end):
        super().__init__()
        self.image = images[0]
        self.images = images
        if end == 2:
            self.rect = image.get_rect()
            self.rect.center = initial_position
        elif end == 4:
            surface = pygame.Surface((64 * 2, 64 * 2), pygame.SRCALPHA, 32)
            surface.blit(self.image,
                         ((surface.get_width() - self.image.get_width()) / 2,
                          (surface.get_height() - self.image.get_width()) / 2))
            self.image = surface
            self.rect = self.image.get_rect()
            self.rect.center = initial_position
            self.initial_position = initial_position
        self.index = 0
        self.update_time = time.time()
        self.score = score
        self.end = end

    def updates(self):
        now = time.time()
        if now - self.update_time > 0.1:
            self.update_time = now
            if self.index == self.end:
                config.Maps.group_lst['boom_group'].remove(self)
                if self.score >= 0:
                    config.Maps.group_lst['score_group'].add(Score(blank=config.image_dict['blank'][0],
                                                                   image=config.image_dict['score'][self.score],
                                                                   initial_position=self.rect.center))
                del self
            else:
                self.index += 1
                self.image = self.images[self.index]
                if self.end == 4:
                    surface = pygame.Surface((64 * 2, 64 * 2), pygame.SRCALPHA, 32)
                    surface.blit(self.image,
                                 ((surface.get_width() - self.image.get_width()) / 2,
                                  (surface.get_height() - self.image.get_width()) / 2))
                    self.image = surface
                    self.rect = self.image.get_rect()
                    self.rect.center = self.initial_position


class Blood(pygame.sprite.Sprite):
    def __init__(self, initial_position, HP, initial_HP):
        super().__init__()
        green = pygame.Surface(size=(88, 5))
        green.fill((0, 255, 0))
        red = pygame.Surface(size=(88 - HP / initial_HP * 88 + 1, 5))
        red.fill((255, 0, 0))
        self.rect = green.blit(red, (HP / initial_HP * 88, 0))
        self.rect.topleft = initial_position
        self.image = green
        self.live_time = 8

    def updates(self):
        if self.live_time > 0:
            self.live_time -= 1
        else:
            config.Maps.group_lst['blood_group'].remove(self)
            del self


class Score(pygame.sprite.Sprite):
    def __init__(self, blank, image, initial_position):
        super().__init__()
        self.rect = blank.get_rect()
        self.rect.center = initial_position
        self.alpha = 255
        self.image = image
        self.update_time = time.time()

    def updates(self):
        now = time.time()
        if now - self.update_time < 0.13:
            return
        self.update_time = now
        if self.alpha - 25.5 > 0:
            self.alpha -= 25.5
            self.image.set_alpha(self.alpha)
        else:
            config.Maps.group_lst['score_group'].remove(self)
            del self


class Cover(pygame.sprite.Sprite):
    def __init__(self, image, initial_position, on_tank, cover_type):
        super().__init__()
        self.rect = image.get_rect()
        self.rect.topleft = initial_position
        self.image = image
        self.on_tank = on_tank
        self.cover_type = cover_type

    def updates(self):
        if self.cover_type == 'normal' and self.on_tank.cover_level == 0 or \
                self.cover_type == 'special' and self.on_tank.tank_type == 0 and not self.on_tank.is_invincible:
            config.Maps.group_lst['cover_group'].remove(self)
            del self
        else:
            self.rect.topleft = self.on_tank.rect.topleft
