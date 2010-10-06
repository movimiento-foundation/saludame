# -*- coding: utf-8 -*-

import pygame

class Widget:
    
    # Un widget representa cualquier cosa "pintable"
    
    def __init__(self, container, rect, frame_rate, surface, tooltip=None):
        self.container = container # Ventana (Rect) que "contiene" al widget
        self.rect = rect # Rect del widget (relativo al container)
        self.rect_in_container = pygame.Rect((self.container.left + self.rect.left,
                                              self.container.top + self.rect.top),
                                              (self.rect.size)) # Rect del widget (absoluto al screen)
        self.frame_rate = frame_rate
        self.background = surface
        
        # El widget puede (opcionalmente) tener un tooltip
        self.tooltip = tooltip
        
    def draw(self, screen):           
        screen.blit(self.background, self.rect_in_container)        
        return self.rect_in_container  
    
    def force_update(self): # Forzamos la actualizacion del widget independientemente del frame_rate
        #screen.blit(self.background, self.rect_in_container)
        #pygame.display.update(self.rect_in_container)
        pass
        
                  
