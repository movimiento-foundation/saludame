# -*- coding: utf-8 -*-

from window import Window
import menu_creator
import pygame
import animation
import os

BACKGROUND_PATH = os.path.normpath("assets/background/schoolyard_sunny.png")

class KidWindow(Window):

    def __init__(self, container, rect, frame_rate, windows_controller, game_man):
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "kid_window")
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())        
        
        self.kid_rect = pygame.Rect((80, 10), (350, 480))       
        kid_window = animation.Kid(rect, self.kid_rect, 1, windows_controller, game_man)
        
        self.add_window(kid_window)
        kid_window.set_bg_image(self.bg_image.subsurface(self.kid_rect))          

        self.windows.append(menu_creator.load_menu(game_man, (200, 200), self.rect, windows_controller))
    

