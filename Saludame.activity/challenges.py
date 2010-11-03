# -*- coding: utf-8 -*-

"""
Challenges module
"""

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
        Window.__init__(self, container, rect, frame_rate, windows_controller, "challenges_window", bg_color)     
        
        ###### Sounds ######
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        ####################
        
        self.choices = []
        self.correct = 0
        
        # If a question is setted, we have to "erase" the old challenge
        self.question = None
        
        # Control de preguntas largas (más de 1 línea)
        # Problema para decidir "donde" cortar la pregunta
        self.question_lines = 1;
        
        # Close Button
        self.btn_close = TextButton(self.rect, pygame.Rect((910, 0), (30, 30)), 1, "X", 32, (0, 0, 0), self._cb_button_click_close)
        self.buttons += [self.btn_close] 
        
        # Answer Button
        self.btn_view_answer = TextButton(self.rect, pygame.Rect(30, 350, 20, 20), 1, "Me doy por vencido! :(...", 30, (255, 20, 20), self._cb_button_click_answer, self._cb_button_over_answer, self._cb_button_out_answer)        
        self.buttons += [self.btn_view_answer]        
        
        for b in self.buttons:
            self.add_child(b) 
            
    ####### Set attributes #######
    def set_question(self, question):
        if (self.question):
            self.erase()
        self.question = Text(self.rect, 30, 30, 1, question, 40, (0, 0, 0))
        
        """
        Control de preguntas largas. Funciona bien y "relocaliza" las respuestas
        en función de la cantidad de líenas de la pregunta.
        Problema: "corta" la pregunta en un valor hardcodeado el
        cual muchas veces "corta" a una palabra en cualquier lado.
        """               
        if (self.question.rect_in_container.width > self.rect.width -20):
            q1 = Text(self.rect, 30, 30, 1, question[:43], 40, (0, 255, 0))
            q2 = Text(self.rect, 30, 65, 1, question[43:], 40, (0, 255, 0))
            self.add_child(q1)
            self.add_child(q2)
            self.question_lines = 2
            return
        
        self.question_lines = 1
        self.add_child(self.question)
        
    def set_correct_answer(self, a):
        self.correct = a
        
    def set_answers(self, answers):
        x = 35 
        y = 20       
        """
        Control de preguntas largas. Funciona bien y "relocaliza" las respuestas
        en función de la cantidad de líenas de la pregunta.
        Problema: "corta" la pregunta en un valor hardcodeado el
        cual muchas veces "corta" a una palabra en cualquier lado.
        """
        y += 40 * self.question_lines        
        for ans in answers:
            y += 30
            b = TextButton(self.rect, pygame.Rect((x, y), (1, 1)), 1, ans, 30, pygame.Color("blue"), self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)
            self.choices.append(b)
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
        if not FIN_MC:
            if(button == self.choices[self.correct]):
                self.s_correct.play()
                FIN_MC = True # Damos por finalizada la pregunta
            else:
                self.s_incorrect.play()
        
    def _cb_button_over_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(pygame.Color("green"))
            button.force_update()
            self.s_over.play()        
            
    def _cb_button_out_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(pygame.Color("blue"))
            button.force_update()
    
    def _cb_button_click_answer(self, button):
        global FIN_MC
        FIN_MC = True
        for c in self.choices:
            c.switch_color_text((10, 10, 10)) 
        (self.choices[self.correct]).switch_color_text((255, 0, 0))       
        
    def _cb_button_over_answer(self, button):
        if not FIN_MC:        
            self.s_over.play()
            
    def _cb_button_out_answer(self, button):
        pass
    
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
    
    ######## Others ########
    
    def erase(self):
        """
        Delete question and answers and repaint. Set FIN_MC false
        """
        self.choices = []
        self.widgets = [self.btn_close, self.btn_view_answer]
        self.buttons = [self.btn_close, self.btn_view_answer]
        self.repaint = True
        global FIN_MC
        FIN_MC = False
