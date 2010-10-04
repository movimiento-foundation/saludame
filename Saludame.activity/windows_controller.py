# -*- coding: utf-8 -*-

import pygame

"""
Clase encargada del control de ventanas
"""
class WindowsController:
    def __init__(self):
        self.windows = {} # Diccionario de ventanas. Aca se encuentran todas las ventanas del programa
        self.windows_stack = [] # Stack de ventanas para el control de venta activa. Aca se enceuntra el stack de ventanas abiertas
        self.reload_main = True
    
    def close_active_window(self):
        self.windows_stack[-1].repaint = True
        # Solo puede ser llamado por la ventana activa e implica
        # hacer un pop del stack
        self.windows_stack.pop()        
        if (self.windows_stack[-1].name == "main"):
            self.reload_main = True
            for win in self.windows_stack[-1].windows:
                win.repaint = True
    
    def set_active_window(self, window_key):
        self.windows_stack.append(self.windows[window_key])
        
    def add_new_window(self, window, window_key):
        self.windows[window_key] = window
        
    def handle_mouse_down(self, (x, y)):
        self.windows_stack[-1].handle_mouse_down((x, y))
                
    def handle_mouse_over(self, (x, y)):
        self.windows_stack[-1].handle_mouse_over((x, y))
        
    def update(self, frames, screen):
        """
        Cada vez que "volvamos" a la ventana principal es necesario
        repintar el fondo para que no queden rastros de la ventana anterior        
        """
        if (self.reload_main): 
            screen.fill((0, 0, 0))
            pygame.display.flip() # Actualizamos el screen para hacer visibles los efectos
            self.reload_main = False       
        
        changes = []
        if frames % self.windows_stack[-1].frame_rate == 0:
            changes.extend(self.windows_stack[-1].draw(screen, frames))   
          
        if changes:
            pygame.display.update(changes)
