# -*- coding: utf-8 -*-

import pygame
from window import Window
from utilities import *

"""
Clase encargada del control de ventanas
"""
class WindowsController:
    
    def __init__(self, screen):
        internal_size = 1200, 780       # The game is meant to run in this resolution
        self.scaled_game = ScaledGame(screen, internal_size)
        
        self.screen = self.scaled_game.get_internal_screen()
        
        self.windows = {} # Diccionario de ventanas. Aca se encuentran todas las ventanas del programa
        self.windows_stack = [] # Stack de ventanas para el control de venta activa. Aca se enceuntra el stack de ventanas abiertas
        self.reload_main = True
        
        self.next_update_list = []
        
        # Tooltips
        self.showing_tooltip = False
        self.active_tooltip_bg = None
        self.active_tooltip = None
        
    def close_active_window(self):
        self.windows_stack[-1].repaint = True
        # Solo puede ser llamado por la ventana activa e implica
        # hacer un pop del stack
        self.windows_stack.pop()        
        if (self.windows_stack[-1].name == "main"):
            self.reload_main = True 
            for win in self.windows_stack[-1].windows:
                if isinstance(win, Window):
                    win.enable_repaint()
    
    def set_active_window(self, window_key):
        self.windows_stack.append(self.windows[window_key])
        
    def add_new_window(self, window, window_key):
        self.windows[window_key] = window
        
    def handle_mouse_down(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_down((x, y))
                
    def handle_mouse_over(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_over((x, y))
        
    def show_tooltip(self, tooltip):
        x, y = self.scaled_game.scale_coordinates(pygame.mouse.get_pos())
        self.active_tooltip = Text(self.screen.get_rect(), x, y, 1, tooltip, 20, pygame.Color('red'))
        
        # Necesitamos guardar lo que esta atras del tooltip para cuando lo querramos esconder
        self.active_tooltip_bg = (self.screen.subsurface(self.active_tooltip.rect_absolute).copy(), self.active_tooltip.rect_absolute) 
        self.showing_tooltip = True
        
    def hide_active_tooltip(self):
        # Solo se ejecuta si se esta mostrando algun tooltip en la pantalla
        if self.showing_tooltip:
            # Hacemos un blit con lo que tenia atras el tooltip
            self.screen.blit(self.active_tooltip_bg[0], self.active_tooltip_bg[1])
            # Lo guardamos en la lista de las proximas actualizaciones 
            self.next_update(self.active_tooltip_bg[1])      
            self.showing_tooltip = False
            
    def next_update(self, rect):
        # Agregamos un rectangulo que debe ser actualizado en el proximo update
        self.next_update_list.append(rect)
        
    def update(self, frames):
        
        # Cada vez que "volvamos" a la ventana principal es necesario
        # repintar el fondo para que no queden rastros de la ventana anterior  
        if (self.reload_main): 
            pygame.display.flip() # Actualizamos el screen para hacer visibles los efectos
            self.reload_main = False       
        
        changes = []
        if frames % self.windows_stack[-1].frame_rate == 0:
            changes.extend(self.windows_stack[-1].draw(self.screen, frames))   
        
        if changes:
            if self.next_update_list:
                changes.extend(self.next_update_list)
                self.next_update_list = [] # Vaciamos la lista
        
        # Tooltips        
        if self.showing_tooltip:
            self.screen.fill((255,255,255), self.active_tooltip.rect_in_container)
            # Le decimos al tooltip (widget) que se dibuje
            self.active_tooltip.draw(self.screen)
            changes.append(self.active_tooltip_bg[1])
        
        self.scaled_game.update_screen(changes)


class ScaledGame:
    
    def __init__(self, pygame_screen, internal_size):
        self.screen = pygame_screen

        pygame_screen_size = pygame_screen.get_size()
        self.scale_factor = pygame_screen_size[0] / float(internal_size[0]), pygame_screen_size[1] / float(internal_size[1])
        
        if self.scale_factor == (1, 1):
            self.internal_screen = self.screen
        else:
            self.internal_screen = pygame.Surface(internal_size)
        
        
    def get_internal_screen(self):
        """ Returns the screen where everything should be drawn.
        If using scalation its a virtual surface if not is the real display surface.
        """
        return self.internal_screen
    
    def update_screen(self, rect_list):
        if self.scale_factor == (1,1):
            pygame.display.update(rect_list)
        else:
            pygame.transform.scale(self.internal_screen, self.screen.get_size(), self.screen)
            pygame.display.update(self.scale_rect_list(rect_list))
    
    def scale_rect_list(self, rect_list):
        return [self.scale_rect(rect) for rect in rect_list if rect]
    
    def scale_rect(self, rect):
        if rect:
            left = int(rect.left * self.scale_factor[0])
            top = int(rect.top * self.scale_factor[1])
            width = int(rect.width * self.scale_factor[0])
            height = int(rect.height * self.scale_factor[1])
            return pygame.Rect(left, top, width, height)
        else:
            return None
    
    def scale_coordinates(self, display_coordinates):
        """ Retruns the internal coordinates corresponding to the display coordinates """
        if self.scale_factor == (1,1):
            return display_coordinates
        else:
            x = int(display_coordinates[0] / self.scale_factor[0])
            y = int(display_coordinates[1] / self.scale_factor[0])
            return x, y
        