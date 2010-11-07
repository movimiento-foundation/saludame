# -*- coding: utf-8 -*-
import os
import pygame

from window import Window
import utilities
import menu_creator
import animation

BACKGROUND_PATH = os.path.normpath("assets/background/schoolyard_sunny.png")

class KidWindow(Window):

    def __init__(self, container, rect, frame_rate, windows_controller, game_man):
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "kid")
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())   
        
        self.kid_rect = pygame.Rect((280, 70), (350, 480))  
        self.mood = "normal" 
            
        self.kid = animation.Kid(rect, self.kid_rect, 1, windows_controller, game_man, self.mood)
        
        self.add_window(self.kid)
        self.kid.set_bg_image(self.bg_image.subsurface(self.kid_rect))          

        self.balloon = None
        
        # Menu
        self.menu = menu_creator.load_menu(game_man, (480, 270), self.rect, windows_controller)
        self.add_window(self.menu)
        
        # Para probar:
        self.show_kid_balloon("Me duele la panza :(")
        
        self.last_repaint = False
        
    def change_mood(self):
        self.kid.change_mood()
    
    def show_kid_balloon(self, text):
        self.balloon = KidBalloon(self.rect, pygame.Rect(580, 80, 1, 1), 1, self.windows_controller)
        self.balloon.set_text(text)
        self.add_window(self.balloon)

    def draw(self, screen, frames):
        
        if self.last_repaint:
            self.repaint = True
            self.last_repaint = False
            
        # If the menu is showing repaint the whole window
        if self.menu.show:
            self.last_repaint = True
            self.repaint = True
        
        return Window.draw(self, screen, frames)
        
class KidBalloon(Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller):
        background = pygame.image.load("assets/events/balloon.png").convert_alpha()
        rect.size = background.get_size()
        Window.__init__(self, container, rect, frame_rate, windows_controller, "balloon")
        self.set_bg_image(background)
        self.text = None
        
    def set_text(self, text):
        self.text = utilities.TextBlock(self.rect, 140, 20, 1, text, 18, pygame.Color(0,0,0))
        self.add_child(self.text)
    
    def draw(self, screen, frames):
        self.repaint = True
        return Window.draw(self, screen, frames)
        