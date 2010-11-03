# -*- coding: utf-8 -*-

import pygame
from gettext import gettext as _

import menu_creator

from window import *
from panel_window import PanelWindow
from kid_window import KidWindow
import status_bars

class MainWindow(Window):
    
    def __init__(self, container, rect, frame_rate, clock, windows_controller, cha_loader, bars_loader, game_man):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "main_window")
        
        self.clock = clock
        self.cha_loader = cha_loader
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        
        # temporal para probar PanelWindow (se cargará el diccionario en un módulo aparte).
        # self.animations_dic = {'eat_apple': (animation.Apple(pygame.Rect((0, 0), (120, 172)), 10), "Eating an apple!") }
        
        self.panel_win = PanelWindow(container, pygame.Rect((180, 609), (1015, 200)), 1, windows_controller, pygame.Color("blue"))
        self.windows.append(self.panel_win)
        
        self.kidW = KidWindow(container, pygame.Rect((227, 0), (973, 609)), 1, windows_controller, game_man)
        self.windows.append(self.kidW)
        #self.windows.append(animation.Apple(pygame.Rect((700, 90), (150, 172)), 10))
        
        #self.windows.append(animation.FPS(container, pygame.Rect((1100, 550), (50, 20)), 15, self.clock))
        self.windows.append(status_bars.BarsWindow(container, pygame.Rect(0, 0, 227, 590), 1, windows_controller, bars_loader))
        
        self.add_child(Clock(container, pygame.Rect(0, 528, 1, 1), 40))
        
        challengesButton = ImageButton(self.rect, pygame.Rect((1000, 400), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_challenges)
        challengesButton.set_tooltip("Challenges module")
        customizationButton = ImageButton(self.rect, pygame.Rect((1000, 530), (50, 50)), 1, "customization/palette.png", self._cb_button_click_customization)
        customizationButton.set_tooltip("Customization module")
        
        stop_animation_button = TextButton(self.rect, pygame.Rect((800, 550), (30, 30)), 1, "Stop animation", 38, (255, 0, 0), self._cb_button_click_stop_animation)
        
        self.buttons.append(challengesButton)
        self.buttons.append(customizationButton) 
        self.buttons.append(stop_animation_button) 
        
        for b in self.buttons:
            self.add_child(b) 
    
    #### Callbacks ####    
    def _cb_button_click_challenges(self, button):
        self.cha_loader.get_challenge()
        self.windows_controller.set_active_window("challenges_window")
        
    def _cb_button_click_customization(self, button):
        self.windows_controller.set_active_window("customization_window")
        
    def _cb_button_click_stop_animation(self, button):
        self.panel_win.stop_animation()


class Clock(Widget):
    
    def __init__(self, container, rect_in_container, frame_rate):
        background = pygame.image.load("assets/layout/clock_background.png").convert_alpha()
        rect_in_container.size = background.get_size()
        Widget.__init__(self, container, rect_in_container, frame_rate)
        
        self.background = background
        self.frame_index = 0
        self.frame_paths = [
            "assets/layout/clock_A.png",
            "assets/layout/clock_B.png",
            "assets/layout/clock_C.png",
            "assets/layout/clock_D.png"
        ]
        
    def draw(self, screen):
        change = Widget.draw(self, screen)
        
        image = pygame.image.load(self.frame_paths[self.frame_index]).convert_alpha()
        rect = pygame.Rect((0, 0), image.get_size())
        rect.center = self.rect_absolute.center
        screen.blit(image, rect)
        self.frame_index += 1
        self.frame_index %= 4
        return change
        
