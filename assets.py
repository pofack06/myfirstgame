import pygame
import os
from constants import W, H, IMAGE_DIR, MUSIC_DIR, GROUND_H

def load_images():
    images = {}
    
    # Загрузка фона
    background_image = pygame.image.load(os.path.join(IMAGE_DIR, 'background.jpg'))
    images['background'] = pygame.transform.scale(background_image, (W, H))
    
    # Загрузка земли
    ground_image = pygame.image.load(os.path.join(IMAGE_DIR, 'ground.png'))
    images['ground'] = pygame.transform.scale(ground_image, (1000, GROUND_H))
    
    # Загрузка врага (только оригинальные изображения)
    enemy_image = pygame.image.load(os.path.join(IMAGE_DIR, 'goomba.png'))
    images['enemy'] = pygame.transform.scale(enemy_image, (80, 80))
    
    enemy_dead_image = pygame.image.load(os.path.join(IMAGE_DIR, 'goomba_dead.png'))
    images['enemy_dead'] = pygame.transform.scale(enemy_dead_image, (80, 80))
    
    # Загрузка игрока (только оригинальное изображение)
    player_image = pygame.image.load(os.path.join(IMAGE_DIR, 'cat.png'))
    images['player'] = pygame.transform.scale(player_image, (80, 80))
    
    return images

def load_sounds():
    sounds = {}
    
    sounds['jump'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'jump.mp3'))
    sounds['powerup'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'powerup.mp3'))
    sounds['death'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'death.mp3'))
    sounds['enemy_death'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'enemy_death.mp3'))
    
    sounds['jump'].set_volume(0.5)
    sounds['powerup'].set_volume(0.7)
    sounds['death'].set_volume(0.7)
    sounds['enemy_death'].set_volume(0.5)
    
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'Factory.ogg'))
    pygame.mixer.music.set_volume(0.5)
    
    return sounds

def load_fonts():
    fonts = {}
    font_path = os.path.join(IMAGE_DIR, 'mario_font.ttf')
    fonts['large'] = pygame.font.Font(font_path, 48)
    fonts['medium'] = pygame.font.Font(font_path, 36)
    fonts['small'] = pygame.font.Font(font_path, 24)
    return fonts