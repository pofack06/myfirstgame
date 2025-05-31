import pygame
from menu import Menu
from game import run_game

def main():
    pygame.init()
    
    # Показываем меню только один раз при запуске
    menu = Menu()
    result = menu.run()
    
    if result == 'play':
        # Запускаем игру (она теперь сама будет перезапускаться)
        run_game()
    
    pygame.quit()

if __name__ == "__main__":
    main()