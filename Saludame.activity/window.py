# -*- coding: utf-8 -*-

import pygame
import os
import animation

from utilities import *

BLACK = pygame.Color("black")
BACKGROUND_PATH = os.path.normpath("assets/background/background.png")
PANEL_BG_PATH = os.path.normpath("assets/layout/panel.png")

class Window:
    
    # Una ventana contiene 'n' widgets
    
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=None):
        self.container = container
        self.rect = pygame.Rect(container.left + rect.left, container.top + rect.top, rect.width, rect.height) # Relativo al container
        self.frame_rate = frame_rate
        self.background = pygame.Surface(rect.size)
        self.bg_color = bg_color
        self.bg_image = None
        self.windows_controller = windows_controller
        
        self.widgets = [] # Lista de widgets que contiene la ventana
        self.windows = [] # Lista de ventanas que contiene la ventana
        self.buttons = [] # Lista de botones que contiene la ventana
        
        self.repaint = True
    
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
        
class ActionWindow(Window):
    """
    Ventana de acciones
    """
    def __init__(self, container, rect, frame_rate, windows_controller, actions_dictionary, bg_color=(0, 0, 0)):
        
        self.timing = 1 # la idea de timing es llevar una cuenta adentro, de los frames que fueron pasando
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        
        self.actions_dictionary = actions_dictionary
        self.on_animation = False
        self.actual_animation = None
        self.set_bg_image(PANEL_BG_PATH)
        
        info = Info(rect, pygame.Rect(885, 0, 1, 1), 10)
        self.add_child(info)
    
    def play_animation(self, id):
        self.actual_animation = (self.actions_dictionary[id][0], self.actions_dictionary[id][1])
        self.on_animation = True
        
    def pre_draw(self, screen):
        """   
        self.background.fill((0, 0, 255))      
          
        self.timing += 3
        changes = []
        if(self.on_animation and self.actual_animation != None):
            if(self.timing > 12):
                self.timing = 1
            
            font = pygame.font.Font(None, 20 + self.timing)
            self.background.blit(font.render(self.actual_animation[1], 1, (255, 255, 255)), (5, 5 + self.timing))
            changes += self.actual_animation[0].draw(self.background, self.timing)
        
         screen.blit(self.background, self.rect)
         """   
        return [self.rect]     
    
class Info(Widget):    
    
    def __init__(self, container, rect_in_container, frame_rate):
        surface = pygame.image.load("assets/layout/info.png").convert_alpha()
        rect_in_container.size = surface.get_size()
        Widget.__init__(self, container, rect_in_container, frame_rate, surface)   

class KidWindow(Window):

    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())        
        
        self.kid_rect = pygame.Rect((80, 10), (350, 480))       
        kid_window = animation.Kid(rect, self.kid_rect, 1, windows_controller)
        
        #self.add_window(kid_window)
        kid_window.set_bg_image(self.bg_image.subsurface(self.kid_rect))          


