# -*- coding: utf-8 -*-

import pygame

class Widget:
    
    # Un widget representa cualquier cosa "pintable"
    
    def __init__(self, container, rect_in_container, frame_rate, surface, tooltip=None):
        self.container = container # Ventana (Rect) que "contiene" al widget
        self.set_rect_in_container(rect_in_container)
        self.frame_rate = frame_rate
        self.background = surface
        
        # El widget puede (opcionalmente) tener un tooltip
        self.tooltip = tooltip
        self.showing_tooltip = False
    
    def draw(self, screen):
        screen.blit(self.background, self.rect_absolute)
        return self.rect_absolute
    
    def force_update(self): # Forzamos la actualizacion del widget independientemente del frame_rate
        #screen.blit(self.background, self.rect_in_container)
        #pygame.display.update(self.rect_in_container)
        pass
    
    def set_rect_in_container(self, rect):
        # Rect del widget (relativo al container)
        self.rect_in_container = rect
        
        # Rect del widget (absoluto al screen)
        self.rect_absolute = pygame.Rect((self.container.left + self.rect_in_container.left, self.container.top + self.rect_in_container.top), (self.rect_in_container.size))
  
    def set_rect_size(self, size):
        # Rect del widget (relativo al container)
        self.rect_in_container.size = size
        
        # Rect del widget (absoluto al screen)
        self.rect_absolute.size = size
      