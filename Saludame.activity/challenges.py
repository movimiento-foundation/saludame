# -*- coding: utf-8 -*-

# Modulo de desafios

import pygame
import os
from utilities import *
from window import *

S_CORRECT_PATH = os.path.normpath("assets/sound/correct.ogg")
S_OVER_PATH = os.path.normpath("assets/sound/over.ogg")
S_INCORRECT_PATH = os.path.normpath("assets/sound/incorrect.ogg")
I_FRANCIA_PATH = os.path.normpath("assets/challenges/francia.jpg")

FIN_MC = False # Toma el valor True cuando finaliza el juego de multiple choice

class MultipleChoice(Window):
    
    def __init__(self, rect, frame_rate, background, screen, windows_controller):
        Window.__init__(self, rect, frame_rate, background, screen, windows_controller)     
        
        ###### Images ######    
        self.image = pygame.image.load(I_FRANCIA_PATH).convert()
        ####################
        
        ###### Sounds ######
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        ####################
        
        # Question
        self.question = Text(self.rect, 5, 5, 1, "Cual es la capital de Francia?", 40, (0, 255, 0))
        self.widgets.append(self.question)
        
        # Close Button
        self.btn_close = TextButton(self.rect, pygame.Rect((770, 5), (30, 30)), 1, "X", 30, (0, 0, 0), self._cb_button_click_close)
        self.buttons += [self.btn_close] 
        
        ###### Choices ######      
        self.buttons += [TextButton(self.rect, pygame.Rect((20, 40), (200, 20)), 1, "Buenos Aires", 30, (255, 255, 255), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)]
        self.buttons += [TextButton(self.rect, pygame.Rect((20, 70), (200, 20)), 1, "Oslo", 30, (255, 255, 255), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)]
        self.buttons += [TextButton(self.rect, pygame.Rect((20, 100), (200, 20)), 1, "Roma", 30, (255, 255, 255), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)]
        self.buttons += [TextButton(self.rect, pygame.Rect((20, 130), (200, 20)), 1, "Paris", 30, (255, 255, 255), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)]
        self.buttons += [TextButton(self.rect, pygame.Rect((20, 160), (200, 20)), 1, "Moscu", 30, (255, 255, 255), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)]   
        
        # Answer Button
        self.btn_view_answer = TextButton(self.rect, pygame.Rect(20, 200, 20, 20), 1, "Me doy por vencido! :(...", 30, (255, 20, 20), self._cb_button_click_answer, self._cb_button_over_answer, self._cb_button_out_answer)        
        self.buttons += [self.btn_view_answer]        

        france_image = Image(self.rect, pygame.Rect(500, 40, 20, 20), 1, self.image)
        self.widgets.append(france_image)    
    
    def _cb_button_click_choice(self, button):
        global FIN_MC
        if(button.rect.top == 130):
            self.s_correct.play()
            FIN_MC = True # Damos por finalizada la pregunta
        else:
            self.s_incorrect.play()
        
    def _cb_button_over_choice(self, button):
        button.switch_color_text((255, 0, 0))
        button.force_update(self.screen)
        self.s_over.play()        
            
    def _cb_button_out_choice(self, button):
        button.switch_color_text((255, 255, 255))
        button.force_update(self.screen)
    
    def _cb_button_click_answer(self, button):
        global FIN_MC
        FIN_MC = True
        
    def _cb_button_over_answer(self, button):        
        self.s_over.play()
            
    def _cb_button_out_answer(self, button):
        pass
    
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
