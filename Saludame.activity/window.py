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
    
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
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
                            
            self.background.fill(self.bg_color)      
                  
            if self.bg_image != None:
                
                if (not isinstance(self.background, pygame.Surface)):
                    # Si entramos aca es porque es una imagen que tenemos que convertir
                    self.background = pygame.image.load(self.bg_image).convert_alpha()
                else:
                    self.background = self.bg_image

            screen.blit(self.background, self.rect) # Pintamos el "fondo" de la ventana
            
            changes.append(self.rect)
                        
            self.repaint = False
        
        for widget in self.widgets:
            if (frames % widget.frame_rate == 0):
                changes.append(widget.draw(screen)) # Pintamos los widgets que "contiene" la ventana
            
        for win in self.windows:
            if (frames % win.frame_rate == 0):
                changes.extend(win.draw(screen, frames)) # Le decimos a cada ventana que se pinte
                      
        return changes
    
    def add_child(self, widget):
        self.widgets.append(widget)
        
    def add_window(self, window):
        self.windows.append(window)
        
    def enable_repaint(self):
        self.repaint = True
        for win in self.windows:
            win.enable_repaint()
    
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
    
    def play_animation(self, id):
        self.actual_animation = (self.actions_dictionary[id][0], self.actions_dictionary[id][1])
        self.on_animation = True
        
    def pre_draw(self, screen):
            
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
        
        return [self.rect]        

class KidWindow(Window):

    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())        
        
        kid_rect = pygame.Rect((80, 10), (350, 480))       
        kid_window = animation.Kid(rect, kid_rect, 1, windows_controller)
        
        self.add_window(kid_window)
        kid_window.set_bg_image(self.bg_image.subsurface(kid_rect))          

class MainWindow(Window):
    
    def __init__(self, container, rect, frame_rate, clock, windows_controller, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        
        self.name = "main"
        self.clock = clock
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        
        #temporal para probar ActionWindow (se cargará el diccionario en un módulo aparte).
        self.animations_dic = {'eat_apple': (animation.Apple(pygame.Rect((210, 20), (150, 172)), 10), "Eating an apple!") }
        self.action_win = ActionWindow(container, pygame.Rect((0, 505), (600, 200)), 10, windows_controller, self.animations_dic, pygame.Color("blue"))
        
        self.status_bars = status_bars.BarsWindow((0, 0), 1, pygame.Color("gray"))
        #self.add_window(self.status_bars)

        
        self.windows.append(KidWindow(container, pygame.Rect((0, 0), (600, 500)), 1, windows_controller))
        #self.windows.append(animation.Apple(pygame.Rect((700, 90), (150, 172)), 10))        
        
        self.windows.append(animation.FPS(container, pygame.Rect((650, 80), (50, 20)), 15, self.clock))
        self.windows.append(self.action_win)  
        #self.windows.append(status_bars.BarsWindow((700, 90), 1, pygame.Color("gray")))
        
        challengesButton = ImageButton(self.rect, pygame.Rect((700, 300), (80, 80)), 1, "challenges/trophy.png", self._cb_button_click_challenges)
        customizationButton = ImageButton(self.rect, pygame.Rect((700, 400), (80, 80)), 1, "customization/palette.png", self._cb_button_click_customization)
        
        self.buttons.append(challengesButton)
        self.buttons.append(customizationButton) 
        
        for b in self.buttons:
            self.add_child(b) 
            
    ######## Callbacks buttons  ########   
        
    def _cb_button_click_challenges(self, button):
        self.windows_controller.set_active_window("challenges")
        
    def _cb_button_click_customization(self, button):
        self.windows_controller.set_active_window("customization")
    
    ########################################

