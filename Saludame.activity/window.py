# -*- coding: utf-8 -*-

import pygame
import os
import animation

from utilities import *

BLACK = pygame.Color("black")

class Window:
    
    # Una ventana contiene 'n' widgets
    
    def __init__(self, container, rect, frame_rate, windows_controller, register_id, bg_color=None):
        self.container = container
        self.rect = pygame.Rect(container.left + rect.left, container.top + rect.top, rect.width, rect.height) # Relativo al container
        self.frame_rate = frame_rate
        self.background = pygame.Surface(rect.size)
        self.bg_color = bg_color
        self.bg_image = None
        self.windows_controller = windows_controller
        
        # Register
        self.register_id = register_id
        self.windows_controller.register_new_window(register_id, self)
        
        self.widgets = [] # Lista de widgets que contiene la ventana
        self.windows = [] # Lista de ventanas que contiene la ventana
        self.buttons = [] # Lista de botones que contiene la ventana
        
        self.repaint = True
        
    def get_register_id(self):
        return self.register_id
    
    def set_bg_image(self, image):
        if (not isinstance(image, pygame.Surface)):
            # Is a path, convert it to a surface
            self.bg_image = pygame.image.load(image).convert_alpha()
        else:
            self.bg_image = image
        
    def set_bg_color(self, color):
        self.bg_color = color
    
    # Abstract function.    
    def pre_draw(self, screen):
        return []
    
    # Logica de pintado de cualquier ventana    
    def draw(self, screen, frames):
        
        changes = []
        
        changes += self.pre_draw(screen)
        
        if self.repaint:    # Solo actualizamos el fondo de la ventana cuando hagamos un 'repaint'
                            # De otra forma solo actualizamos los widgets y subventanas                
            
            if self.bg_image != None:
                screen.blit(self.bg_image, self.rect) # Pintamos el "fondo" de la ventana
            else:
                if self.bg_color:
                    screen.fill(self.bg_color, self.rect)
            
            changes.append(self.rect)
            
            self.repaint = False
        
        for win in self.windows:
            if (frames % win.frame_rate == 0):
                changes.extend(win.draw(screen, frames)) # Le decimos a cada ventana que se pinte
        
        for widget in self.widgets:
            if (frames % widget.frame_rate == 0):
                changes.append(widget.draw(screen)) # Pintamos los widgets que "contiene" la ventana
        
        return changes
    
    def add_child(self, widget):
        self.widgets.append(widget)
        
    def add_button(self, button):
        self.add_child(self, button)
        self.buttons.append(button)
    
    def add_window(self, window):
        self.windows.append(window)
        
    def enable_repaint(self):
        self.repaint = True
        for win in self.windows:
            win.enable_repaint()
    
    def handle_mouse_down(self, (x, y)):
        for button in self.buttons:
            if button.contains_point(x, y):
                # Tooltips
                if button.showing_tooltip:
                    self.windows_controller.hide_active_tooltip()
                    button.showing_tooltip = False
                button.on_mouse_click()
        
        for win in self.windows:
            if win.rect.collidepoint(x, y):
                win.handle_mouse_down((x, y))
    
    def handle_mouse_over(self, (x, y)):
        for button in self.buttons:
            if button.contains_point(x, y):
                if(not button.over):
                    # Tooltips
                    if button.tooltip: # Si el boton tiene tooltip entonces lo mostramos
                        self.windows_controller.hide_active_tooltip()
                        self.windows_controller.show_tooltip(button.tooltip)
                        button.showing_tooltip = True
                    button.on_mouse_over()
                    button.over = True 
            else:
                # Ineficiente! Por ahora lo dejo asi para PROBAR
                # Esta todo el tiempo haciendo esto! Cambiar
                if button.showing_tooltip:
                    # Si estabamos mostrando el tooltip ahora debemos esconderlo
                    self.windows_controller.hide_active_tooltip()
                    button.showing_tooltip = False
                button.over = False
                button.on_mouse_out()

    def move(self, (x, y)):
        """ Moves the window the given offset, notifying all its subitems """
        self.rect.move_ip(x, y)
        for win in self.windows:
            win.move(x, y)
        
        # Buttons are usually in widget list, so they are not moved
        for widget in self.widgets:
            if not (self.rect == widget.container):
                widget.container.move_ip(x, y)
            widget.rect_absolute.move_ip(x, y)
