import pygame
import os
import sys
from random import choice
from p_classes import Board, SpritePictures, NormalSprite, HealphBar, Ground, PlayerSprite, BulletMonsterSprite, Turns
from p_game_classes import dogge_move


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
    ground.add_object(
        BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 4, ground.board.cell_size * 4,
                            (ground.board.cell_size, ground.board.cell_size)), (4, 4))
    all_sprites.draw(screen)
    pygame.mixer.music.load('data/James Primate — Threat - Garbage Wastes.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.0)
    turn = Turns()
    turn.deep_init(ground)
    turn.add_object(ground, (3, 4))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ground.get_click(event.pos)
            if True in pygame.key.get_pressed():
                if turn:
                    print(pygame.key.get_pressed().index(True))
                    if pygame.key.get_pressed().index(True) in [79, 80, 81, 82]:
                        dogge_move(ground)
                        turn.re_turn()

        screen.fill('black')
        ground.render()
        if not turn:
            ground.move_object(turn.bodies[0][1], (turn.bodies[0][1][0] + 1, turn.bodies[0][1][1]))
            turn.bodies[0] = (turn.bodies[0][0], (turn.bodies[0][1][0] + 1, turn.bodies[0][1][1]))
            turn.re_turn()
        for i in range(len(turn.bodies)):
            ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].cicle_animation()
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(200)


# def main():

if __name__ == '__main__':
    game_sobstvenno()