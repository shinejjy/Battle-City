import pygame
import time


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, initial_position):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.rect.topleft = initial_position


class River(Wall):
    def __init__(self, image, images, initial_position):
        super().__init__(image, initial_position)
        self.index = 0
        self.update_time = time.time() - 0.5
        self.image = images[self.index]
        self.images = images

    def updates(self):
        now = time.time()
        if now - self.update_time > 0.5:
            self.update_time = now
            self.index = 1 - self.index
            self.image = self.images[self.index]


class Brick(Wall):
    def __init__(self, image, initial_position):
        super().__init__(image, initial_position)


class Tree(Wall):
    def __init__(self, image, initial_position):
        super().__init__(image, initial_position)


class Base(Wall):
    def __init__(self, image, initial_position):
        super().__init__(image, initial_position)


class Ice(Wall):
    def __init__(self, image, initial_position):
        super().__init__(image, initial_position)


class Iron(Wall):
    def __init__(self, image, initial_position):
        super().__init__(image, initial_position)


class Slime(Wall):
    def __init__(self, image, initial_position):
        super().__init__(image, initial_position)


class Startpoint(Wall):
    def __init__(self, image, images, initial_position):
        super().__init__(image, initial_position)
        self.images = images
        self.index = 0
        self.image = images[self.index]

    def updates(self):
        self.index = (self.index + 1) % 5
        self.image = self.images[self.index]
        if self.index == 0:
            return True
        return False
