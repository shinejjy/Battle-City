import pygame
import time


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, initial_position):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.rect.topleft = initial_position


class DynamicWall(Wall):
    def __init__(self, image, images, initial_position, space_time):
        super().__init__(image, initial_position)
        self.index = 0
        self.update_time = time.time() - 0.5
        self.image = images[self.index]
        self.images = images
        self.len = len(images)
        self.space_time = space_time

    def updates(self):
        now = time.time()
        if now - self.update_time > self.space_time:
            self.update_time = now
            self.index = (self.index + 1) % self.len
            self.image = self.images[self.index]
            if self.index == 0:
                return 'new'
            else:
                return True
        else:
            return False
