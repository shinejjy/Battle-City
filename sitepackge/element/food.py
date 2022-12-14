import time

import pygame

from sitepackge import config


class Food(pygame.sprite.Sprite):
    def __init__(self, images, initial_position, types):
        super().__init__()
        self.images = images
        self.rect = self.images[0].get_rect()
        self.index = 0
        self.image = self.images[self.index]
        self.rect.topleft = initial_position
        self.shine_time = time.time() - 0.5
        self.type = types

    def updates(self):
        now = time.time()
        if now - self.shine_time > 0.5:
            self.shine_time = now
            self.index = 1 - self.index
            self.image = self.images[self.index]

    def effect(self, tank):
        if self.type == 1:  # board
            tank.delay_board(is_initial=True)
        elif self.type == 2:  # faster
            tank.delay_faster(is_initial=True)
        elif self.type == 3:  # shot faster
            tank.delay_shot_faster(is_initial=True)
        elif self.type == 5:  # cover
            tank.delay_cover(is_initial=True)
        elif self.type == 7:  # strong
            tank.delay_strong(is_initial=True)

        if tank.tank_type == 0:
            if self.type != 4 and self.type != 2:
                config.audio_dict['food'].play()
            elif self.type == 2:
                config.audio_dict['move_speed'].play()
            if self.type == 0:  # save for another
                if tank.tank_type == 0:
                    for player in config.Maps.group_lst['player_group']:
                        if not player.HP:
                            player.be_saved()
            elif self.type == 4:  # upgrade
                config.audio_dict['upgrade'].play()
                tank.upgrade()
            elif self.type == 6:  # tracking_bomb
                tank.n_bomb = min(tank.n_bomb + 1, 4)
            elif self.type == 8:  # mini_tank
                tank.create_mini_tank()
            elif self.type == 9:  # HP++
                tank.HP = min(config.player_label[tank.level]['HP'], tank.HP + 1)
