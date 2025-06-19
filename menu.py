import pygame
import os

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Инициализация звуковой системы
        
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Приключение Лунного Кота")
        
        # Загрузка и настройка музыки
        self.music_volume = 0.5  # Громкость музыки (от 0.0 до 1.0)
        self.current_track = None
        self.load_music()
        
        # Загрузка фонового изображения
        self.background = self.load_background()
        self.bg_offset = 0  # Для параллакс-эффекта
        
        # Полупрозрачный оверлей для текста
        self.overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Черный с прозрачностью 50%
        
        # Инициализация элементов меню
        self.init_elements()
        
        # Для плавного перехода
        self.transition_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.transition_speed = 15
        
        # Запуск фоновой музыки
        self.play_music("menu")
    
    def load_music(self):
        #Загружает и настраивает музыкальные треки
        self.music_tracks = {
            "menu": os.path.join('music', 'menu_music.mp3'),
            "gameplay": os.path.join('music', 'Factory.ogg')
        }
        
        # Проверяем существование файлов
        for name, path in self.music_tracks.items():
            if not os.path.exists(path):
                print(f"Предупреждение: музыкальный файл не найден - {path}")
                self.music_tracks[name] = None
        
        # Настройка микшера
        pygame.mixer.music.set_volume(self.music_volume)
    
    def play_music(self, track_name, loops=-1):
        # Воспроизводит фоновую музыку
        if track_name not in self.music_tracks or not self.music_tracks[track_name]:
            return
            
        if self.current_track != track_name:
            try:
                pygame.mixer.music.load(self.music_tracks[track_name])
                pygame.mixer.music.play(loops=loops)
                self.current_track = track_name
            except Exception as e:
                print(f"Ошибка загрузки музыки: {e}")
    
    def stop_music(self, fadeout=1000):
        #плавно останавливает музыку
        pygame.mixer.music.fadeout(fadeout)
        self.current_track = None
    
    def set_music_volume(self, volume):
        #устанавливает громкость музыки
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def load_background(self):
        #загружает и подгоняет фоновое изображение
        try:
            bg_path = os.path.join('images', 'menu_bg.jpg')
            background = pygame.image.load(bg_path).convert()
            
            # Рассчитываем соотношение сторон
            bg_width, bg_height = background.get_size()
            screen_ratio = self.WIDTH / self.HEIGHT
            bg_ratio = bg_width / bg_height
            
            if bg_ratio > screen_ratio:
                # Обрезаем по ширине
                new_height = bg_height
                new_width = int(bg_height * screen_ratio)
                crop_x = (bg_width - new_width) // 2
                background = background.subsurface((crop_x, 0, new_width, new_height))
            else:
                # Обрезаем по высоте
                new_width = bg_width
                new_height = int(bg_width / screen_ratio)
                crop_y = (bg_height - new_height) // 2
                background = background.subsurface((0, crop_y, new_width, new_height))
            
            return pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            # Создаем градиентный фон если изображение не загрузилось
            background = pygame.Surface((self.WIDTH, self.HEIGHT))
            for y in range(self.HEIGHT):
                color = 30 + int(40 * y / self.HEIGHT)
                pygame.draw.line(background, (color, color, 70), (0, y), (self.WIDTH, y))
            return background
    
    def init_elements(self):
        # Инициализирует элементы меню
        # Шрифты
        try:
            font_path = os.path.join('images', 'mario_font.ttf')
            self.title_font = pygame.font.Font(font_path, 64)
            self.button_font = pygame.font.Font(font_path, 36)
        except:
            self.title_font = pygame.font.SysFont('arial', 64)
            self.button_font = pygame.font.SysFont('arial', 36)
        
        # Текст меню (без тени)
        self.title_line1 = self.title_font.render("Приключение", True, (255, 255, 255))
        self.title_line2 = self.title_font.render("Лунного Кота", True, (255, 255, 255))
        
        # Кнопки
        self.play_button = self.create_button(self.WIDTH//2 - 150, self.HEIGHT//2, 300, 50, "Играть")
        self.exit_button = self.create_button(self.WIDTH//2 - 150, self.HEIGHT//2 + 100, 300, 50, "Выход")
        self.sound_button = self.create_button(self.WIDTH - 240, 40, 200, 50, 
                                             "Звук: Вкл" if self.music_volume > 0 else "Звук: Выкл")
    
    def create_button(self, x, y, width, height, text):
        # Создает кнопку меню с анимацией
        return {
            'rect': pygame.Rect(x, y, width, height),
            'text': text,
            'hovered': False,
            'scale': 1.0,
            'target_scale': 1.0
        }
    
    def draw_button(self, button):
        #отрисовывает анимированную кнопку
        # Анимация масштаба
        button['scale'] += (button['target_scale'] - button['scale']) * 0.1
        
        # Создаем поверхность для кнопки
        btn_surface = pygame.Surface((int(button['rect'].width * button['scale']), 
                                    int(button['rect'].height * button['scale'])), pygame.SRCALPHA)
        
        # Цвет кнопки
        color = (255, 255, 255, 200) if button['hovered'] else (173, 216, 230, 200)
        pygame.draw.rect(btn_surface, color, (0, 0, btn_surface.get_width(), btn_surface.get_height()), 
                        border_radius=int(10 * button['scale']))
        pygame.draw.rect(btn_surface, (0, 0, 0, 200), (0, 0, btn_surface.get_width(), btn_surface.get_height()), 
                        2, border_radius=int(10 * button['scale']))
        
        # Текст кнопки
        text_surf = self.button_font.render(button['text'], True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(btn_surface.get_width()//2, btn_surface.get_height()//2))
        btn_surface.blit(text_surf, text_rect)
        
        # Позиционирование
        btn_rect = btn_surface.get_rect(
            center=(button['rect'].centerx, button['rect'].centery))
        self.screen.blit(btn_surface, btn_rect)
    
    def run_transition(self, direction=1):
        #Анимация перехода (1 - вперед, -1 - назад)
        for alpha in range(0, 255, self.transition_speed * direction)[::direction]:
            self.transition_surface.fill((255, 255, 255, abs(alpha)))
            self.screen.blit(self.transition_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)
    
    def toggle_sound(self):
        #Переключает звук и обновляет текст кнопки
        if self.music_volume > 0:
            self.set_music_volume(0.0)
            self.sound_button['text'] = "Звук: Выкл"
        else:
            self.set_music_volume(0.5)
            self.sound_button['text'] = "Звук: Вкл"
            if not self.current_track:
                self.play_music("menu")
    
    def run(self):
        # Главный цикл меню
        running = True
        clock = pygame.time.Clock()
        
        while running:
            dt = clock.tick(60) / 1000.0  # Дельта времени для плавной анимации
            mouse_pos = pygame.mouse.get_pos()
            
            # Отрисовка фона (без параллакса)
            self.screen.blit(self.background, (0, 0))
            
            # Затемнение фона
            self.screen.blit(self.overlay, (0, 0))
            
            # Текст меню (без тени)
            self.screen.blit(self.title_line1, (self.WIDTH//2 - self.title_line1.get_width()//2, 
                                              self.HEIGHT//4 - 40))
            self.screen.blit(self.title_line2, (self.WIDTH//2 - self.title_line2.get_width()//2, 
                                              self.HEIGHT//4 + 40))
            
            # Обновление кнопок
            buttons = [self.play_button, self.exit_button, self.sound_button]
            for button in buttons:
                was_hovered = button['hovered']
                button['hovered'] = button['rect'].collidepoint(mouse_pos)
                
                # Анимация при наведении
                if button['hovered'] and not was_hovered:
                    button['target_scale'] = 1.1
                elif not button['hovered'] and was_hovered:
                    button['target_scale'] = 1.0
                
                self.draw_button(button)
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.stop_music()
                    return 'exit'
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_button['rect'].collidepoint(mouse_pos):
                        self.run_transition(1)  # Анимация перехода
                        self.stop_music()
                        return 'play'
                    elif self.exit_button['rect'].collidepoint(mouse_pos):
                        self.run_transition(1)
                        self.stop_music()
                        return 'exit'
                    elif self.sound_button['rect'].collidepoint(mouse_pos):
                        self.toggle_sound()
            
            pygame.display.flip()
        
        self.stop_music()
        return 'exit'