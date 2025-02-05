import pygame
import os
import sys
from random import choice
from p_classes import Board, SpritePictures, NormalSprite, HealphBar, Ground, PlayerSprite, BulletSprite, \
    BulletMonsterSprite, Turns, Jaw, JawsBar, Heal


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


def dagge_fight(ground: Ground, turn: Turns, jawsbar: JawsBar, healph: HealphBar, hard: int):
    need_to_fight = [(ground.player_pos[0] - 1, ground.player_pos[1] - 1),
                     (ground.player_pos[0] - 1, ground.player_pos[1]),
                     (ground.player_pos[0] - 1, ground.player_pos[1] + 1),
                     (ground.player_pos[0], ground.player_pos[1] + 1),
                     (ground.player_pos[0] + 1, ground.player_pos[1] + 1),
                     (ground.player_pos[0] + 1, ground.player_pos[1]),
                     (ground.player_pos[0] + 1, ground.player_pos[1] - 1),
                     (ground.player_pos[0], ground.player_pos[1] - 1)]
    if jawsbar.is_exists_or_not_exists():
        print('собакен бросается в атаку!')
        hp = 0
        for i in need_to_fight:
            if isinstance(ground.objects[i[0]][i[1]], BulletSprite):
                del turn.bodies[turn.bodies.index((ground.objects[i[0]][i[1]], i))]
                ground.objects[i[0]][i[1]].kill()
                ground.objects[i[0]][i[1]] = None
                hp += 1
            if isinstance(ground.objects[i[0]][i[1]], BulletMonsterSprite):
                del turn.bodies[turn.bodies.index((ground.objects[i[0]][i[1]], i))]
                ground.objects[i[0]][i[1]].kill()
                ground.objects[i[0]][i[1]] = None
                hp += 1
        if hp:
            if hard == 1:
                healph += 1

    else:
        print('у собакена нет челюстей для атаки!')
        if hard == 3:
            turn.re_turn()
    jawsbar -= 1
    ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(fight=True, reverse=ground.objects[
        ground.player_pos[0]]
    [ground.player_pos[
            1]].reversing)


def dogge_search(ground: Ground, turn: Turns, jawsbar: JawsBar, healphbar: HealphBar, hard):
    need_to_chek = [(ground.player_pos[0] - 1, ground.player_pos[1] - 1),
                    (ground.player_pos[0] - 1, ground.player_pos[1]),
                    (ground.player_pos[0] - 1, ground.player_pos[1] + 1),
                    (ground.player_pos[0], ground.player_pos[1] + 1),
                    (ground.player_pos[0] + 1, ground.player_pos[1] + 1),
                    (ground.player_pos[0] + 1, ground.player_pos[1]),
                    (ground.player_pos[0] + 1, ground.player_pos[1] - 1),
                    (ground.player_pos[0], ground.player_pos[1] - 1)]
    for i in need_to_chek:
        if isinstance(ground.objects[i[0]][i[1]], Jaw):
            del turn.bodies[turn.bodies.index((ground.objects[i[0]][i[1]], i))]
            ground.objects[i[0]][i[1]].kill()
            ground.objects[i[0]][i[1]] = None
            jawsbar += 1
        if isinstance(ground.objects[i[0]][i[1]], Heal):
            del turn.bodies[turn.bodies.index((ground.objects[i[0]][i[1]], i))]
            ground.objects[i[0]][i[1]].kill()
            ground.objects[i[0]][i[1]] = None
            healphbar += 1
            if hard == 3:
                jawsbar -= 1
    ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(loot=True)


def turning(ground: Ground, turn: Turns, health: HealphBar, harding):
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
            if not c1 and not c2 and harding != 1 and turn.bullet_and_bulletmonster_chek()[0] < 4:
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
                if harding == 3 and turn.bullet_and_bulletmonster_chek()[0] <= 10:
                    if not ground.objects[turn.bodies[i][1][0] + 0][turn.bodies[i][1][1] + 1]:
                        ground.add_object(
                            BulletSprite(ground.objects_sprites, ground.board.cell_size * (turn.bodies[i][1][0] + 0),
                                         ground.board.cell_size * (turn.bodies[i][1][1] + 1),
                                         (ground.board.cell_size, ground.board.cell_size)),
                            (turn.bodies[i][1][0] + 0, turn.bodies[i][1][1] + 1))
                        turn.add_object(ground, (turn.bodies[i][1][0] + 0, turn.bodies[i][1][1] + 1))
            elif isinstance(ground.objects[turn.bodies[i][1][0] + c1][turn.bodies[i][1][1] + c2], PlayerSprite):
                print('BulletMonster врезался в собакена!')
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].kill()
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]] = None
                turn.bodies[i] = (None,
                                  (turn.bodies[i][1][0],
                                   turn.bodies[i][1][1]))
                health -= 1
                ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(passive=True,
                                                                                            reverse=ground.objects[
                                                                                                ground.player_pos[0]]
                                                                                            [ground.player_pos[
                                                                                                    1]].reversing)
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
                print('Bullet врезался в собакена!')
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].kill()
                ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]] = None
                turn.bodies[i] = (None,
                                  (turn.bodies[i][1][0],
                                   turn.bodies[i][1][1]))
                health -= 1
                ground.objects[ground.player_pos[0]][ground.player_pos[1]].change_animation(passive=True,
                                                                                            reverse=ground.objects[
                                                                                                ground.player_pos[0]]
                                                                                            [ground.player_pos[
                                                                                                    1]].reversing)
    for i in turn.bodies:
        if not i[0]:
            del turn.bodies[turn.bodies.index(i)]

    if not turn.jaws_check():
        need_to_spawn_jaws = [(1, 1),
                              (1, len(ground.objects[1]) - 7),
                              (len(ground.objects) - 7, len(ground.objects[1]) - 7),
                              (len(ground.objects) - 7, 1)]
        for _ in range(len(need_to_spawn_jaws)):
            i = choice(need_to_spawn_jaws)
            if not ground.objects[i[0]][i[1]] and not turn.jaws_check():
                ground.add_object(
                    Jaw(ground.objects_sprites, ground.board.cell_size * i[0], ground.board.cell_size * i[1],
                        (ground.board.cell_size, ground.board.cell_size)), i)
                turn.add_object(ground, i)
    if not turn.heal_check() and harding != 3:
        need_to_spawn_heal = [(1, 1),
                              (1, len(ground.objects[1]) - 7),
                              (len(ground.objects) - 7, len(ground.objects[1]) - 7),
                              (len(ground.objects) - 7, 1)]
        for _ in range(len(need_to_spawn_heal)):
            i = choice(need_to_spawn_heal)
            if not ground.objects[i[0]][i[1]] and not turn.heal_check():
                ground.add_object(
                    Heal(ground.objects_sprites, ground.board.cell_size * i[0], ground.board.cell_size * i[1],
                         (ground.board.cell_size, ground.board.cell_size)), i)
                turn.add_object(ground, i)

    if not turn.bullet_and_bulletmonster_chek()[1]:
        can_be_use_to_spawn = []
        if harding == 1:
            for i in range(2, len(ground.objects[1]) - 8):
                for g in range(2, len(ground.objects) - 8):
                    if not ground.objects[i][g] and (i, g) not in [(ground.player_pos[0] - 1, ground.player_pos[1] - 1),
                                                                   (ground.player_pos[0] - 1, ground.player_pos[1]),
                                                                   (ground.player_pos[0] - 1, ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0], ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1]),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1] - 1),
                                                                   (ground.player_pos[0], ground.player_pos[1] - 1),
                                                                   (player_pos[0], player_pos[1])]:
                        can_be_use_to_spawn.append((i, g))
            can_be_use_to_spawn = choice(can_be_use_to_spawn)
            ground.add_object(
                BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * can_be_use_to_spawn[0],
                                    ground.board.cell_size * can_be_use_to_spawn[1],
                                    (ground.board.cell_size, ground.board.cell_size)), can_be_use_to_spawn)
            turn.add_object(ground, can_be_use_to_spawn)
        if harding == 2:
            for i in range(2, len(ground.objects[1]) - 8):
                for g in range(2, len(ground.objects) - 8):
                    if not ground.objects[i][g] and (i, g) not in [(ground.player_pos[0] - 1, ground.player_pos[1] - 1),
                                                                   (ground.player_pos[0] - 1, ground.player_pos[1]),
                                                                   (ground.player_pos[0] - 1, ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0], ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1]),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1] - 1),
                                                                   (ground.player_pos[0], ground.player_pos[1] - 1),
                                                                   (player_pos[0], player_pos[1])]:
                        can_be_use_to_spawn.append((i, g))
            c1 = choice(can_be_use_to_spawn)
            del can_be_use_to_spawn[can_be_use_to_spawn.index(c1)]
            c2 = choice(can_be_use_to_spawn)
            can_be_use_to_spawn = c1, c2
            ground.add_object(
                BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * can_be_use_to_spawn[0][0],
                                    ground.board.cell_size * can_be_use_to_spawn[0][1],
                                    (ground.board.cell_size, ground.board.cell_size)), can_be_use_to_spawn[0])
            turn.add_object(ground, can_be_use_to_spawn[0])
            ground.add_object(
                BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * can_be_use_to_spawn[1][0],
                                    ground.board.cell_size * can_be_use_to_spawn[1][1],
                                    (ground.board.cell_size, ground.board.cell_size)), can_be_use_to_spawn[1])
            turn.add_object(ground, can_be_use_to_spawn[1])
        if harding == 3:
            for i in range(2, len(ground.objects[1]) - 8):
                for g in range(2, len(ground.objects) - 8):
                    if not ground.objects[i][g] and (i, g) not in [(ground.player_pos[0] - 1, ground.player_pos[1] - 1),
                                                                   (ground.player_pos[0] - 1, ground.player_pos[1]),
                                                                   (ground.player_pos[0] - 1, ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0], ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1] + 1),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1]),
                                                                   (ground.player_pos[0] + 1, ground.player_pos[1] - 1),
                                                                   (ground.player_pos[0], ground.player_pos[1] - 1),
                                                                   (player_pos[0], player_pos[1])]:
                        can_be_use_to_spawn.append((i, g))
            c1 = choice(can_be_use_to_spawn)
            del can_be_use_to_spawn[can_be_use_to_spawn.index(c1)]
            c2 = choice(can_be_use_to_spawn)
            del can_be_use_to_spawn[can_be_use_to_spawn.index(c2)]
            c3 = choice(can_be_use_to_spawn)
            can_be_use_to_spawn = c1, c2, c3
            ground.add_object(
                BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * can_be_use_to_spawn[0][0],
                                    ground.board.cell_size * can_be_use_to_spawn[0][1],
                                    (ground.board.cell_size, ground.board.cell_size)), can_be_use_to_spawn[0])
            turn.add_object(ground, can_be_use_to_spawn[0])
            ground.add_object(
                BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * can_be_use_to_spawn[1][0],
                                    ground.board.cell_size * can_be_use_to_spawn[1][1],
                                    (ground.board.cell_size, ground.board.cell_size)), can_be_use_to_spawn[1])
            turn.add_object(ground, can_be_use_to_spawn[1])
            ground.add_object(
                BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * can_be_use_to_spawn[2][0],
                                    ground.board.cell_size * can_be_use_to_spawn[2][1],
                                    (ground.board.cell_size, ground.board.cell_size)), can_be_use_to_spawn[2])
            turn.add_object(ground, can_be_use_to_spawn[2])
    turn.re_turn()

# def dead_screen(screen, size):
