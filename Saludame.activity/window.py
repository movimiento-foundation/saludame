# -*- coding: utf-8 -*-

import pygame
import os
import menu_creator
import animation
import status_bars

from utilities import *

BLACK = pygame.Color("black")
BACKGROUND_PATH = os.path.normpath("assets/background/background.png")

class Window:
    
    # Una ventana contiene 'n' widgets
    
    def __init__(self, rect, frame_rate, background, screen, windows_controller):
        self.rect = rect
        self.frame_rate = frame_rate
        self.background = background
        self.surface = pygame.Surface((rect.width, rect.height))
        self.screen = screen
        self.windows_controller = windows_controller
        
        self.widgets = [] # Lista de widgets que contiene la ventana
        self.windows = [] # Lista de ventanas que contiene la ventana
        self.buttons = [] # Lista de botones que contiene la ventana
        
        self.repaint = True
        
    def draw(self, screen, frames):
        if self.repaint:    # Solo actualizamos el fondo de la ventana cuando hagamos un 'repaint'
                            # De otra forma solo actualizamos los widgets
            if ((not isinstance(self.background, pygame.Surface)) and (not isinstance(self.background, tuple)) and (not isinstance(self.background, pygame.Color))):
                # Si entramos aca es porque es una imagen que tenemos que convertir
                self.surface = pygame.image.load(self.background).convert_alpha()
            else:
                self.surface.fill(self.background) # En este caso background se corresponde con un color            
            
            screen.blit(self.surface, self.rect) # Pintamos el "fondo" de la ventana
                        
            self.repaint = False
        
        self.widgets.extend(self.buttons) # Agregamos los botones a la lista de widgets para que sean pintados
        
        for widget in self.widgets:
            if (frames % widget.frame_rate == 0):
                widget.draw(screen) # Pintamos los widgets que "contiene" la ventana
            
        for win in self.windows:
            if (frames % win.frame_rate == 0):
                win.draw(screen) # Le decimos a cada ventana que se pinte
            
        return self.rect
    
    def handle_mouse_down(self, (x, y)):
        for button in self.buttons:
            if button.contains_point(x, y):
                button.on_mouse_click()
        
    def handle_mouse_over(self, (x, y)):
        for button in self.buttons:
            if button.contains_point(x, y):
                if(not button.over):
                    button.on_mouse_over()
                    button.over = True 
            else:
                # Ineficiente! Por ahora lo dejo asi para PROBAR
                # Esta todo el tiempo haciendo esto! Cambiar
                button.over = False
                button.on_mouse_out()

class KidWindow(Window):

    def __init__(self, rect, frame_rate, screen, windows_controller):
        
        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        Window.__init__(self, rect, frame_rate, self.background, screen, windows_controller)        
        
        kid_rect = pygame.Rect((100, 20), (350, 480))
        kid_background = self.background.subsurface(kid_rect)
        
        self.windows.append(animation.Kid(kid_rect, kid_background, 1))
    
    def draw(self, screen):
        """    
        if self.first:
            # First time blits the entire background
            self.first = False
            screen.blit(self.background, self.rect)
            return [self.rect]
        else:
            # Next blits only the changed areas
            changes = []
            for win in self.windows:
                changes.extend(win.draw(screen))
                
            return changes #[rect.move(self.rect.left, self.rect.top) for rect in changes]
        """   
        
        # Temporal para que se vea bien el menu principal
        screen.blit(self.background, self.rect)
        changes = [self.rect]
        for win in self.windows:
            changes.extend(win.draw(screen))
        return changes     

class MainWindow(Window):
    
    def __init__(self, rect, frame_rate, clock, screen, windows_controller):
        Window.__init__(self, rect, frame_rate, (0, 0, 0), screen, windows_controller)
        
        self.name = "main"
        self.clock = clock
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        
        self.windows.append(KidWindow(pygame.Rect((0, 0), (600, 500)), 1, screen, windows_controller))
        self.windows.append(animation.Apple(pygame.Rect((150, 550), (150, 172)), 10))        
        self.windows.append(menu_creator.load_menu())
        self.windows.append(animation.FPS(pygame.Rect((650, 80), (50, 20)), 15, self.clock))        
        self.windows.append(status_bars.BarsWindow((700, 90), 1, pygame.Color("gray")))
        
        challengesButton = ImageButton(self.rect, pygame.Rect((40, 550), (80, 80)), 1, "challenges/trophy.png", self._cb_button_click_challenges)
        customizationButton = ImageButton(self.rect, pygame.Rect((100, 550), (80, 80)), 1, "customization/palette.png", self._cb_button_click_customization)
        
        self.buttons.append(challengesButton)
        self.buttons.append(customizationButton)       
        
    def _cb_button_click_challenges(self, button):
        self.windows_controller.set_active_window("challenges")
        
    def _cb_button_click_customization(self, button):
        #self.windows_controller.set_active_window("customization")
        pass
