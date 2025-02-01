import pygame
import os
import sys
from random import choice
from p_classes import Board, SpritePictures, NormalSprite, HealphBar, Ground, PlayerSprite, BulletSprite, \
    BulletMonsterSprite, Turns


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


def turning(ground: Ground, turn: Turns, health: HealphBar):
    player_pos = ground.player_pos
    for i in range(len(turn.bodies)):
        if isinstance(turn.bodies[i][0], BulletMonsterSprite):
            c1, c2 = choice([-1, 0, 1]), choice([-1, 0, 1])
            if turn.bodies[i][1][0] == 0:
                c1 = 1
            elif turn.bodies[i][1][0] + 1 == len(ground.objects[0]) - 6:
                c1 = -1
            if turn.bodies[i][1][1] == 0:
                c2 = 1
            elif turn.bodies[i][1][1] + 1 == len(ground.objects) - 6:
                c2 = -1
            if not c1 and not c2:
                if not ground.objects[turn.bodies[i][1][0] + 0][turn.bodies[i][1][1] + 1]:
                    ground.add_object(
                        BulletSprite(ground.objects_sprites, ground.board.cell_size * (turn.bodies[i][1][0] + 0),
                                     ground.board.cell_size * (turn.bodies[i][1][1] + 1),
                                     (ground.board.cell_size, ground.board.cell_size)),
                        (turn.bodies[i][1][0] + 0, turn.bodies[i][1][1] + 1))
                    turn.add_object(ground, (turn.bodies[i][1][0] + 0, turn.bodies[i][1][1] + 1))
                    print('BulletMonster проталкивает часть себя ближе к клавиатуре!')
            elif not ground.objects[turn.bodies[i][1][0] + c1][turn.bodies[i][1][1] + c2]:
                ground.move_object(turn.bodies[i][1],
                                   (turn.bodies[i][1][0] + c1, turn.bodies[i][1][1] + c2))
                turn.bodies[i] = (turn.bodies[i][0],
                                  (turn.bodies[i][1][0] + c1,
                                   turn.bodies[i][1][1] + c2))
            elif isinstance(ground.objects[turn.bodies[i][1][0] + c1][turn.bodies[i][1][1] + c2], PlayerSprite):
                print('BulletMonster врезался в собакена!')
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].kill()
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]] = None
                turn.bodies[i] = (None,
                                  (turn.bodies[i][1][0],
                                   turn.bodies[i][1][1]))
                health -= 1
        elif isinstance(turn.bodies[i][0], BulletSprite):
            what_it_do_in_this_turn = (0, 0)
            if turn.bodies[i][1][0] == player_pos[0] or turn.bodies[i][1][1] == player_pos[1]:
                if turn.bodies[i][1][0] == player_pos[0]:
                    if turn.bodies[i][1][1] < player_pos[1]:
                        what_it_do_in_this_turn = (what_it_do_in_this_turn[0], what_it_do_in_this_turn[1] + 1)
                    else:
                        what_it_do_in_this_turn = (what_it_do_in_this_turn[0], what_it_do_in_this_turn[1] - 1)
                elif turn.bodies[i][1][1] == player_pos[1]:
                    if turn.bodies[i][1][0] < player_pos[0]:
                        what_it_do_in_this_turn = (what_it_do_in_this_turn[0] + 1, what_it_do_in_this_turn[1])
                    else:
                        what_it_do_in_this_turn = (what_it_do_in_this_turn[0] - 1, what_it_do_in_this_turn[1])
            c1, c2 = what_it_do_in_this_turn
            if not ground.objects[turn.bodies[i][1][0] + c1][turn.bodies[i][1][1] + c2]:
                ground.move_object(turn.bodies[i][1],
                                   (turn.bodies[i][1][0] + c1, turn.bodies[i][1][1] + c2))
                turn.bodies[i] = (turn.bodies[i][0],
                                  (turn.bodies[i][1][0] + c1,
                                   turn.bodies[i][1][1] + c2))
            elif isinstance(ground.objects[turn.bodies[i][1][0] + c1][turn.bodies[i][1][1] + c2], PlayerSprite):
                print('BulletMonster врезался в собакена!')
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].kill()
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]] = None
                turn.bodies[i] = (None,
                                  (turn.bodies[i][1][0],
                                   turn.bodies[i][1][1]))
                health -= 1
    for i in turn.bodies:
        if not i[0]:
            del turn.bodies[turn.bodies.index(i)]

    turn.re_turn()
# ground.move_object(turn.bodies[0][1], (turn.bodies[0][1][0] + 1, turn.bodies[0][1][1]))
# turn.bodies[0] = (turn.bodies[0][0], (turn.bodies[0][1][0] + 1, turn.bodies[0][1][1]))
