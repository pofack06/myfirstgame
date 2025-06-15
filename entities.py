import pygame
import random
from constants import W, H, GROUND_H

class Entity:
    def __init__(self, image):
        self.image = image
        self.current_image = image
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0 
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.jump_speed = -12
        self.gravity = 0.5
        self.is_grounded = False
        self.facing_right = True
    
    def handle_input(self):
        pass

    def kill(self, dead_image=None):  # Сделаем аргумент необязательным
        if dead_image:
            self.current_image = dead_image
            self.image = dead_image
        self.is_dead = True
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed
        return True  # Возвращаем True для воспроизведения звука

    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.x_speed > 0:
            self.facing_right = True
            self.current_image = pygame.transform.flip(self.image, True, False)
        elif self.x_speed < 0:
            self.facing_right = False
            self.current_image = self.image

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
        surface.blit(self.current_image, self.rect)

class Player(Entity):
    def __init__(self, image):
        super().__init__(image)
        self.can_jump = True
        self.moon_jump_ready = True
        self.moon_jump_active = False
        self.moon_jump_start_time = 0
        self.moon_jump_duration = 2000
        self.moon_jump_cooldown = 10000
        self.original_jump_speed = self.jump_speed
        self.rect.midbottom = (100, H - GROUND_H)
        self.invincible = False
        self.invincible_timer = 0
    
    def handle_input(self):
        self.x_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed
        elif keys[pygame.K_d]:
            self.x_speed = self.speed
    
    def respawn(self):
        self.is_dead = False
        self.y_speed = 0
        self.current_image = self.image
        self.facing_right = True
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks() + 2000  # 2 секунды неуязвимости
            
            # Не меняем позицию игрока, только сбрасываем состояние
        self.rect.bottom = min(self.rect.bottom, H - GROUND_H)  # Не даем уйти ниже земли
        if self.rect.top < 0:  # Если игрок вышел за верх экрана
            self.rect.top = 0 
    
    def jump(self):
        if self.is_grounded:
            self.is_grounded = False
            self.y_speed = self.jump_speed
            return True  # Возвращаем True для воспроизведения звука
        return False
    
    def activate_moon_jump(self):
        if self.moon_jump_ready and not self.moon_jump_active:
            self.moon_jump_active = True
            self.moon_jump_start_time = pygame.time.get_ticks()
            self.moon_jump_ready = False
            self.jump_speed = self.original_jump_speed * 1.5
            return True  # Возвращаем True для воспроизведения звука
        return False
    
    def update_moon_jump(self):
        current_time = pygame.time.get_ticks()
        if self.moon_jump_active:
            if current_time - self.moon_jump_start_time > self.moon_jump_duration:
                self.moon_jump_active = False
                self.jump_speed = self.original_jump_speed
        elif not self.moon_jump_ready:
            if current_time - self.moon_jump_start_time > self.moon_jump_cooldown:
                self.moon_jump_ready = True

    def update(self):
        super().update()
        current_time = pygame.time.get_ticks()
        if self.invincible and current_time > self.invincible_timer:
            self.invincible = False
    
    def draw(self, surface):
        if self.invincible:
            # Мигание во время неуязвимости
            if pygame.time.get_ticks() % 200 < 100:  # Мигаем каждые 100мс
                self.current_image.set_alpha(150)
            else:
                self.current_image.set_alpha(255)
        else:
            self.current_image.set_alpha(255)
        surface.blit(self.current_image, self.rect)

class Goomba(Entity):
    def __init__(self, image, dead_image):
        super().__init__(image)
        self.dead_image = dead_image
        self.spawn()

    def spawn(self):
        direction = random.randint(0,1)
        if direction == 0:
            self.x_speed = self.speed
            self.rect.bottomright = (0, 0)
            self.facing_right = True
            self.current_image = pygame.transform.flip(self.image, True, False)
        else:
            self.x_speed = -self.speed
            self.rect.bottomleft = (W, 0)
            self.facing_right = False
            self.current_image = self.image
    
    def kill(self):
        return super().kill(self.dead_image)
    
    def update(self):
        super().update()
        if self.x_speed>0 and self.rect.left > W or self.x_speed < 0 and self.rect.right < 0:
            self.is_out = True

class HeartBonus(Entity):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.rect.center = (x, y)
        self.y_speed = -15  # Сердце немного подпрыгивает при появлении
        self.lifetime = 5000  # Время жизни бонуса в миллисекундах
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self):
        super().update()
        self.y_speed += self.gravity
        
        # Исчезаем после истечения времени
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.is_out = True
        
        # Останавливаемся на земле
        if self.rect.bottom > H - GROUND_H:
            self.rect.bottom = H - GROUND_H
            self.y_speed = 0

class Meteor(Entity):
    def __init__(self, image):
        super().__init__(image)
        # Увеличиваем размер метеорита (80x80 вместо 60x60)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, W - self.rect.width)
        self.rect.y = -self.rect.height
        self.y_speed = random.randint(8, 12)
        self.x_speed = random.uniform(-1.5, 1.5)  # Увеличили разброс горизонтального движения
        self.damage = 1
    
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
        if self.rect.left < 0 or self.rect.right > W:
            self.x_speed *= -1