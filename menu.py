import pygame
import random
import os

class Menu:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Приключение Лунного Кота")
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_BLUE = (173, 216, 230)
        self.DARK_BLUE = (30, 30, 70)
        
        # Загрузка шрифтов
        try:
            font_path = os.path.join('images', 'mario_font.ttf')
            self.title_font = pygame.font.Font(font_path, 64)
            self.button_font = pygame.font.Font(font_path, 36)
        except:
            self.title_font = pygame.font.SysFont('arial', 64)
            self.button_font = pygame.font.SysFont('arial', 36)
        
        # Загрузка музыки для меню
        self.load_menu_music()
        
        # Создание элементов меню
        self.create_menu_elements()
    
    def load_menu_music(self):
        """Загружает и настраивает фоновую музыку для меню"""
        try:
            pygame.mixer.music.load(os.path.join('music', 'menu_music.mp3'))  # Убедитесь, что файл существует
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
        except Exception as e:
            print(f"Не удалось загрузить музыку меню: {e}")
    
    def create_menu_elements(self):
        """Создает все элементы интерфейса меню"""
        # Текст меню
        self.title_line1 = self.title_font.render("Приключение", True, self.WHITE)
        self.title_line2 = self.title_font.render("Лунного Кота", True, self.WHITE)
        self.title_rect1 = self.title_line1.get_rect(center=(self.WIDTH//2, self.HEIGHT//4 - 40))
        self.title_rect2 = self.title_line2.get_rect(center=(self.WIDTH//2, self.HEIGHT//4 + 40))
        
        # Создание кнопок
        self.play_button = self.create_button(self.WIDTH//2 - 150, self.HEIGHT//2, 300, 50, "Играть")
        self.exit_button = self.create_button(self.WIDTH//2 - 150, self.HEIGHT//2 + 100, 300, 50, "Выход")
        
        # Фон с звездами
        self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background.fill(self.DARK_BLUE)
        for _ in range(100):
            x, y = random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(self.background, self.WHITE, (x, y), size)
    
    def create_button(self, x, y, width, height, text):
        """Создает кнопку меню"""
        button = {
            'rect': pygame.Rect(x, y, width, height),
            'text': text,
            'hovered': False
        }
        return button
    
    def draw_button(self, button):
        """Отрисовывает кнопку меню"""
        color = self.WHITE if button['hovered'] else self.LIGHT_BLUE
        pygame.draw.rect(self.screen, color, button['rect'], border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, button['rect'], 2, border_radius=10)
        
        text_surf = self.button_font.render(button['text'], True, self.BLACK)
        text_rect = text_surf.get_rect(center=button['rect'].center)
        self.screen.blit(text_surf, text_rect)
    
    def run(self):
        """Запускает главный цикл меню"""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    return 'exit'
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_button['rect'].collidepoint(mouse_pos):
                        pygame.mixer.music.fadeout(500)  # Плавное затухание музыки
                        return 'play'
                    elif self.exit_button['rect'].collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        return 'exit'
            
            # Проверка наведения на кнопки
            self.play_button['hovered'] = self.play_button['rect'].collidepoint(mouse_pos)
            self.exit_button['hovered'] = self.exit_button['rect'].collidepoint(mouse_pos)
            
            # Отрисовка
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title_line1, self.title_rect1)
            self.screen.blit(self.title_line2, self.title_rect2)
            self.draw_button(self.play_button)
            self.draw_button(self.exit_button)
            
            pygame.display.flip()
        
        return 'exit'