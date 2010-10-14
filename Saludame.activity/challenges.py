# -*- coding: utf-8 -*-

# Modulo de desafios

import pygame
import os
from utilities import *
from window import *

S_CORRECT_PATH = os.path.normpath("assets/sound/correct.ogg")
S_OVER_PATH = os.path.normpath("assets/sound/over.ogg")
S_INCORRECT_PATH = os.path.normpath("assets/sound/incorrect.ogg")

FIN_MC = False # Toma el valor True cuando finaliza el juego de multiple choice

class MultipleChoice(Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)     
        
        ###### Sounds ######
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        ####################
        
        # Close Button
        self.btn_close = TextButton(self.rect, pygame.Rect((770, 5), (30, 30)), 1, "X", 30, (0, 0, 0), self._cb_button_click_close)
        self.buttons += [self.btn_close] 
        
        # Answer Button
        self.btn_view_answer = TextButton(self.rect, pygame.Rect(20, 350, 20, 20), 1, "Me doy por vencido! :(...", 30, (255, 20, 20), self._cb_button_click_answer, self._cb_button_over_answer, self._cb_button_out_answer)        
        self.buttons += [self.btn_view_answer]        
        
        for b in self.buttons:
            self.add_child(b) 
            
    ####### Set attributes #######
    def set_question(self, question):
        self.question = Text(self.rect, 5, 5, 1, question, 40, (0, 255, 0))
        self.add_child(self.question)
        
    def set_correct_answer(self, a):
        pass
        
    def set_answers(self, answers):
        x = 20
        y = 10        
        width = 200 
        height = 20
        for ans in answers:
            y += 30
            b = TextButton(self.rect, pygame.Rect((x, y), (width, height)), 1, ans, 30, (255, 255, 255), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)
            self.buttons.append(b)
            self.add_child(b)
            
        
    
    def set_image(self, image):
        if (not isinstance(image, pygame.Surface)):
            image = pygame.image.load(image)
        image = Image(self.rect, pygame.Rect(500, 40, 20, 20), 1, image)
        self.add_child(image)
    
    ######## Callbacks buttons ########
    
    def _cb_button_click_choice(self, button):
        global FIN_MC
        if(button.rect_in_container.top == 130):
            self.s_correct.play()
            FIN_MC = True # Damos por finalizada la pregunta
        else:
            self.s_incorrect.play()
        
    def _cb_button_over_choice(self, button):
        button.switch_color_text((255, 0, 0))
        button.force_update()
        self.s_over.play()        
            
    def _cb_button_out_choice(self, button):
        button.switch_color_text((255, 255, 255))
        button.force_update()
    
    def _cb_button_click_answer(self, button):
        global FIN_MC
        FIN_MC = True
        
    def _cb_button_over_answer(self, button):        
        self.s_over.play()
            
    def _cb_button_out_answer(self, button):
        pass
    
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
        
    ########################################
