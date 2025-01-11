import pygame
import os
import sys
from random import choice
from p_classes import Board, SpritePictures, NormalSprite, HealphBar, Ground, PlayerSprite


def game_sobstvenno(*args, **kwargs):
    pygame.init()
    pygame.display.set_caption('game')
    size = 550, 550
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill('black')
    all_sprites = pygame.sprite.Group()
    health = HealphBar(all_sprites, 6, 21)
    ground = Ground(screen, 500, 500, 50)
    ground.deep_init((5, 5))
    # ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True)
    for i in range(11):
        for g in range(11):
            ground.assign_sprite(SpritePictures(n1=choice(['Grass-300x300.jpg',
                                                           '20190901_152050.png'])), (i, g))
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ground.get_click(event.pos)
        screen.fill('black')
        ground.render()
        all_sprites.draw(screen)
        pygame.display.flip()
        # pygame.time.Clock().tick(200)


# def main():

if __name__ == '__main__':
    game_sobstvenno()
