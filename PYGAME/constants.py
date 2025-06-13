import pygame
import os

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Константы
W = 800
H = 600
FPS = 60
GROUND_H = 90
INIT_DELAY = 2000
DECREASE_BASE = 1.01

# Пути к папкам
IMAGE_DIR = 'images'
MUSIC_DIR = 'music'

# Настройка экрана
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()