# -*- coding: utf-8 -*-

import pygame
from window import Window
import animation
import os
from widget import Widget
import window

PANEL_BG_PATH = os.path.normpath("assets/layout/panel.png")

class PanelWindow(Window):
    """
    Ventana de acciones
    """
    def __init__(self, container, rect, frame_rate, windows_controller, actions_dictionary, bg_color=(0, 0, 0)):
        
        self.timing = 1 # la idea de timing es llevar una cuenta adentro, de los frames que fueron pasando        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "panel_window", bg_color)
        
        # Actions
        self.surf_action = pygame.Surface((260, 110))
        self.surf_action.fill((255, 255, 255))
        self.actions_dictionary = actions_dictionary
        self.on_animation = False
        self.actual_animation = None
        self.set_bg_image(PANEL_BG_PATH)
        
        # Personal
        
        # Environment 
        
        # Social
        
        # Info
        info = Info(rect, pygame.Rect(885, 0, 1, 1), 1)
        self.add_child(info)
    
    def play_animation(self, id):
        self.actual_animation = (self.actions_dictionary[id][0], self.actions_dictionary[id][1])
        self.on_animation = True
        
    def pre_draw(self, screen):    
          
        # Actions  
        self.timing += 1
        changes = []
        if(self.on_animation and self.actual_animation != None and self.timing % self.actual_animation[0].frame_rate == 0):
            if(self.timing > 12):
                self.timing = 0
            
            font = pygame.font.SysFont("Dejavu", 25)
            self.surf_action.blit(font.render(self.actual_animation[1], 1, (0, 0, 255)), (120, 20))
            changes += self.actual_animation[0].draw(self.surf_action, self.timing)
        
        screen.blit(self.surf_action, (780, 652))
        
        # Personal
        
        # Environment 
        
        # Social
        
        # Info
        
        return [self.rect]
    
class Info(Widget):    
    
    def __init__(self, container, rect_in_container, frame_rate):
        surface = pygame.image.load("assets/layout/info.png").convert_alpha()
        rect_in_container.size = surface.get_size()
        Widget.__init__(self, container, rect_in_container, frame_rate, surface)
