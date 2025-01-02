import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    loading_image = pygame.image.load(fullname)
    if colorkey is not None:
        loading_image = loading_image.convert()
        if colorkey == -1:
            colorkey = loading_image.get_at((0, 0))
        loading_image.set_colorkey(colorkey)
    else:
        loading_image = loading_image.convert_alpha()
    return loading_image


class AbstractSpriteClass(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = load_image("not_founded.png")
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y, need_update_picture=False, update_picture='car2.png', rotation=0, flip_x=False,
               flip_y=False):
        if need_update_picture:
            self.image = load_image(update_picture)
        if flip_x or flip_y:
            self.image = pygame.transform.flip(self.image, flip_x, flip_y)
        if rotation:
            self.image = pygame.transform.rotate(self.image, rotation)
        self.rect.x, self.rect.y = x, y

def main():
    pygame.init()
    pygame.display.set_caption('PG-5.3')
    size = 600, 300
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill('black')
    all_sprites = pygame.sprite.Group()
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('blue')
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(200)


if __name__ == '__main__':
    main()
