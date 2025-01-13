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
    all_sprites.draw(screen)
    pygame.mixer.music.load('data/James Primate — Threat - Garbage Wastes.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ground.get_click(event.pos)
            if True in pygame.key.get_pressed():
                print(pygame.key.get_pressed().index(True))
                if pygame.key.get_pressed().index(True) == 79:
                    ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                                       (ground.player_pos[0] + 1, ground.player_pos[1]),
                                       tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
                    ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True)
                if pygame.key.get_pressed().index(True) == 80:
                    ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                                       (ground.player_pos[0] - 1, ground.player_pos[1]),
                                       tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
                    ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True)
                if pygame.key.get_pressed().index(True) == 82:
                    ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                                       (ground.player_pos[0], ground.player_pos[1] - 1),
                                       tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
                    ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True)
                if pygame.key.get_pressed().index(True) == 81:
                    ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                                       (ground.player_pos[0], ground.player_pos[1] + 1),
                                       tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
                    ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True)
                if (ground.player_pos[0] < 0 or ground.player_pos[0] > len(
                        ground.board.board[0])) // ground.board.cell_size or (
                        ground.player_pos[1] < 0 or ground.player_pos[1] >
                        len(ground.board.board) // ground.board.cell_size):
                    print('собакен выпал из мира')
                    # running = False
        screen.fill('black')
        ground.render()
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(200)


# def main():

if __name__ == '__main__':
    game_sobstvenno()
