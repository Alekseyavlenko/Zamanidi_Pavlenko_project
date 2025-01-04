import pygame
import os
import sys
from p_classes import Board, SpritePictures, NormalSprite, HealphBar


def game_sobstvenno(*args, **kwargs):
    pygame.init()
    pygame.display.set_caption('game')
    size = 500, 500
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill('black')
    all_sprites = pygame.sprite.Group()
    # health = NormalSprite(all_sprites, -100, -100, SpritePictures(n1='valentine_heart.png',n2='valentine_broken_heart.png'), (18, 18))
    # health = [health.clone() for i in range(6)]
    # for i in range(len(health)):
    # health[i].update_rect((i * 21) + 1, 1)
    health = HealphBar(all_sprites, 6, 21)

    # health[i].scale(18, 18) for i in range(len(health))
    # health = [health[i].update_rect((i * 21) + 1, 1) for i in range(len(health))]
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        # healph_bar.render(screen)
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
