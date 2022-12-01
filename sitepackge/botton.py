import pygame


def get_text_surface(text, color, font):
    return font.render(text, True, color)


def draw_text(text, color, font, position, surface):
    image = get_text_surface(text, color, font)
    surface.blit(image, position)


class Button:
    def __init__(self, text, position, color, font, scale):
        image = get_text_surface(text, color, font)
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.clicked = False

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
