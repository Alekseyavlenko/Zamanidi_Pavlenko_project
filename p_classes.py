import pygame
import os
import sys


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


class AbstractSpriteClass(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = load_image("not_founded.png")
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y, need_update_picture=False, update_picture='car2.png', rotation=0, flip_x=False,
               flip_y=False):
        if need_update_picture:
            self.image = load_image(update_picture)
        if flip_x or flip_y:
            self.image = pygame.transform.flip(self.image, flip_x, flip_y)
        if rotation:
            self.image = pygame.transform.rotate(self.image, rotation)
        self.rect.x, self.rect.y = x, y


class SpritePictures:
    def __init__(self, *args, **kwargs):
        self.puctures = {}
        for i in kwargs:
            self.puctures[i] = load_image(kwargs[i])