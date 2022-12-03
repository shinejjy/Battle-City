from __future__ import annotations
import time

import pygame


def get_text_surface(text, color, font):
    return font.render(text, True, color)


def draw_text(text, color, font, position, surface, scale):
    image = get_text_surface(text, color, font)
    width, height = image.get_size()
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    surface.blit(image, position)


class Text:
    def __init__(self, text, color, font, position, scale):
        self.image = get_text_surface(text, color, font)
        width, height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.position = position

    def draw(self, surface):
        surface.blit(self.image, self.position)


class Image:
    def __init__(self, image, position, scale):
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.position = position

    def draw(self, surface):
        surface.blit(self.image, self.position)


class Gif:
    def __init__(self, images, position, scale):
        self.images = images[:]
        width, height = images[0].get_size()
        for index, image in enumerate(self.images):
            self.images[index] = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.position = position
        self.index = 0
        self.len = len(self.images)

    def draw(self, surface):
        surface.blit(self.images[self.index], self.position)
        self.index = (self.index + 1) % self.len


class DisplayButton:
    def __init__(self, image, position, scale, content: Image | Text | Gif):
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.content = content
        self.stay_time = None
        self.stay = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if self.stay:
                if time.time() - self.stay_time > 2:
                    self.content.draw(surface)
            else:
                self.stay = True
                self.stay_time = time.time()
        else:
            self.stay = False


class Button:
    def __init__(self, text, position, color, font, scale, event, middle_width=0):
        image = get_text_surface(text, color, font)
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        if middle_width:
            self.rect.topleft = (middle_width - self.image.get_width()) / 2, position[1]
        self.clicked = False
        self.event = event

    def draw(self, surface):
        action = False
        bk = pygame.draw.rect(surface, (0, 0, 0), self.rect)

        # 获取鼠标位置：
        pos = pygame.mouse.get_pos()

        # 鼠标划过按钮并点击
        if bk.collidepoint(pos):
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 3)
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
                pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, self.rect.topleft)

        return action


class Menu:
    def __init__(self, bk_image=None):
        self.bk_image = bk_image
        self.button_group = []
        self.text_group = []
        self.image_group = []
        self.gif_group = []
        self.sub_menu_group = []

    def draw(self, surface):
        if self.bk_image:
            surface.blit(self.bk_image, (0, 0))
        for text in self.text_group:
            text.draw(surface)
        for button in self.button_group:
            if button.draw(surface):
                return button.event
        for image in self.image_group:
            image.draw(surface)
        for gif in self.gif_group:
            gif.draw(surface)

    def add_text(self, text: Text):
        self.text_group.append(text)

    def add_button(self, button: Button):
        self.button_group.append(button)

    def add_image(self, image: Image):
        self.image_group.append(image)

    def add_gif(self, gif: Gif):
        self.gif_group.append(gif)
