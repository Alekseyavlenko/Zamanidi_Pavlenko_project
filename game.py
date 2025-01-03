import pygame
import os
import sys
from p_classes import Board, load_image


def game_sobstvenno(*args, **kwargs):
    pygame.init()
    pygame.display.set_caption('game')
    size = 500, 500
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill('black')
    all_sprites = pygame.sprite.Group()
    all_sprites.draw(screen)
    healph_bar = Board(6, 1, 0, 0, 20)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        healph_bar.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        # pygame.time.Clock().tick(200)


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
    game_sobstvenno()
