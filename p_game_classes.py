import pygame
import os
import sys
from random import choice
from p_classes import Board, SpritePictures, NormalSprite, HealphBar, Ground, PlayerSprite, BulletMonsterSprite, Turns


def dogge_move(ground):
    if pygame.key.get_pressed().index(True) == 79:
        ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                           (ground.player_pos[0] + 1, ground.player_pos[1]),
                           tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
        ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True)
    if pygame.key.get_pressed().index(True) == 80:
        ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                           (ground.player_pos[0] - 1, ground.player_pos[1]),
                           tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
        ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True,
                                                                                    reverse=1)
    if pygame.key.get_pressed().index(True) == 82:
        ground.move_object((ground.player_pos[0], ground.player_pos[1]),
                           (ground.player_pos[0], ground.player_pos[1] - 1),
                           tipe=ground.objects[ground.player_pos[0]][ground.player_pos[1]])
        ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(run=True, reverse=1)
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
