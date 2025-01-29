import pygame
import os
import sys
from random import choice


class Board:
    def __init__(self, width: int, height: int, left: int, top: int, cell_size: int):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.board = [[pygame.Color(0, 0, 0, 0)] * width for _ in range(height)]
        self.rect_color = pygame.Color('white')

    def set_view(self, left: int, top: int, cell_size: int):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def change_all_rect_color(self, color: str | tuple, hsva=False, string=False):
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
        if hsva:
            self.rect_color.hsva = color
        elif string:
            self.rect_color = pygame.Color(color)
        else:
            self.rect_color = pygame.Color(*color)

    def render(self, screen):
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

    def get_click(self, mouse_pos):
        mouse_pos = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)
        if mouse_pos[0] < 0 or mouse_pos[1] < 0:
            return None
        if mouse_pos[0] >= self.width or mouse_pos[1] >= self.height:
            return None
        return mouse_pos[0], mouse_pos[1]


def load_image(name, colorkey=None):
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


class SpritePictures:
    def __init__(self, *args, **kwargs):
        self.puctures = {}
        for i in kwargs:
            if isinstance(kwargs[i], str):
                self.puctures[i] = load_image(kwargs[i])
            else:
                self.puctures[i] = load_image(kwargs[i][0], kwargs[i][1])

    def __getitem__(self, item: int | str):
        if isinstance(item, str):
            return self.puctures[item]
        return self.puctures[list(self.puctures)[item]]

    def __reversed__(self, reverse=0):
        if reverse:
            for i in self.puctures:
                if reverse == 1:
                    self.puctures[i] = pygame.transform.flip(self.puctures[i], 1, 0)
                elif reverse == 2:
                    self.puctures[i] = pygame.transform.flip(self.puctures[i], 0, 1)
                elif reverse == 3:
                    self.puctures[i] = pygame.transform.flip(self.puctures[i], 1, 1)


class AbstractSpriteClass(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, pictures: SpritePictures):
        super().__init__(group)
        self.pictures = pictures
        self.image = self.pictures[0]
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_rect(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update_picture(self, update_picture_name: str | int):
        self.image = self.pictures[update_picture_name]

    def rotate(self, rotation=0):
        self.image = pygame.transform.rotate(self.image, rotation)

    def flip(self, flip_horizontal=False, flip_vertical=False):
        self.image = pygame.transform.flip(self.image, flip_horizontal, flip_vertical)

    def scale(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))


class NormalSprite(AbstractSpriteClass):

    def __init__(self, group: pygame.sprite.Group, x: int, y: int, pictures: SpritePictures,
                 scaling: (int, int)):
        super().__init__(group, x, y, pictures)
        self.group = group
        self.scaling = scaling
        self.scale(scaling[0], scaling[1])

    def clone(self):
        return NormalSprite(self.group, self.rect.x, self.rect.y, self.pictures, self.scaling)

    def scale(self, x, y):
        self.scaling = (x, y)
        self.image = pygame.transform.scale(self.image, (x, y))

    def update_picture(self, update_picture_name: str | int):
        self.image = self.pictures[update_picture_name]
        self.image = pygame.transform.scale(self.image, self.scaling)


class PlayerSprite(NormalSprite):
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('Doge_Passive_0.png', 'white'),
                                                     p1=('Doge_Passive_1.png', 'white'),
                                                     p2=('Doge_Passive_0.png', 'white'),
                                                     p3=('Doge_Passive_1.png', 'white')),
                         scaling)
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

    def change_animation(self, passive=False, run=False, reverse=0):
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
        self.pictures.__reversed__(reverse)


class BulletMonsterSprite(NormalSprite):
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('BulletMonster_Normal_0.png', 'white'),
                                                     p1=('BulletMonster_Normal_1.png', 'white'),
                                                     p2=('BulletMonster_Normal_2.png', 'white'),
                                                     p3=('BulletMonster_Normal_3.png', 'white')),
                         scaling)
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


class BulletSprite(NormalSprite):
    def __init__(self, group: pygame.sprite.Group, x: int, y: int, scaling: (int, int)):
        super().__init__(group, x, y, SpritePictures(p0=('Bullet_Sprite_0.png', 'white'),
                                                     p1=('Bullet_Sprite_1.png', 'white'),
                                                     p2=('Bullet_Sprite_2.png', 'white'),
                                                     p3=('Bullet_Sprite_3.png', 'white')),
                         scaling)
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


class HealphBar:
    def __init__(self, group, points: int, cell_size: int):
        self.healph_bar_board = Board(points, 1, 0, 0, cell_size)
        health = NormalSprite(group,
                              -100, -100,
                              SpritePictures(n1='valentine_heart.png',
                                             n2='valentine_broken_heart.png'), (cell_size - 3, cell_size - 3))
        self.health = [health.clone() for _ in range(points)]
        self.zdravie = 6
        for i in range(points):
            self.health[i].update_rect((i * cell_size) + 1, 1)
        del health

    def __isub__(self, other: int):
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

    def __iadd__(self, other: int):
        if self.zdravie > len(self.health):
            self.zdravie += 1
        if self.zdravie < len(self.health):
            self.health[self.zdravie].update_picture(0)
            self.health[self.zdravie].scale(self.healph_bar_board.cell_size - 3,
                                            self.healph_bar_board.cell_size - 3)
        print('Собакен выздоравливается!')
        return self

    def is_dead_or_alive(self):
        if self.zdravie <= 0:
            return False
        return True


class Ground:
    def __init__(self, screen, width, heigth, cell_size):
        self.screen = screen
        self.board = Board(width, heigth, 0, 0, cell_size)
        self.tiles = [[None] * ((width // cell_size) + 1) for _ in range(heigth // cell_size + 1)]
        self.objects = [[None] * ((width // cell_size) + 6) for _ in range(heigth // cell_size + 6)]
        self.sprites = pygame.sprite.Group()
        self.objects_sprites = pygame.sprite.Group()
        self.player_pos = None

    def deep_init(self, player_pos: (int, int)):
        self.player_pos = player_pos
        self.add_object(PlayerSprite(self.objects_sprites, self.board.cell_size * player_pos[0],
                                     self.board.cell_size * player_pos[1],
                                     (self.board.cell_size, self.board.cell_size)),
                        (player_pos[0], player_pos[1]))
        for i in range(len(self.tiles[0])):
            for g in range(len(self.tiles)):
                self.assign_sprite(SpritePictures(n1=choice(['Grass-300x300.jpg'])), (i, g))

    def render(self):
        self.board.render(self.screen)
        self.sprites.draw(self.screen)
        self.objects[self.player_pos[0]][self.player_pos[1]].cicle_animation()
        self.objects_sprites.draw(self.screen)

    def get_click(self, mouse_pos):
        mouse_position = self.board.get_click(mouse_pos)
        object_in_position = self.objects[mouse_position[0]][mouse_position[1]]
        print(mouse_position, object_in_position)
        return mouse_position, object_in_position

    def add_object(self, objject: NormalSprite | None, pos: (int, int)):
        self.objects[pos[0]][pos[1]] = objject

    def assign_sprite(self, pictures: SpritePictures, pos: (int, int), offset=(0, 0)):
        self.tiles[pos[0]][pos[1]] = NormalSprite(self.sprites,
                                                  (pos[0] * self.board.cell_size) + offset[0],
                                                  (pos[1] * self.board.cell_size) + offset[1],
                                                  pictures,
                                                  (self.board.cell_size, self.board.cell_size))

    def move_object(self, pos_start: (int, int), pos_end: (int, int), tipe=None):
        if not tipe:
            if self.objects[pos_start[0]][pos_start[1]]:
                if not self.objects[pos_end[0]][pos_end[1]]:
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
        if isinstance(tipe, PlayerSprite):
            if pos_end[0] < 0:
                if not self.objects[(len(self.board.board[0]) // self.board.cell_size)][self.player_pos[1]]:
                    pos_end = ((len(self.board.board[0]) // self.board.cell_size), self.player_pos[1])
                    self.player_pos = ((len(self.board.board[0]) // self.board.cell_size), self.player_pos[1])
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif pos_end[0] > len(self.board.board[0]) // self.board.cell_size:
                if not self.objects[0][self.player_pos[1]]:
                    pos_end = (0, self.player_pos[1])
                    self.player_pos = (0, self.player_pos[1])
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif pos_end[1] < 0:
                if not self.objects[pos_end[0]][(len(self.board.board[1]) // self.board.cell_size)]:
                    pos_end = (self.player_pos[0], (len(self.board.board[1]) // self.board.cell_size))
                    self.player_pos = (self.player_pos[0], (len(self.board.board[1]) // self.board.cell_size))
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif pos_end[1] > len(self.board.board[1]) // self.board.cell_size:
                if not self.objects[pos_end[0]][0]:
                    pos_end = (self.player_pos[0], 0)
                    self.player_pos = (self.player_pos[0], 0)
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
            elif not self.objects[pos_end[0]][pos_end[1]]:
                if not self.objects[pos_end[0]][pos_end[1]]:
                    self.player_pos = pos_end
                    self.objects[pos_start[0]][pos_start[1]].update_rect(pos_end[0] * self.board.cell_size,
                                                                         pos_end[1] * self.board.cell_size)
                    self.objects[pos_start[0]][pos_start[1]], self.objects[pos_end[0]][pos_end[1]] = None, \
                        self.objects[pos_start[0]][pos_start[1]]
                print(self.player_pos)


class Turns:
    def __init__(self):
        self.turn = False

    def deep_init(self, ground, *args: (int, int)):
        self.bodies = []
        for i in args:
            self.bodies.append([ground.objects[i[0]][i[1]], i])

    def add_object(self, ground, pos: (int, int)):
        if ground.objects[pos[0]][pos[1]]:
            self.bodies.append([ground.objects[pos[0]][pos[1]], pos])

    def __bool__(self):
        return self.turn

    def re_turn(self):
        self.turn = True if not self.turn else False

    def intellectual_move(self):
        pass

    def __getitem__(self, item):
        return self.bodies[item]
