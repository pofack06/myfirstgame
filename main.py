import pygame
from menu import Menu
from game import run_game

def main():
    pygame.init()

    menu = Menu()
    result = menu.run()
    
    if result == 'play':
        run_game()
    
    pygame.quit()

if __name__ == "__main__":
    main()