import pygame
import math

WIDTH = 800
HEIGHT = 800

CANVAS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm!")

RED = (255, 0 ,0)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255 ,0)
WHITE = (255, 255 ,255)
BLACK = (0, 0 ,0)
PURPLE = (128, 0 ,128)
ORANGE = (255, 165 ,0)
GREY = (128, 128 ,128)
TURQUOISE = (64, 224 ,208)

class Cell:
    def __init__(self, row, column, width, height, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * height
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.height = height
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.column

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
   
    def is_open(self):
        return self.color == GREEN
   
    def is_start(self):
        return self.color == BLUE
    
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color == WHITE


    def make_closed(self):
        self.color == RED

    def make_open(self):
        self.color == GREEN

    def make_barrier(self):
        self.color == BLACK
   
    def make_open(self):
        self.color == GREEN
   
    def make_start(self):
        self.color == BLUE
    
    def make_end(self):
        self.color == PURPLE