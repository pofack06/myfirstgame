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

    def kill(self, dead_image):
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
        self.moon_jump_ready = True
        self.moon_jump_active = False
        self.current_image = self.image
        self.facing_right = True
    
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