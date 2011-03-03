# -*- coding: utf-8 -*-

import pygame
from window import Window
from utilities import Text, TextBlock

"""
Clase encargada del control de ventanas
"""
class WindowsController:
    
    def __init__(self, screen):
        internal_size = 1200, 780       # The game is meant to run in this resolution
        self.scaled_game = ScaledGame(screen, internal_size)
        
        self.screen = self.scaled_game.get_internal_screen()
        
        self.windows = {}       # Diccionario de ventanas. Aca se encuentran todas las ventanas del programa
        self.windows_stack = [] # Stack de ventanas para el control de venta activa. Aca se enceuntra el stack de ventanas abiertas
        self.reload_main = True
        
        self.next_update_list = []      # Keeps track of updates done to the screen
        
        # Tooltips
        self.showing_tooltip = False
        self.active_tooltip = None
        
        self.mouse_on_window = None
    
    def get_screen(self):
        return self.screen
    
    # Windows
    def set_mouse_on_window(self, register_id):
        if (self.mouse_on_window != register_id and self.showing_tooltip):
            self.hide_active_tooltip()
        self.mouse_on_window = register_id
    
    def close_active_window(self):
        self.windows_stack[-1].repaint = True
        # Solo puede ser llamado por la ventana activa e implica
        # hacer un pop del stack
        self.windows_stack.pop()
        
        self.show_window_hierarchy(self.windows_stack[-1])
               
        if self.windows_stack[-1].get_register_id() == "main_window":
            self.game_man.continue_game()
            self.reload_main = True
            for win in self.windows_stack[-1].windows:
                if isinstance(win, Window):
                    win.enable_repaint()
    
    def set_active_window(self, window_key):
        if window_key <> "main_window":
            self.game_man.pause_game()
        
        self.windows_stack.append(self.windows[window_key])
        self.show_window_hierarchy(self.windows_stack[-1])
        
    def register_new_window(self, id, window):
        self.windows[id] = window
        
    def unregister_window(self, window):
        try:
            del self.windows[window.register_id]
        except:
            pass
        
    def show_window_hierarchy(self, window):
        print window.get_register_id()
        W = []
        for win in window.windows:
            W.append(win.register_id)
        print(" (%s)" % (W))
    
    
    # Events handlers
    def handle_mouse_down(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_down((x, y))
        
    def handle_mouse_up(self, pos):
        self.windows_stack[-1].handle_mouse_up(pos)
                
    def handle_mouse_over(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_over((x, y))
        
    def handle_mouse_motion(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_motion((x, y))
    
    
    # Tooltips
    def show_tooltip(self, tooltip):
        x, y = self.scaled_game.scale_coordinates(pygame.mouse.get_pos())
        self.active_tooltip = Text(self.screen.get_rect(), x, y, 1, tooltip, 18, pygame.Color('red'), "tooltip")
        
        self.showing_tooltip = True
        
    def show_super_tooltip(self, tooltip):
        x, y = self.scaled_game.scale_coordinates(pygame.mouse.get_pos())
        self.active_tooltip = TextBlock(self.screen.get_rect(), x, y, 1, tooltip, 18, pygame.Color('red'), "tooltip")
        
        self.showing_tooltip = True
    
    def hide_active_tooltip(self):
        if self.showing_tooltip:            
            for win in self.windows_stack[-1].windows:
                if win.rect.colliderect(self.active_tooltip.rect_absolute):
                    win.dirty_background = True
                    
            self.showing_tooltip = False
    
    # Updates to the screen
    def next_update(self, rect):
        """
        Add a rect that must be updated at next update
        """
        self.next_update_list.append(rect)
    
    def update(self, frames):
        """
        Updates GUI
        """

        # Cada vez que "volvamos" a la ventana principal es necesario
        # repintar el fondo para que no queden rastros de la ventana anterior
        if self.reload_main:
            self.scaled_game.flip() # Actualizamos el screen para hacer visibles los efectos
            self.reload_main = False
        
        self.windows_stack[-1].update(frames)
        
        changes = []
        if frames % self.windows_stack[-1].frame_rate == 0:
            changes.extend(self.windows_stack[-1].draw(self.screen, frames))
        
        if changes:
            if self.next_update_list:
                changes.extend(self.next_update_list)
                self.next_update_list = []
        
        # Tooltips
        if self.showing_tooltip:
            if isinstance(self.active_tooltip, Text):
                self.screen.fill((255, 255, 255), self.active_tooltip.rect_in_container)
            # Le decimos al tooltip (widget) que se dibuje
            self.active_tooltip.draw(self.screen)
            changes.append(self.active_tooltip.rect_absolute)
        
        self.scaled_game.update_screen(changes)
        #self.scaled_game.flip()

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
    
    def flip(self):
        if self.scale_factor == (1, 1):
            pygame.display.flip()
        else:
            pygame.transform.scale(self.internal_screen, self.screen.get_size(), self.screen)
            pygame.display.flip()
        
    def update_screen(self, rect_list):
        if self.scale_factor == (1, 1):
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
        if self.scale_factor == (1, 1):
            return display_coordinates
        else:
            x = int(display_coordinates[0] / self.scale_factor[0])
            y = int(display_coordinates[1] / self.scale_factor[0])
            return x, y
