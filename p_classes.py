import pygame


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.left = 70
        self.top = 70
        self.cell_size = 50

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for g in range(self.height):
                pygame.draw.rect(screen, 'white',
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
