import pygame
import sys
import subprocess
import random
from settings import WIDTH, HEIGHT, WHITE, BLACK, GRAY, LIGHT_BLUE, DARK_BLUE
from fonts import title_font, button_font

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Приключение Лунного Кота")

title_line1 = title_font.render("Приключение", True, WHITE)
title_line2 = title_font.render("Лунного Кота", True, WHITE)

title_rect1 = title_line1.get_rect(center=(WIDTH//2, HEIGHT//4 - 40))
title_rect2 = title_line2.get_rect(center=(WIDTH//2, HEIGHT//4 + 40))

# Кнопки
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.text_surf = button_font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        surface.blit(self.text_surf, self.text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Создание кнопок
play_button = Button(WIDTH//2 - 150, HEIGHT//2, 300, 50, "Играть", LIGHT_BLUE, WHITE)
exit_button = Button(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 50, "Выход", LIGHT_BLUE, WHITE)

# Фоновое изображение
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(DARK_BLUE)

# Добавляем звезды для "лунного" эффекта
for _ in range(100):
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    size = random.randint(1, 3)
    pygame.draw.circle(background, WHITE, (x, y), size)

# Главный цикл меню
def main_menu():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if play_button.is_clicked(mouse_pos, event):
                running = False
                # Запуск основной игры
                subprocess.Popen(["python", "game.py"]) 
                pygame.quit()
                return
            
            if exit_button.is_clicked(mouse_pos, event):
                running = False
                pygame.quit()
                sys.exit()
        
        # Проверка наведения на кнопки
        play_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
        
        # Отрисовка
        screen.blit(background, (0, 0))
        screen.blit(title_line1, title_rect1)
        screen.blit(title_line2, title_rect2)
        play_button.draw(screen)
        exit_button.draw(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()