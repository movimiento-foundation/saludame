# -*- coding: utf-8 -*-

import pygame

class Widget:
    
    # Un widget representa cualquier cosa "pintable"
    
    def __init__(self, container, rect_in_container, frame_rate, surface=None, tooltip=None):
        self.container = container # Ventana (Rect) que "contiene" al widget
        self.set_rect_in_container(rect_in_container)
        self.frame_rate = frame_rate
        self.background = surface
        self.parent = None
        
        # El widget puede (opcionalmente) tener un tooltip
        self.tooltip = tooltip
        self.super_tooltip = None
        self.showing_tooltip = False
    
    def draw(self, screen):
        if self.background:
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
           
    def get_background_and_owner(self):
        if self.background:
            return (self.background, self)
        elif self.parent:
            return self.parent.get_background_and_owner()
        else:
            return (None, None)

    def get_background(self):
        return self.get_background_and_owner()[0]
    
    def get_background_rect(self):
        background, owner = self.get_background_and_owner()
        if background:
            if self is owner:
                return background.copy()
            else:
                parents_relative_pos = self.rect_absolute.x - owner.rect.x, self.rect_absolute.y - owner.rect.y
                rect = pygame.Rect(parents_relative_pos, self.rect_absolute.size)
                return background.subsurface(rect)
        return pygame.Surface(self.rect_absolute.size)
    