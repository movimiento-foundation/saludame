# -*- coding: utf-8 -*-

import pygame
from gettext import gettext as _

from window import *
import status_bars

class MainWindow(Window):
    
    def __init__(self, container, rect, frame_rate, clock, windows_controller, cha_loader, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        
        self.name = "main"
        self.clock = clock
        self.cha_loader = cha_loader
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        
        #temporal para probar ActionWindow (se cargará el diccionario en un módulo aparte).
        self.animations_dic = {'eat_apple': (animation.Apple(pygame.Rect((210, 20), (150, 172)), 10), "Eating an apple!") }
        self.action_win = ActionWindow(container, pygame.Rect((200, 505), (600, 200)), 10, windows_controller, self.animations_dic, pygame.Color("blue"))
                
        self.windows.append(KidWindow(container, pygame.Rect((200, 0), (600, 500)), 1, windows_controller))
        #self.windows.append(animation.Apple(pygame.Rect((700, 90), (150, 172)), 10))        
        
        self.windows.append(animation.FPS(container, pygame.Rect((650, 80), (50, 20)), 15, self.clock))
        self.windows.append(self.action_win)  
        self.windows.append(status_bars.BarsWindow(container, pygame.Rect(0, 0, 227, 590), 1, windows_controller))
        
        challengesButton = ImageButton(self.rect, pygame.Rect((700, 300), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_challenges)
        challengesButton.set_tooltip("Challenges module")
        customizationButton = ImageButton(self.rect, pygame.Rect((700, 400), (50, 50)), 1, "customization/palette.png", self._cb_button_click_customization)
        
        self.buttons.append(challengesButton)
        self.buttons.append(customizationButton) 
        
        for b in self.buttons:
            self.add_child(b) 
        
    def _cb_button_click_challenges(self, button):
        challenges_window = self.cha_loader.get_challenge()
        self.windows_controller.add_new_window(challenges_window, "challenges")
        self.windows_controller.set_active_window("challenges")
        
    def _cb_button_click_customization(self, button):
        self.windows_controller.set_active_window("customization")
    