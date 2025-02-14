import pygame

import sys

from p_classes import HealphBar, Ground, BulletMonsterSprite, Turns, Jaw, JawsBar, Heal

from p_game_classes import dogge_move, turning, dogge_search, dagge_fight

import menu


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
    health = HealphBar(all_sprites, 6, 21)  # здоровье и оружие
    jaws = JawsBar(all_sprites, 3, 21, 550)

    # поле
    ground = Ground(screen, 500, 500, 50)
    ground.deep_init((5, 5))
    turn = Turns()

    # уровень сложности влияет на положение предметов и врагов
    if harding == 1:
        ground.add_object(
            BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 2, ground.board.cell_size * 2,
                                (ground.board.cell_size, ground.board.cell_size)), (2, 2))
        ground.add_object(Jaw(ground.objects_sprites, ground.board.cell_size * 9, ground.board.cell_size * 1,
                              (ground.board.cell_size, ground.board.cell_size)), (9, 1))
        ground.add_object(Heal(ground.objects_sprites, ground.board.cell_size * 1, ground.board.cell_size * 1,
                               (ground.board.cell_size, ground.board.cell_size)), (1, 1))
        turn.deep_init(ground, (2, 2), (1, 1), (9, 1))
    elif harding == 2:
        ground.add_object(
            BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 2, ground.board.cell_size * 2,
                                (ground.board.cell_size, ground.board.cell_size)), (2, 2))
        ground.add_object(Jaw(ground.objects_sprites, ground.board.cell_size * 9, ground.board.cell_size * 1,
                              (ground.board.cell_size, ground.board.cell_size)), (9, 1))
        ground.add_object(Heal(ground.objects_sprites, ground.board.cell_size * 1, ground.board.cell_size * 1,
                               (ground.board.cell_size, ground.board.cell_size)), (1, 1))
        ground.add_object(
            BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 2, ground.board.cell_size * 8,
                                (ground.board.cell_size, ground.board.cell_size)), (2, 8))
        turn.deep_init(ground, (2, 2), (1, 1), (9, 1), (2, 8))
    elif harding == 3:
        ground.add_object(
            BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 2, ground.board.cell_size * 2,
                                (ground.board.cell_size, ground.board.cell_size)), (2, 2))
        ground.add_object(Jaw(ground.objects_sprites, ground.board.cell_size * 9, ground.board.cell_size * 1,
                              (ground.board.cell_size, ground.board.cell_size)), (9, 1))
        ground.add_object(
            BulletMonsterSprite(ground.objects_sprites, ground.board.cell_size * 2, ground.board.cell_size * 8,
                                (ground.board.cell_size, ground.board.cell_size)), (2, 8))
        turn.deep_init(ground, (2, 2), (9, 1), (2, 8))
    all_sprites.draw(screen)

    # музыка (тоже зависит от сложности)
    if harding == 1 or harding == 2:
        pygame.mixer.music.load('data/James Primate — Threat - Garbage Wastes.mp3')
    elif harding == 3:
        pygame.mixer.music.load('data/Connor (12Lbs) Skidmore  — Sheer Ice Torrent.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_value)

    # цикл
    while running:

        # управление:
        #   стрелочки - ходить
        #   оба ctrl - подбор предметов
        #   оба shift - атаковать
        #   цифры на клавиатуре - изменение громкости

        # обработка событий
        for event in pygame.event.get():  # обработка событий
            if event.type == pygame.QUIT:  # выход
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # координаты клика
                ground.get_click(event.pos)
            if True in pygame.key.get_pressed():
                if turn:
                    # если нужен индекс кнопки
                    # print(pygame.key.get_pressed().index(True))
                    if pygame.key.get_pressed().index(True) in [79, 80, 81, 82]:  # движение персонажа
                        dogge_move(ground)
                        turn.re_turn()
                    if pygame.key.get_pressed().index(True) == 224 or pygame.key.get_pressed().index(True) == 228:
                        dogge_search(ground, turn, jaws, health, harding)  # подбор предметов
                        turn.re_turn()
                    if pygame.key.get_pressed().index(True) == 225 or pygame.key.get_pressed().index(True) == 229:
                        dagge_fight(ground, turn, jaws, health, harding)  # атака по области
                    if pygame.key.get_pressed().index(True) in [39, 30, 31, 32, 33, 34, 35, 36, 37, 38]:
                        music_value = [39, 30, 31, 32, 33, 34, 35, 36, 37, 38].index(
                            pygame.key.get_pressed().index(True)) * 0.1
                        pygame.mixer.music.set_volume(music_value)  # изменение уровня громкости

        # обязательные действия в цикле
        screen.fill('black')
        ground.render()

        # смена спрайтов у объектов
        for i in range(len(turn.bodies)):
            ground.objects[turn.bodies[i][1][0]][turn.bodies[i][1][1]].cicle_animation()

        # ход противников
        if not turn:
            turning(ground, turn, health, harding)

        # отрисовка объектов
        all_sprites.draw(screen)

        # при проигрыше
        if not health.is_dead_or_alive():
            try:
                # переход в начальное меню
                menu.main_menu({'ach_1': True, 'ach_2': True, 'ach_3': True}, "ru")
            except Exception as hhh:
                print('Вы наткнулись на', hhh)
            pygame.quit()
            sys.exit()

        # смена цикла
        pygame.display.flip()
        pygame.time.Clock().tick(200)


if __name__ == '__main__':
    try:
        game_sobstvenno(harding=1, music_value=0.0)
    except Exception as e:
        print('Вы наткнулись на', e)
