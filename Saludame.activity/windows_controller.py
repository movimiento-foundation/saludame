# -*- coding: utf-8 -*-

import pygame
from window import Window
from utilities import *

"""
Clase encargada del control de ventanas
"""
class WindowsController:
    
    def __init__(self, screen):
        self.screen = screen
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
        self.windows_stack[-1].handle_mouse_down((x, y))
                
    def handle_mouse_over(self, (x, y)):
        self.windows_stack[-1].handle_mouse_over((x, y))
        
    def show_tooltip(self, tooltip):
        self.active_tooltip = Text(self.screen.get_rect(), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, tooltip, 20, pygame.Color('red'))
        
        # Necesitamos guardar lo que esta atras del tooltip para cuando lo querramos esconder
        active_tooltip_bg = pygame.PixelArray(self.screen.subsurface(self.active_tooltip.rect_in_container))
        self.active_tooltip_bg = (active_tooltip_bg.make_surface(), self.active_tooltip.rect_in_container)
        active_tooltip_bg = None # Necesario para liberar el lock sobre screen
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
        """
        Cada vez que "volvamos" a la ventana principal es necesario
        repintar el fondo para que no queden rastros de la ventana anterior        
        """
        if (self.reload_main): 
            self.screen.fill((0, 0, 0))
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
            
        pygame.display.update(changes)
