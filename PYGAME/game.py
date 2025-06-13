import pygame
import os
import random
from constants import W, H, FPS, INIT_DELAY, DECREASE_BASE, GROUND_H
from utils import load_high_score, save_high_score
from entities import Player, Goomba

def load_images():
    images = {}
    IMAGE_DIR = 'images'
    try:
        images['background'] = pygame.image.load(os.path.join(IMAGE_DIR, 'background.jpg'))
        images['background'] = pygame.transform.scale(images['background'], (W, H))

        images['ground'] = pygame.image.load(os.path.join(IMAGE_DIR, 'ground.png'))
        images['ground'] = pygame.transform.scale(images['ground'], (1000, 110))

        # Удалены enemy_flipped и enemy_dead_flipped
        images['enemy'] = pygame.image.load(os.path.join(IMAGE_DIR, 'goomba.png'))
        images['enemy'] = pygame.transform.scale(images['enemy'], (80, 80))
        
        images['enemy_dead'] = pygame.image.load(os.path.join(IMAGE_DIR, 'goomba_dead.png'))
        images['enemy_dead'] = pygame.transform.scale(images['enemy_dead'], (80, 80))

        # Удален player_flipped
        images['player'] = pygame.image.load(os.path.join(IMAGE_DIR, 'cat.png'))
        images['player'] = pygame.transform.scale(images['player'], (80, 80))
    except Exception as e:
        print(f"Ошибка загрузки изображений: {e}")
        pygame.quit()
        exit()
    return images

def load_sounds():
    sounds = {}
    MUSIC_DIR = 'music'
    try:
        sounds['jump'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'jump.mp3'))
        sounds['powerup'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'powerup.mp3'))
        sounds['death'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'death.mp3'))
        sounds['enemy_death'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'enemy_death.mp3'))
        sounds['fast_wave'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'fast_wave.mp3'))
        
        sounds['jump'].set_volume(0.5)
        sounds['powerup'].set_volume(0.7)
        sounds['death'].set_volume(0.7)
        sounds['enemy_death'].set_volume(0.5)
        sounds['fast_wave'].set_volume(0.7)
        
        pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'Factory.ogg'))
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"Ошибка загрузки звуков: {e}")
    return sounds

def load_fonts():
    fonts = {}
    IMAGE_DIR = 'images'
    try:
        font_path = os.path.join(IMAGE_DIR, 'mario_font.ttf')
        fonts['large'] = pygame.font.Font(font_path, 48)
        fonts['small'] = pygame.font.Font(font_path, 24)
        fonts['medium'] = pygame.font.Font(font_path, 36)
    except:
        fonts['large'] = pygame.font.SysFont('arial', 48)
        fonts['small'] = pygame.font.SysFont('arial', 24)
        fonts['medium'] = pygame.font.SysFont('arial', 36)
    return fonts

def run_game():
    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    
    # Загрузка ресурсов
    images = load_images()
    sounds = load_sounds()
    fonts = load_fonts()

    # Инициализация текстов
    retry_text = fonts['small'].render('PRESS ANY KEY', True, (255,255,255))
    retry_rect = retry_text.get_rect()
    retry_rect.midtop = (W//2, H//2)

    pause_text = fonts['large'].render('PAUSED', True, (255, 255, 255))
    pause_rect = pause_text.get_rect()
    pause_rect.center = (W//2, H//2)

    super_text = fonts['small'].render('MOON JUMP READY', True, (173, 216, 230))
    super_rect = super_text.get_rect()
    super_rect.topright = (W - 10, 10)

    # Подсказки управления
    controls_text1 = fonts['small'].render('A/D - Move', True, (255, 255, 255))
    controls_text2 = fonts['small'].render('W - Jump', True, (255, 255, 255))
    controls_text3 = fonts['small'].render('X - Moon Jump', True, (173, 216, 230))
    controls_text4 = fonts['small'].render('ESC - Pause', True, (255, 255, 255))

    # Фон для подсказок
    controls_bg = pygame.Surface((200, 100))
    controls_bg.set_alpha(150)
    controls_bg.fill((0, 0, 0))
    controls_rect = controls_bg.get_rect(bottomright=(W - 10, H - 10))
    controls_positions = [
        (controls_rect.left + 10, controls_rect.top + 10),
        (controls_rect.left + 10, controls_rect.top + 35),
        (controls_rect.left + 10, controls_rect.top + 60),
        (controls_rect.left + 10, controls_rect.top + 85)
    ]

    # Инициализация игры
    high_score = load_high_score()
    player = Player(images['player'])
    score = 0
    paused = False
    goombas = []
    spawn_delay = INIT_DELAY
    last_spawn_time = pygame.time.get_ticks()

    # Система волн
    fast_spawn_active = False
    fast_spawn_end_time = 0
    fast_spawn_duration = 1000  # 1 секунда быстрого спавна
    kills_for_fast_wave = 20
    kill_count = 5

    wave_spawn_delay = 500
    max_wave_enemies = 2
    # Запуск музыки
    pygame.mixer.music.play(-1)

    # Главный игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 'exit'
            
            if event.type == pygame.KEYDOWN:
                if player.is_out:  # Если игрок умер
                    # Сбрасываем игру
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    
                    # Перезапускаем игру
                    player = Player(images['player'])
                    score = 0
                    kill_count = 0
                    goombas = []
                    spawn_delay = INIT_DELAY
                    last_spawn_time = pygame.time.get_ticks()
                    pygame.mixer.music.play(-1)
                    continue
                
                # Остальная обработка ввода
                if event.key == pygame.K_w:
                    if not paused and player.jump():
                        sounds['jump'].play()
                elif event.key == pygame.K_x and not paused:
                    if player.activate_moon_jump():
                        sounds['powerup'].play()
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        clock.tick(FPS)

        # Проверяем, нужно ли активировать быстрый спавн
        if kill_count >= kills_for_fast_wave and not fast_spawn_active:
            fast_spawn_active = True
            kill_count = 0
            fast_spawn_end_time = pygame.time.get_ticks() + fast_spawn_duration
            if 'fast_wave' in sounds:
                sounds['fast_wave'].play()

        # Проверяем, закончился ли период быстрого спавна
        if fast_spawn_active and pygame.time.get_ticks() > fast_spawn_end_time:
            fast_spawn_active = False

        # Логика спавна врагов
        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time
        
        # Определяем интервал спавна в зависимости от режима
        current_spawn_delay = wave_spawn_delay if fast_spawn_active else spawn_delay
        
        if elapsed > current_spawn_delay:
            last_spawn_time = now
            goombas.append(Goomba(images['enemy'], images['enemy_dead']))
            
            # В быстром режиме спавним дополнительных гумб с меньшей вероятностью
            if fast_spawn_active and random.random() > 0.8: 
                extra_enemies = random.randint(0, max_wave_enemies)  # От 0 до max_wave_enemies
                for _ in range(extra_enemies):
                    goombas.append(Goomba(images['enemy'], images['enemy_dead']))

        # Отрисовка
        screen.blit(images['background'], (0, 0))
        screen.blit(images['ground'], (0, H-GROUND_H))

        score_text = fonts['large'].render(str(score), True, (255,255,255))
        score_rect = score_text.get_rect()
        
        high_score_text = fonts['medium'].render(f'RECORD: {high_score}', True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.topleft = (10, 10)

        # Логика спавна врагов
        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time
        
        # Определяем интервал спавна в зависимости от режима
        current_spawn_delay = 300 if fast_spawn_active else spawn_delay
        
        if elapsed > current_spawn_delay:
            last_spawn_time = now
            goombas.append(Goomba(images['enemy'], images['enemy_dead']))
            
            # В быстром режиме спавним дополнительных гумб
            if fast_spawn_active and random.random() > 0.5:
                for _ in range(random.randint(1, 2)):
                    goombas.append(Goomba(images['enemy'], images['enemy_dead']))

        if player.is_out:
            score_rect.midbottom = (W//2, H//2)
            screen.blit(retry_text, retry_rect)
            
            final_score_text = fonts['medium'].render(f'YOUR SCORE: {score}', True, (255, 255, 255))
            final_score_rect = final_score_text.get_rect()
            final_score_rect.midbottom = (W//2, H//2 - 40)
            screen.blit(final_score_text, final_score_rect)
            
            record_text = fonts['medium'].render(f'RECORD: {high_score}', True, (255, 215, 0))
            record_rect = record_text.get_rect()
            record_rect.midbottom = (W//2, H//2 - 80)
            screen.blit(record_text, record_rect)
        else:
            if not paused:
                player.update()
                player.update_moon_jump()
                
                for goomba in list(goombas):
                    if goomba.is_out:
                        goombas.remove(goomba)
                    else:
                        goomba.update()

                        if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                            if player.rect.bottom - player.y_speed < goomba.rect.top:
                                if goomba.kill():
                                    sounds['enemy_death'].play()
                                    kill_count += 1
                                    score += 1
                                    spawn_delay = INIT_DELAY / (DECREASE_BASE**score)
                                    if score > high_score:
                                        high_score = score
                                if player.jump():
                                    sounds['jump'].play()
                            else:
                                player.kill(images['player'])
                                sounds['death'].play()
            
            player.draw(screen)
            for goomba in goombas:
                goomba.draw(screen)
            
            if paused:
                screen.blit(pause_text, pause_rect)
            
            if player.moon_jump_ready and not player.is_out:
                screen.blit(super_text, super_rect)
            
            if not player.is_out:
                screen.blit(controls_bg, controls_rect)
                screen.blit(controls_text1, controls_positions[0])
                screen.blit(controls_text2, controls_positions[1])
                screen.blit(controls_text3, controls_positions[2])
                screen.blit(controls_text4, controls_positions[3])
            
            # Отрисовываем индикатор волны
            if fast_spawn_active:
                
                wave_font = fonts['large']
                
                # Создаем текст с обводкой
                wave_text = wave_font.render("WAVE!", True, (255, 0, 0))  # Ярко-красный
                wave_rect = wave_text.get_rect(center=(W//2, 100))  # Фиксированная позиция сверху
                
                # Черная обводка
                outline_surf = wave_font.render("WAVE!", True, (0, 0, 0))
                for dx in [-3, -2, -1, 1, 2, 3]:
                    for dy in [-3, -2, -1, 1, 2, 3]:
                        screen.blit(outline_surf, (wave_rect.x + dx, wave_rect.y + dy))
                
                # Основной текст
                screen.blit(wave_text, wave_rect)
                
                # Дополнительный эффект - полоса под текстом
                pygame.draw.rect(screen, (255, 0, 0), (wave_rect.x - 10, wave_rect.bottom, wave_rect.width + 20, 5))
                        
            screen.blit(high_score_text, high_score_rect)
            score_rect.midtop = (W//2, 5)

        screen.blit(score_text, score_rect)
        pygame.display.flip()

    # Завершение игры
    if score > high_score:
        save_high_score(score)

    pygame.mixer.music.stop()
    return 'exit'