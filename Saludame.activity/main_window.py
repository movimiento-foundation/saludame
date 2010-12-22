# -*- coding: utf-8 -*-

import pygame
from gettext import gettext as _

import utilities

from window import *
from panel_window import PanelWindow
from kid_window import KidWindow
import status_bars

class MainWindow(Window):
    
    def __init__(self, container, rect, frame_rate, clock, windows_controller, cha_loader, bars_loader, game_man):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "main_window")
        
        self.clock = clock
        self.cha_loader = cha_loader
        
        self.game_manager = game_man
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
           
        self.panel_win = PanelWindow(container, pygame.Rect((180, 609), (1015, 200)), 1, windows_controller)
        self.windows.append(self.panel_win)
        
        self.kidW = KidWindow(container, pygame.Rect((227, 0), (973, 609)), 1, windows_controller, game_man)
        self.windows.append(self.kidW)
        #self.windows.append(animation.Apple(pygame.Rect((700, 90), (150, 172)), 10))
        
        self.windows.append(animation.FPS(container, pygame.Rect((1150, 0), (50, 20)), 15, self.clock))
        self.windows.append(status_bars.BarsWindow(container, pygame.Rect(0, 0, 227, 590), 5, windows_controller, bars_loader))
        
        self.add_child(Clock(container, pygame.Rect(0, 528, 1, 1), 1, game_man))
        
        # Challenges
        
        challenges_button = ImageButton(self.rect, pygame.Rect((1120, 400), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_mc_challenges)
        challenges_button.set_tooltip(_("Multiple choice"))
        self.add_button(challenges_button)
        
        challenges_button2 = ImageButton(self.rect, pygame.Rect((1120, 500), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_tf_challenges)
        challenges_button2.set_tooltip(_("True or false"))
        self.add_button(challenges_button2)
        
        challenges_button3 = ImageButton(self.rect, pygame.Rect((1120, 300), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_master_challenge)
        challenges_button3.set_tooltip(_("Master challenge"))
        self.add_button(challenges_button3)
        
        challenges_button4 = ImageButton(self.rect, pygame.Rect((1120, 200), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_cooking_challenge)
        challenges_button4.set_tooltip(_("Cooking"))
        self.add_button(challenges_button4)
        
        button_back = pygame.image.load("customization/customization_button.png").convert_alpha()
        btn_reset = utilities.TextButton2(self.rect, pygame.Rect((1000, 20), (70, 30)), 1, _("Reset"), 30, (255, 255, 255), button_back, self._cb_reset_game)
        self.add_button(btn_reset)
        #stop_animation_button = TextButton(self.rect, pygame.Rect((800, 550), (30, 30)), 1, "Stop animation", 38, (255, 0, 0), self._cb_button_click_stop_animation)
        #self.add_button(stop_animation_button)
        
        #btn_change_mood = ImageButton(self.rect, pygame.Rect((1120, 500), (60, 60)), 1, "assets/icons/change.png", self._cb_button_click_change_mood)
        #self.add_button(btn_change_mood)
    
    #### Callbacks ####    
    def _cb_button_click_mc_challenges(self, button):
        self.cha_loader.get_challenge("mc")
        self.windows_controller.set_active_window("mc_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Múltiple Opción: %s" %(self.cha_loader.game_man.get_lowest_bar().label),  u"Tu barra de %s está baja. \nPara ganar puntos tienes que acertar \nla respuesta correcta. \n\n¡Suerte!" %(self.cha_loader.game_man.get_lowest_bar().label))
        self.windows_controller.set_active_window("info_challenge_window")
        
    def _cb_button_click_tf_challenges(self, button):
        self.cha_loader.get_challenge("tf")
        self.windows_controller.set_active_window("tf_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Verdadero o Flaso: %s" %(self.cha_loader.game_man.get_lowest_bar().label), u"Tu barra de %s está baja. \nPara ganar puntos tienes que acertar \nlas preguntas de verdero o falso. \n\n¡Suerte!" %(self.cha_loader.game_man.get_lowest_bar().label))
        self.windows_controller.set_active_window("info_challenge_window")
        
    def _cb_button_click_master_challenge(self, button):
        self.cha_loader.get_challenge("master")
        self.windows_controller.set_active_window("tf_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Super Desafío",  u"¡Estas por pasar de nivel! \nPara superarlo tienes que responder \ncorrecto a 3 de las 5 preguntas \nque siguen \n\n¡Suerte!")
        self.windows_controller.set_active_window("info_challenge_window")
        
    def _cb_button_click_cooking_challenge(self, button):
        self.windows_controller.set_active_window("cooking_challenge_window")
        
    def _cb_button_click_stop_animation(self, button):
        self.panel_win.stop_animation()
        
    def _cb_button_click_change_mood(self, button):
        self.kidW.change_mood()
    
    def _cb_reset_game(self, button):
        self.game_manager.reset_game()

class Clock(Widget):
    
    def __init__(self, container, rect_in_container, frame_rate, game_manager):
        background = pygame.image.load("assets/layout/clock_background.png").convert_alpha()
        rect_in_container.size = background.get_size()
        Widget.__init__(self, container, rect_in_container, frame_rate)
        
        self.game_manager = game_manager
        self.background = background
        self.frames = 0
        self.frame_index = 0
        self.frame_paths = [
            "assets/layout/clock_D.png",
            "assets/layout/clock_A.png",
            "assets/layout/clock_B.png",
            "assets/layout/clock_C.png",
        ]
        self.set_frame()
    
    def set_frame(self):
        self.frame = pygame.image.load(self.frame_paths[self.frame_index]).convert_alpha()
        
    def draw(self, screen):
        change = Widget.draw(self, screen)
        
        if self.game_manager.hour <> self.frame_index:
            self.frame_index = self.game_manager.hour
            self.set_frame()
        
        rect = pygame.Rect((0, 0), self.frame.get_size())
        rect.center = self.rect_absolute.center
        screen.blit(self.frame, rect)
        
        return change
        

