import pygame
import os
import sys


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
        screen.fill('black')
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(200)


if __name__ == '__main__':
    main()
