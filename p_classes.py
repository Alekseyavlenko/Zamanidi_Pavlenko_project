import pygame
import os
import sys
from random import choice


class Board:  # класс доски
    def __init__(self, width: int, height: int, left: int, top: int, cell_size: int):  # инициализация доски
        self.width = width  # ширина
        self.height = height  # высота
        self.left = left  # смещение вправо
        self.top = top  # смещение вниз
        self.cell_size = cell_size  # размер одного деления в пикселях
        self.board = [[pygame.Color(0, 0, 0, 0)] * width for _ in
                      range(height)]  # цвет заливки квадрата
        self.rect_color = pygame.Color('white')  # цвет границ квадрата

    def set_view(self, left: int, top: int, cell_size: int):
        self.left = left  # новое смещение вправо
        self.top = top  # новое смещение вниз
        self.cell_size = cell_size  # новый размер одного деления в пикселях

    def change_all_rect_color(self, color: str | tuple, hsva=False, string=False):
        # смена цвета заливки для всех квадратов
        if hsva:
            color_o = pygame.Color(0, 0, 0)
            color_o.hsva = color
            self.board = [[color_o] * self.width for _ in range(self.height)]
        elif string:
            color = pygame.Color(color)
            self.board = [[color] * self.width for _ in range(self.height)]
        else:
            color = pygame.Color(*color)
            self.board = [[color] * self.width for _ in range(self.height)]

    def change_one_rect_color(self, rect: [int, int], color: str | tuple, hsva=False, string=False):
        # смена цвета заливки для одного квадрата
        if hsva:
            color_o = pygame.Color(0, 0, 0)
            color_o.hsva = color
            self.board[rect[0]][rect[1]] = color_o
        elif string:
            color = pygame.Color(color)
            self.board[rect[0]][rect[1]] = color
        else:
            color = pygame.Color(*color)
            self.board[rect[0]][rect[1]] = color

    def change_frame_color(self, color: str | tuple, hsva=False, string=False):
        # смена цвета границ всех квадратов
        if hsva:
            self.rect_color.hsva = color
        elif string:
            self.rect_color = pygame.Color(color)
        else:
            self.rect_color = pygame.Color(*color)

    def render(self, screen):  # отрисовывание доски
        for i in range(self.width):
            for g in range(self.height):
                pygame.draw.rect(screen, self.board[g][i],
                                 (i * self.cell_size + self.left,
                                  g * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 0)
                pygame.draw.rect(screen, self.rect_color,
                                 (i * self.cell_size + self.left,
                                  g * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def get_click(self, mouse_pos):  # получение координат клика на доске
        mouse_pos = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)
        if mouse_pos[0] < 0 or mouse_pos[1] < 0:
            return None
        if mouse_pos[0] >= self.width or mouse_pos[1] >= self.height:
            return None
        return mouse_pos[0], mouse_pos[1]


def load_image(name, colorkey=None):  # функция загрузки изображения (из урока)
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    loading_image = pygame.image.load(fullname)
    if colorkey is not None:
        loading_image = loading_image.convert()
        if colorkey == -1:
            colorkey = loading_image.get_at((0, 0))
        loading_image.set_colorkey(colorkey)
    else:
        loading_image = loading_image.convert_alpha()
    return loading_image


class SpritePictures:  # класс спрайта
    def __init__(self, *args, **kwargs):
        self.puctures = {}
        for i in kwargs:  # каждый спрайт - отдельная картинка (это стоит не забывать!!!)
            if isinstance(kwargs[i], str):
                self.puctures[i] = load_image(kwargs[i])
            else:
                self.puctures[i] = load_image(kwargs[i][0], kwargs[i][1])

    def __getitem__(self, item: int | str):  # можно получить спрайт как именем, так и ключом
        if isinstance(item, str):
            return self.puctures[item]
        return self.puctures[list(self.puctures)[item]]

    def __reversed__(self, reverse=0):  # функция переворачивает изображения (все)
        if reverse:
            for i in self.puctures:
                if reverse == 1:  # 1 - переворот (горизонт)
                    self.puctures[i] = pygame.transform.flip(self.puctures[i], 1, 0)
                elif reverse == 2:  # 2 - переворот (вертикаль)
                    self.puctures[i] = pygame.transform.flip(self.puctures[i], 0, 1)
                elif reverse == 3:  # 3 - переворот (горизонт и вертикаль)
                    self.puctures[i] = pygame.transform.flip(self.puctures[i], 1, 1)


class AbstractSpriteClass(pygame.sprite.Sprite):  # от него будут отходить все остальные ветви спрайтов (объектов)
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, pictures: SpritePictures):
        super().__init__(group)
        self.pictures = pictures  # изображения спрайта
        self.image = self.pictures[0]  # титульное изображение спрайта
        self.rect = self.image.get_rect()  # положение в пространстве
        self.rect.x = x
        self.rect.y = y

    def update_rect(self, x, y):  # новое положение в пространстве
        self.rect.x, self.rect.y = x, y

    def update_picture(self, update_picture_name: str | int):  # смена одной картинки на другую
        self.image = self.pictures[update_picture_name]

    def rotate(self, rotation=0):  # поворот изображения
        self.image = pygame.transform.rotate(self.image, rotation)

    def flip(self, flip_horizontal=False, flip_vertical=False):  # переворот изображения
        self.image = pygame.transform.flip(self.image, flip_horizontal, flip_vertical)

    def scale(self, x, y):  # уменьшение или увеличение изображения
        self.image = pygame.transform.scale(self.image, (x, y))


class NormalSprite(AbstractSpriteClass):  # от него будут отходить игрок, монстры, предметы
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, pictures: SpritePictures,
                 scaling: (int, int)):
        super().__init__(group, x, y, pictures)
        self.group = group  # группа спрайтов (из pygame)
        self.scaling = scaling  # размеры спрайта
        self.scale(scaling[0], scaling[1])

    def clone(self):  # от этого спрайта можно получить ровно такой же
        return NormalSprite(self.group, self.rect.x, self.rect.y, self.pictures, self.scaling)

    def scale(self, x, y):  # уменьшение или увеличение изображения
        self.scaling = (x, y)
        self.image = pygame.transform.scale(self.image, (x, y))

    def update_picture(self, update_picture_name: str | int):  # смена изображений
        self.image = self.pictures[update_picture_name]
        self.image = pygame.transform.scale(self.image, self.scaling)


class Heal(NormalSprite):
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('Flag_of_the_Red_Cross_0.png', -1),
                                                     p1=('Flag_of_the_Red_Cross_1.png', -1),
                                                     p2=('Flag_of_the_Red_Cross_0.png', -1),
                                                     p3=('Flag_of_the_Red_Cross_1.png', -1)),
                         scaling)
        self.reversing = False
        self.cicl = 0

    def cicle_animation(self):
        if not self.cicl:
            self.cicl = 1
            self.update_picture('p1')
        elif self.cicl == 1:
            self.cicl = 2
            self.update_picture('p2')
        elif self.cicl == 2:
            self.cicl = 3
            self.update_picture('p3')
        elif self.cicl == 3:
            self.cicl = 0
            self.update_picture('p0')


class Jaw(NormalSprite):
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('chelust.jpg', -1),
                                                     p1=('chelust_pobolshe.jpg', -1),
                                                     p2=('chelust.jpg', -1),
                                                     p3=('chelust_pobolshe.jpg', -1)),
                         scaling)
        self.reversing = False
        self.cicl = 0

    def cicle_animation(self):
        if not self.cicl:
            self.cicl = 1
            self.update_picture('p1')
        elif self.cicl == 1:
            self.cicl = 2
            self.update_picture('p2')
        elif self.cicl == 2:
            self.cicl = 3
            self.update_picture('p3')
        elif self.cicl == 3:
            self.cicl = 0
            self.update_picture('p0')


class PlayerSprite(NormalSprite):  # класс игрока
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('Doge_Passive_0.png', 'white'),
                                                     p1=('Doge_Passive_1.png', 'white'),
                                                     p2=('Doge_Passive_0.png', 'white'),
                                                     p3=('Doge_Passive_1.png', 'white')),
                         scaling)
        self.reversing = 0
        self.cicl = 0

    def cicle_animation(self):  # функция запускается в каждом тике игры (то есть это - анимация)
        if not self.cicl:
            self.cicl = 1
            self.update_picture('p1')
        elif self.cicl == 1:
            self.cicl = 2
            self.update_picture('p2')
        elif self.cicl == 2:
            self.cicl = 3
            self.update_picture('p3')
        elif self.cicl == 3:
            self.cicl = 0
            self.update_picture('p0')

    def change_animation(self, passive=False, run=False, loot=False, fight=False,
                         reverse=0):  # смена анимации (на заготовки)
        self.reversing = reverse
        if passive:
            self.pictures = SpritePictures(p0=('Doge_Passive_0.png', 'white'),
                                           p1=('Doge_Passive_1.png', 'white'),
                                           p2=('Doge_Passive_0.png', 'white'),
                                           p3=('Doge_Passive_1.png', 'white'))
        elif run:
            self.pictures = SpritePictures(p0=('Doge_Walk_1.png', 'white'),
                                           p1=('Doge_Walk_0.png', 'white'),
                                           p2=('Doge_Walk_1.png', 'white'),
                                           p3=('Doge_Walk_0.png', 'white'))
        elif loot:
            self.pictures = SpritePictures(p0=('buhank_doge.jpeg', -1),
                                           p1=('rebuhank_doge.jpg', -1),
                                           p2=('buhank_doge.jpeg', -1),
                                           p3=('rebuhank_doge.jpg', -1))
        elif fight:
            self.pictures = SpritePictures(p0=('Doge_Fight_0.png', 'white'),
                                           p1=('Doge_Fight_1.png', 'white'),
                                           p2=('Doge_Fight_2.png', 'white'),
                                           p3=('Doge_Fight_3.png', 'white'))
        self.pictures.__reversed__(self.reversing)


class BulletMonsterSprite(NormalSprite):  # класс рядового противника
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('BulletMonster_Normal_0.png', 'white'),
                                                     p1=('BulletMonster_Normal_1.png', 'white'),
                                                     p2=('BulletMonster_Normal_2.png', 'white'),
                                                     p3=('BulletMonster_Normal_3.png', 'white')),
                         scaling)
        self.cicl = 0

    def cicle_animation(self):  # анимация
        if not self.cicl:
            self.cicl = 1
            self.update_picture('p1')
        elif self.cicl == 1:
            self.cicl = 2
            self.update_picture('p2')
        elif self.cicl == 2:
            self.cicl = 3
            self.update_picture('p3')
        elif self.cicl == 3:
            self.cicl = 0
            self.update_picture('p0')


class BulletSprite(NormalSprite):  # класс призывателя рядовых противников
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('Bullet_Sprite_0.png', 'white'),
                                                     p1=('Bullet_Sprite_1.png', 'white'),
                                                     p2=('Bullet_Sprite_2.png', 'white'),
                                                     p3=('Bullet_Sprite_3.png', 'white')),
                         scaling)
        self.cicl = 0

    def cicle_animation(self):  # анимация
        if not self.cicl:
            self.cicl = 1
            self.update_picture('p1')
        elif self.cicl == 1:
            self.cicl = 2
            self.update_picture('p2')
        elif self.cicl == 2:
            self.cicl = 3
            self.update_picture('p3')
        elif self.cicl == 3:
            self.cicl = 0
            self.update_picture('p0')


class HealphBar:  # полоска здоровья
    def __init__(self, group, points: int, cell_size: int):
        self.healph_bar_board = Board(points, 1, 0, 0, cell_size)
        health = NormalSprite(group,
                              -100, -100,
                              SpritePictures(n1='valentine_heart.png',
                                             n2='valentine_broken_heart.png'), (cell_size - 3, cell_size - 3))
        self.health = [health.clone() for _ in range(points)]  # извините, костыль
        self.zdravie = points
        for i in range(points):
            self.health[i].update_rect((i * cell_size) + 1, 1)
        del health

    def __isub__(self, other: int):  # получение урона (по задумке, сосуд жизни всегда теряет одно сердечко)
        self.zdravie -= 1
        if self.zdravie < len(self.health):
            self.health[self.zdravie].update_picture(1)
            self.health[self.zdravie].scale(self.healph_bar_board.cell_size - 3,
                                            self.healph_bar_board.cell_size - 3)
        else:
            self.zdravie = 5
            self.health[self.zdravie].update_picture(1)
            self.health[self.zdravie].scale(self.healph_bar_board.cell_size - 3,
                                            self.healph_bar_board.cell_size - 3)
        print('Собакену дырявят ХП!')
        return self

    def __iadd__(self, other: int):  # лечение (по задумке, всегда на одно сердце)
        if self.zdravie > len(self.health):
            self.zdravie += 1
        if self.zdravie < len(self.health):
            self.health[self.zdravie].update_picture(0)
            self.health[self.zdravie].scale(self.healph_bar_board.cell_size - 3,
                                            self.healph_bar_board.cell_size - 3)
        print('Собакен выздоравливается!')
        return self

    def is_dead_or_alive(self):  # проверка на умерщвлённость
        if self.zdravie <= 0:
            return False
        return True


class JawsBar:
    def __init__(self, group, points: int, cell_size: int, end_coords: int):
        self.jaws_bar_board = Board(points, 1, 0, 0, cell_size)
        jaw = NormalSprite(group,
                           -100, -100,
                           SpritePictures(n1=('chelust.jpg', -1), n2=('Без имени.png', -1)),
                           (cell_size - 3, cell_size - 3))
        self.jjaws = [jaw.clone() for _ in range(points)]  # извините, костыль
        self.kus = points
        for i in range(points):
            self.jjaws[i].update_rect(end_coords - (i * cell_size) - cell_size, 1)
        del jaw

    def __iadd__(self, other: int):  # добавление нового ряда зубов
        print('собакен находит ряд новых зубов')
        if self.kus > len(self.jjaws):
            self.kus += 1
        if self.kus < len(self.jjaws):
            self.jjaws[self.kus].update_picture(0)
            self.jjaws[self.kus].scale(self.jaws_bar_board.cell_size - 3,
                                       self.jaws_bar_board.cell_size - 3)
        return self

    def __isub__(self, other: int):  # нанесение урона врагам (по задумке, расходует одну штуку)
        self.kus -= 1
        if self.kus < len(self.jjaws):
            self.jjaws[self.kus].update_picture(1)
            self.jjaws[self.kus].scale(self.jaws_bar_board.cell_size - 3,
                                       self.jaws_bar_board.cell_size - 3)
        else:
            self.kus = 2
            self.jjaws[self.kus].update_picture(1)
            self.jjaws[self.kus].scale(self.jaws_bar_board.cell_size - 3,
                                       self.jaws_bar_board.cell_size - 3)
        return self

    def is_exists_or_not_exists(self):  # проверка на умерщвлённость
        if self.kus <= 0:
            return False
        return True


class Ground:  # класс поля всех действ
    def __init__(self, screen, width, heigth, cell_size):  # сотворение мира
        self.screen = screen  # знание места отображения
        self.board = Board(width, heigth, 0, 0, cell_size)  # для хранения всяких чисел важных и необходимых
        self.tiles = [[None] * ((width // cell_size) + 1) for _ in range(heigth // cell_size + 1)]  # скины квадратиков
        self.objects = [[None] * ((width // cell_size) + 6) for _ in range(heigth // cell_size + 6)]  # спрайты
        self.sprites = pygame.sprite.Group()  # группа спрайтов для скинов дракватиков
        self.objects_sprites = pygame.sprite.Group()  # группа спрайтов для объектов и субъектов
        self.player_pos = None  # заготовка для пришествия на свет машинно-божий великого собакена

    def deep_init(self, player_pos: (int, int)):  # сотворение сути мироздания
        self.player_pos = player_pos  # координаты сего представителя собачьего рода
        self.add_object(PlayerSprite(self.objects_sprites, self.board.cell_size * player_pos[0],
                                     self.board.cell_size * player_pos[1],
                                     (self.board.cell_size, self.board.cell_size)),
                        (player_pos[0], player_pos[1]))
        for i in range(len(self.tiles[0])):
            for g in range(len(self.tiles)):
                self.assign_sprite(SpritePictures(n1=choice(['Grass-300x300.jpg'])), (i, g))  # обувание квадратов

    def render(self):  # отрисование
        self.board.render(self.screen)  # на всякий пожарский доска рисуется
        self.sprites.draw(self.screen)  # на обязательный пожарский кожурки квадратов отображаются
        self.objects[self.player_pos[0]][self.player_pos[1]].cicle_animation()  # собакен в цикле
        self.objects_sprites.draw(self.screen)  # все действа, сущности, тонкости летят в сетчатку глаза

    def get_click(self, mouse_pos):  # курс курсора на позицию мышления мыши
        mouse_position = self.board.get_click(mouse_pos)
        object_in_position = self.objects[mouse_position[0]][mouse_position[1]]
        print(mouse_position, object_in_position)
        return mouse_position, object_in_position

    def add_object(self, objject: NormalSprite | None, pos: (int, int)):  # рождение новой бездушности
        self.objects[pos[0]][pos[1]] = objject

    def assign_sprite(self, pictures: SpritePictures, pos: (int, int), offset=(0, 0)):  # перебувание квадратика
        self.tiles[pos[0]][pos[1]] = NormalSprite(self.sprites,
                                                  (pos[0] * self.board.cell_size) + offset[0],
                                                  (pos[1] * self.board.cell_size) + offset[1],
                                                  pictures,
                                                  (self.board.cell_size, self.board.cell_size))

    def move_object(self, pos_start: (int, int), pos_end: (int, int), tipe=None):  # телепортоперемещение
        if not tipe:  # воздуходувов движение
            if self.objects[pos_start[0]][pos_start[1]]:
                if not self.objects[pos_end[0]][pos_end[1]]:
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
        if isinstance(tipe, PlayerSprite):  # великого собакена физическое размещение
            if pos_end[0] < 0:  # мир бубличен
                if not self.objects[(len(self.board.board[0]) // self.board.cell_size)][self.player_pos[1]]:
                    pos_end = ((len(self.board.board[0]) // self.board.cell_size), self.player_pos[1])
                    self.player_pos = ((len(self.board.board[0]) // self.board.cell_size), self.player_pos[1])
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif pos_end[0] > len(self.board.board[0]) // self.board.cell_size:  # мир бубличен
                if not self.objects[0][self.player_pos[1]]:  # не пойдёт собакен в лапы смерти
                    pos_end = (0, self.player_pos[1])
                    self.player_pos = (0, self.player_pos[1])
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif pos_end[1] < 0:  # мир бубличен
                if not self.objects[pos_end[0]][(len(self.board.board[1]) // self.board.cell_size)]:
                    pos_end = (self.player_pos[0], (len(self.board.board[1]) // self.board.cell_size))
                    self.player_pos = (self.player_pos[0], (len(self.board.board[1]) // self.board.cell_size))
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif pos_end[1] > len(self.board.board[1]) // self.board.cell_size:  # мир бубличен
                if not self.objects[pos_end[0]][0]:  # не пойдёт собакен в лапы смерти
                    pos_end = (self.player_pos[0], 0)
                    self.player_pos = (self.player_pos[0], 0)
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif not self.objects[pos_end[0]][pos_end[1]]:  # мир... мир пластичен
                if not self.objects[pos_end[0]][pos_end[1]]:  # не пойдёт собакен в лапы смерти
                    self.player_pos = pos_end
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
                print(self.player_pos)


class Turns:  # жизнь - игра, но игра по партиям
    def __init__(self):
        self.count = 0.0
        self.turn = True  # собакен не бел, не чист, но ходит первее
        self.bodies = []  # другие не негры, но тьма, и ходят вторее

    def deep_init(self, ground, *args: (int, int)):  # сканированье на всякий погожий иль день черней некуда
        for i in args:
            self.bodies.append([ground.objects[i[0]][i[1]], i])

    def add_object(self, ground, pos: (int, int)):  # добавка надбавки на голову собакевича
        if ground.objects[pos[0]][pos[1]]:
            self.bodies.append((ground.objects[pos[0]][pos[1]], pos))

    def __bool__(self):  # здесь ходят по правде
        self.count += 0.5
        return self.turn

    def re_turn(self):  # не смеет сварожец преступить часов ход
        self.turn = True if not self.turn else False

    def intellectual_move(self):  # чтоб собакам отрадные не походили на глуповцев
        pass

    def jaws_check(self):
        for i in self.bodies:
            if isinstance(i[0], Jaw):
                return True
        return None

    def heal_check(self):
        for i in self.bodies:
            if isinstance(i[0], Heal):
                return True
        return None

    def __getitem__(self, item):  # индекс чтоб старший брат властовал семи
        return self.bodies[item]
