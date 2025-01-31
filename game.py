import pprint

import pygame
import os
import sys
from random import choice
from p_classes import Board, SpritePictures, NormalSprite, HealphBar, Ground, PlayerSprite, BulletSprite, \
    BulletMonsterSprite, Turns
from p_game_classes import dogge_move, turning


def game_sobstvenno(music_value=0.0, harding=1, *args, **kwargs):
    # подготовка
    pygame.init()
    pygame.display.set_caption('game')
    size = 550, 550
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill('black')

    # спрайты интефейса
    all_sprites = pygame.sprite.Group()
    health = HealphBar(all_sprites, 6, 21)  # здоровье

    # поле
    ground = Ground(screen, 500, 500, 50)
    ground.deep_init((5, 5))
    ground.add_object(
        BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 3, ground.board.cell_size * 4,
                            (ground.board.cell_size, ground.board.cell_size)), (3, 4))
    ground.add_object(
        BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 6, ground.board.cell_size * 6,
                            (ground.board.cell_size, ground.board.cell_size)), (6, 6))
    all_sprites.draw(screen)

    if harding == 1 or harding == 2:
        pygame.mixer.music.load('data/James Primate — Threat - Garbage Wastes.mp3')
    elif harding == 3:
        pygame.mixer.music.load('data/Connor (12Lbs) Skidmore  — Sheer Ice Torrent.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_value)
    turn = Turns()
    turn.deep_init(ground)
    turn.add_object(ground, (3, 4))
    turn.add_object(ground, (6, 6))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ground.get_click(event.pos)
            if True in pygame.key.get_pressed():
                if turn:
                    # если нужен индекс кнопки print(pygame.key.get_pressed().index(True))
                    if pygame.key.get_pressed().index(True) in [79, 80, 81, 82]:
                        dogge_move(ground)
                        turn.re_turn()

        screen.fill('black')
        ground.render()
        for i in range(len(turn.bodies)):
            ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].cicle_animation()
        if not turn:
            turning(ground, turn, health)
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(200)


# def main():

if __name__ == '__main__':
    game_sobstvenno(harding=3, music_value=1)
