import pygame
import random
import os  # Добавлено для работы с файлами

pygame.init()
pygame.mixer.init()  # Инициализация микшера для звуков

W = 800
H = 600

screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()


jump_sound = pygame.mixer.Sound('music/jump.mp3')
powerup_sound = pygame.mixer.Sound('music/powerup.mp3')
death_sound = pygame.mixer.Sound('music/death.mp3')
enemy_death_sound = pygame.mixer.Sound('music/enemy_death.mp3')
    
# Установка громкости для звуков
jump_sound.set_volume(0.5)
powerup_sound.set_volume(0.7)
death_sound.set_volume(0.7)
enemy_death_sound.set_volume(0.5)
    
# Фоновая музыка
pygame.mixer.music.load('music/Factory.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Зацикленное воспроизведение


font_path = 'mario_font.ttf'
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)
font_medium = pygame.font.Font(font_path, 36)  # Добавлен средний шрифт для рекорда

game_over = False
retry_text = font_small.render('PRESS ANY KEY', True, (255,255,255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W//2, H//2)

# Текст для паузы
pause_text = font_large.render('PAUSED', True, (255, 255, 255))
pause_rect = pause_text.get_rect()
pause_rect.center = (W//2, H//2)

# Текст для суперспособности
super_text = font_small.render('MOON JUMP READY', True, (173, 216, 230))
super_rect = super_text.get_rect()
super_rect.topright = (W - 10, 10)

# Подсказки управления
controls_text1 = font_small.render('A/D - Move', True, (255, 255, 255))
controls_text2 = font_small.render('W - Jump', True, (255, 255, 255))
controls_text3 = font_small.render('X - Moon Jump', True, (173, 216, 230))
controls_text4 = font_small.render('ESC - Pause', True, (255, 255, 255))

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

# Загрузка фонового изображения
background_image = pygame.image.load('images/background.jpg')
background_image = pygame.transform.scale(background_image, (W, H))

ground_image = pygame.image.load('images/ground.png')
ground_image = pygame.transform.scale(ground_image, (1000, 110))
GROUND_H = ground_image.get_height()

enemy_image = pygame.image.load('images/goomba.png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))

enemy_dead_image = pygame.image.load('images/goomba_dead.png')
enemy_dead_image = pygame.transform.scale(enemy_dead_image, (80, 80))

player_image = pygame.image.load('images/cat.png')
player_image = pygame.transform.scale(player_image, (80, 80))

# Функции для работы с рекордом
def load_high_score():
    if os.path.exists('highscore.dat'):
        with open('highscore.dat', 'r') as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open('highscore.dat', 'w') as file:
        file.write(str(score))

class Entity:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0 
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.jump_speed = -12
        self.gravity = 0.5
        self.is_grounded = False
    
    def handle_input(self):
        pass

    def kill(self, dead_image):
        self.image = dead_image
        self.is_dead = True
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed
        # Воспроизводим звук смерти врага
        enemy_death_sound.play()

    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.is_dead:
            if self.rect.top > H - GROUND_H:
                self.is_out = True

        else:
            self.handle_input()

            if self.rect.bottom > H-GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = H - GROUND_H

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(Entity):
    def __init__(self):
        super().__init__(player_image)
        self.can_jump = True
        # Добавляем параметры для суперспособности
        self.moon_jump_ready = True
        self.moon_jump_active = False
        self.moon_jump_start_time = 0
        self.moon_jump_duration = 2000  # 2 секунды
        self.moon_jump_cooldown = 10000  # 10 секунд
        self.original_jump_speed = self.jump_speed
    
    def handle_input(self):
        self.x_speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed
        elif keys[pygame.K_d]:
            self.x_speed = self.speed
    
    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (W//2, H-GROUND_H)
        # Сброс суперспособности при респавне
        self.moon_jump_ready = True
        self.moon_jump_active = False

    def jump(self):
        if self.is_grounded:
            self.is_grounded = False
            self.y_speed = self.jump_speed
            jump_sound.play()  # Воспроизводим звук прыжка
    
    def activate_moon_jump(self):
        if self.moon_jump_ready and not self.moon_jump_active:
            self.moon_jump_active = True
            self.moon_jump_start_time = pygame.time.get_ticks()
            self.moon_jump_ready = False
            # Увеличиваем высоту прыжка в 1.5 раза
            self.jump_speed = self.original_jump_speed * 1.5
            powerup_sound.play()  # Воспроизводим звук активации способности
    
    def update_moon_jump(self):
        current_time = pygame.time.get_ticks()
        if self.moon_jump_active:
            if current_time - self.moon_jump_start_time > self.moon_jump_duration:
                self.moon_jump_active = False
                self.jump_speed = self.original_jump_speed
        elif not self.moon_jump_ready:
            if current_time - self.moon_jump_start_time > self.moon_jump_cooldown:
                self.moon_jump_ready = True

class Goomba(Entity):
    def __init__(self):
        super().__init__(enemy_image)
        self.spawn()

    def spawn(self):
        direction = random.randint(0,1)
        if direction == 0:
            self.x_speed =self.speed
            self.rect.bottomright = (0, 0)
        else:
            self.x_speed = -self.speed
            self.rect.bottomleft = (W, 0)
    
    def update(self):
        super().update()
        if self.x_speed>0 and self.rect.left > W or self.x_speed < 0 and self.rect.right < 0:
            self.is_out = True

# Загрузка рекорда
high_score = load_high_score()
player = Player()
score = 0
paused = False  # Флаг паузы

goombas = []
INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                if not paused:  # Прыжок только если не пауза
                    player.jump()
            elif e.key == pygame.K_x and not paused:  # Активация суперспособности
                player.activate_moon_jump()
            elif e.key == pygame.K_ESCAPE:  # Обработка паузы по ESC
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()  # Пауза музыки
                else:
                    pygame.mixer.music.unpause()  # Возобновление музыки
            elif e.key and player.is_out:  # Перезапуск игры
                # Сохраняем рекорд перед рестартом
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                score = 0
                spawn_delay = INIT_DELAY
                last_spawn_time = pygame.time.get_ticks()
                player.respawn()
                # Перезапуск фоновой музыки
                pygame.mixer.music.play(-1)

    clock.tick(FPS)

    # Вместо screen.fill() рисуем фоновое изображение
    screen.blit(background_image, (0, 0))
    screen.blit(ground_image, (0, H-GROUND_H))

    score_text = font_large.render(str(score), True, (255,255,255))
    score_rect = score_text.get_rect()
    
    # Текст рекорда
    high_score_text = font_medium.render(f'RECORD: {high_score}', True, (255, 215, 0))  # Золотой цвет
    high_score_rect = high_score_text.get_rect()
    high_score_rect.topleft = (10, 10)

    if player.is_out:
        score_rect.midbottom = (W//2, H//2)
        screen.blit(retry_text, retry_rect)
        
        # Показываем текущий счет и рекорд на экране Game Over
        final_score_text = font_medium.render(f'YOUR SCORE: {score}', True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect()
        final_score_rect.midbottom = (W//2, H//2 - 40)
        screen.blit(final_score_text, final_score_rect)
        
        record_text = font_medium.render(f'RECORD: {high_score}', True, (255, 215, 0))
        record_rect = record_text.get_rect()
        record_rect.midbottom = (W//2, H//2 - 80)
        screen.blit(record_text, record_rect)
    else:
        if not paused:  # Обновление игрового состояния только если не пауза
            player.update()
            player.update_moon_jump()  # Обновляем состояние суперспособности
            
            now = pygame.time.get_ticks()
            elapsed = now - last_spawn_time
            if elapsed > spawn_delay:
                last_spawn_time = now
                goombas.append(Goomba())

            for goomba in list(goombas):
                if goomba.is_out:
                    goombas.remove(goomba)
                else:
                    goomba.update()

                    if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                        if player.rect.bottom - player.y_speed < goomba.rect.top:
                            goomba.kill(enemy_dead_image)
                            player.jump()
                            score += 1
                            spawn_delay = INIT_DELAY / (DECREASE_BASE**score)
                            
                            # Обновляем рекорд в реальном времени
                            if score > high_score:
                                high_score = score
                        else:
                            player.kill(player_image)
                            death_sound.play()  # Воспроизводим звук смерти игрока
        
        # Отрисовка всегда (даже в паузе)
        player.draw(screen)
        for goomba in goombas:
            goomba.draw(screen)
        
        if paused:  # Показываем текст паузы
            screen.blit(pause_text, pause_rect)
        
        # Показываем статус суперспособности
        if player.moon_jump_ready and not player.is_out:
            screen.blit(super_text, super_rect)
        
        # Отрисовываем подсказки управления
        if not player.is_out:  # Не показываем подсказки на экране Game Over
            screen.blit(controls_bg, controls_rect)
            screen.blit(controls_text1, controls_positions[0])
            screen.blit(controls_text2, controls_positions[1])
            screen.blit(controls_text3, controls_positions[2])
            screen.blit(controls_text4, controls_positions[3])
        
        # Отображаем текущий рекорд в углу
        screen.blit(high_score_text, high_score_rect)
        
        score_rect.midtop = (W//2, 5)

    screen.blit(score_text, score_rect)
    pygame.display.flip()

# Перед выходом сохраняем рекорд
if score > high_score:
    save_high_score(score)

pygame.quit()