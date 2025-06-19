import pygame
import os
import random
from constants import W, H, FPS, INIT_DELAY, DECREASE_BASE, GROUND_H
from utils import load_high_score, save_high_score
from entities import Player, Goomba, HeartBonus, Meteor

def load_images():
    images = {}
    IMAGE_DIR = 'images'
    
    images['background'] = pygame.image.load(os.path.join(IMAGE_DIR, 'background.jpg'))
    images['background'] = pygame.transform.scale(images['background'], (W, H))

    images['ground'] = pygame.image.load(os.path.join(IMAGE_DIR, 'ground.png'))
    images['ground'] = pygame.transform.scale(images['ground'], (1000, 110))

    images['enemy'] = pygame.image.load(os.path.join(IMAGE_DIR, 'goomba.png'))
    images['enemy'] = pygame.transform.scale(images['enemy'], (80, 80))
        
    images['enemy_dead'] = pygame.image.load(os.path.join(IMAGE_DIR, 'goomba_dead.png'))
    images['enemy_dead'] = pygame.transform.scale(images['enemy_dead'], (80, 80))

    images['player'] = pygame.image.load(os.path.join(IMAGE_DIR, 'cat.png'))
    images['player'] = pygame.transform.scale(images['player'], (80, 80))
        
    images['heart'] = pygame.image.load(os.path.join(IMAGE_DIR, 'heart.png'))
    images['heart'] = pygame.transform.scale(images['heart'], (30, 30))
        
    images['empty_heart'] = pygame.image.load(os.path.join(IMAGE_DIR, 'empty_heart.webp'))
    images['empty_heart'] = pygame.transform.scale(images['empty_heart'], (30, 30))
        
    images['meteor'] = pygame.image.load(os.path.join(IMAGE_DIR, 'meteor.webp'))
    images['meteor'] = pygame.transform.scale(images['meteor'], (80, 80))
    
    return images

def load_sounds():
    sounds = {}
    MUSIC_DIR = 'music'
    
    sounds['jump'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'jump.mp3'))
    sounds['powerup'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'powerup.mp3'))
    sounds['death'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'death.mp3'))
    sounds['enemy_death'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'enemy_death.mp3'))
    sounds['fast_wave'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'fast_wave.mp3'))
    sounds['heart'] = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'heart.mp3'))

    sounds['jump'].set_volume(0.5)
    sounds['powerup'].set_volume(0.7)
    sounds['death'].set_volume(0.7)
    sounds['enemy_death'].set_volume(0.5)
    sounds['fast_wave'].set_volume(0.7)
    sounds['heart'].set_volume(0.5)
        
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'Factory.ogg'))
    pygame.mixer.music.set_volume(0.5)

    return sounds

def load_fonts():
    fonts = {}
    IMAGE_DIR = 'images'
    
    font_path = os.path.join(IMAGE_DIR, 'mario_font.ttf')
    fonts['large'] = pygame.font.Font(font_path, 48)
    fonts['medium'] = pygame.font.Font(font_path, 36)
    fonts['small'] = pygame.font.Font(font_path, 24)
    
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
    lives = 3
    max_lives = 3
    score = 0
    paused = False
    goombas = []
    heart_bonuses = []
    meteors = []  # Список метеоритов
    HEART_DROP_CHANCE = 0.2  # 20% шанс выпадения сердца
    METEOR_SPAWN_CHANCE = 0.35  # 35% шанс появления метеорита во время волны
    METEOR_SPAWN_INTERVAL = 800  # Интервал спавна метеоритов (мс)
    MAX_METEORS = 8  # Максимальное количество метеоритов
    MAX_LIVES = 3  # 30% шанс появления метеорита во время волны
    spawn_delay = INIT_DELAY
    last_spawn_time = pygame.time.get_ticks()
    last_meteor_time = pygame.time.get_ticks()

    # Система волн
    fast_spawn_active = False
    fast_spawn_end_time = 0
    fast_spawn_duration = 5000  # 5 секунд волны
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
                    player = Player(images['player'])  # Создаем нового игрока
                    lives = 3                         # Восстанавливаем жизни
                    score = 0                         # Сбрасываем счет
                    kill_count = 0                    # Обнуляем счетчик убийств
                    goombas = []                      # Очищаем список врагов
                    heart_bonuses = []                # Очищаем бонусы
                    spawn_delay = INIT_DELAY          # Сбрасываем задержку спавна
                    last_spawn_time = pygame.time.get_ticks()  # Обновляем таймер
                    pygame.mixer.music.play(-1)       # Перезапускаем музыку
                    continue    # Пропускаем остальную обработку
                
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
            meteors = []  # Очищаем метеориты после волны

        # Логика спавна врагов
        now = pygame.time.get_ticks()
        elapsed = now - last_spawn_time
        
        current_spawn_delay = wave_spawn_delay if fast_spawn_active else spawn_delay
        
        if elapsed > current_spawn_delay:
            last_spawn_time = now
            goombas.append(Goomba(images['enemy'], images['enemy_dead']))
            
            if fast_spawn_active and random.random() > 0.8: 
                extra_enemies = random.randint(0, max_wave_enemies)
                for _ in range(extra_enemies):
                    goombas.append(Goomba(images['enemy'], images['enemy_dead']))

        # Спавн метеоритов во время волны
        if (fast_spawn_active and 
        now - last_meteor_time > METEOR_SPAWN_INTERVAL and 
        len(meteors) < MAX_METEORS):
            last_meteor_time = now
            if random.random() < METEOR_SPAWN_CHANCE:
                meteors.append(Meteor(images['meteor']))
                # С шансом 20% спавним дополнительный метеорит
                if random.random() < 0.2 and len(meteors) < MAX_METEORS - 1:
                    meteors.append(Meteor(images['meteor']))

        # Отрисовка
        screen.blit(images['background'], (0, 0))
        screen.blit(images['ground'], (0, H-GROUND_H))

        score_text = fonts['large'].render(str(score), True, (255,255,255))
        score_rect = score_text.get_rect()
        
        high_score_text = fonts['medium'].render(f'RECORD: {high_score}', True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.topleft = (10, 10)

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
                
                # Обновление бонусных сердец
                for heart in list(heart_bonuses):
                    heart.update()
                    if heart.is_out:
                        heart_bonuses.remove(heart)
                    elif player.rect.colliderect(heart.rect) and not player.is_dead:
                        if lives < max_lives:
                            lives += 1
                        heart_bonuses.remove(heart)
                        sounds['heart'].play()
                
                # Обновление метеоритов
                for meteor in list(meteors):
                    meteor.update()
                    if meteor.rect.top > H:  # Удаляем если улетел за экран
                        meteors.remove(meteor)
                    elif not player.is_dead and player.rect.colliderect(meteor.rect):
                        if not player.invincible:
                            lives -= 1
                            if lives <= 0:
                                player.kill()
                                sounds['death'].play()
                            else:
                                player.respawn()
                                player.invincible = True
                                player.invincible_timer = pygame.time.get_ticks() + 2000
                        meteors.remove(meteor)
                
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
                                    
                                    # С шансом 20% создаем бонусное сердце
                                    if random.random() < HEART_DROP_CHANCE:
                                        heart_bonuses.append(HeartBonus(
                                            images['heart'], 
                                            goomba.rect.centerx,
                                            goomba.rect.centery
                                        ))
                                    
                                    if player.jump():
                                        sounds['jump'].play()
                            else:
                                if not player.invincible:
                                    lives -= 1
                                    if lives <= 0:
                                        player.kill()
                                        sounds['death'].play()
                                    else:
                                        player.respawn()
                                        player.invincible = True
                                        player.invincible_timer = pygame.time.get_ticks() + 2000
            
            player.draw(screen)
            for goomba in goombas:
                goomba.draw(screen)

            # Отрисовка метеоритов
            for meteor in meteors:
                meteor.draw(screen)
            
            # Отрисовка бонусных сердец
            for heart in heart_bonuses:
                heart.draw(screen)
            
            # Отрисовка жизней (сердечек)
            for i in range(max_lives):
                if i < lives:
                    screen.blit(images['heart'], (10 + i * 35, 50))
                else:
                    screen.blit(images['empty_heart'], (10 + i * 35, 50))
            
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
                wave_text = wave_font.render("WAVE!", True, (255, 0, 0))
                wave_rect = wave_text.get_rect(center=(W//2, 100))
                
                outline_surf = wave_font.render("WAVE!", True, (0, 0, 0))
                for dx in [-3, -2, -1, 1, 2, 3]:
                    for dy in [-3, -2, -1, 1, 2, 3]:
                        screen.blit(outline_surf, (wave_rect.x + dx, wave_rect.y + dy))
                
                screen.blit(wave_text, wave_rect)
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