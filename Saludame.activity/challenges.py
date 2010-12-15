# -*- coding: utf-8 -*-

"""
Challenges module
"""

import pygame
import os
from utilities import *
from window import *
from gettext import gettext as _

S_CORRECT_PATH = os.path.normpath("assets/sound/correct.ogg")
S_OVER_PATH = os.path.normpath("assets/sound/over.ogg")
S_INCORRECT_PATH = os.path.normpath("assets/sound/incorrect.ogg")

N_TF = 4

FIN_MC = False # Toma el valor True cuando finaliza el juego de multiple choice

TITLE_FONT_SIZE = 24
TEXT_FONT_SIZE = 18

ANSWER_COLOR = pygame.Color("blue")
MOUSE_OVER_COLOR = pygame.Color("green")

class MultipleChoice(Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "challenges_window", bg_color)     
        
        ###### Sounds ######
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        ####################
        
        self.choices = []
        self.correct = 0
        
        self.kind = "mc"
        self.n_tf = N_TF
        
        self.challenges_creator = challenges_creator
        
        # If a question is setted, we have to "erase" the old challenge
        self.question = None
        
        self.win_points = 0
        self.lose_points = 0
        
        # Control de preguntas largas (más de 1 línea)
        # Problema para decidir "donde" cortar la pregunta
        self.question_lines = 1;
        
        # Close Button
        self.btn_close = TextButton(self.rect, pygame.Rect((910, 0), (30, 30)), 1, "X", 32, (0, 0, 0), self._cb_button_click_close)
        self.buttons += [self.btn_close] 
        
        # Answer Button
        #self.btn_view_answer = TextButton(self.rect, pygame.Rect(30, 350, 20, 20), 1, "Me doy por vencido! :(...", TEXT_FONT_SIZE, (255, 20, 20), self._cb_button_click_answer, self._cb_button_over_answer, self._cb_button_out_answer)        
        #self.buttons += [self.btn_view_answer]        
        
        for b in self.buttons:
            self.add_child(b) 
        
        self.wait = 0
        
    ####### Set attributes #######
    def set_question(self, question):
        if (self.question):
            self.erase()
        self.question = Text(self.rect, 30, 30, 1, question, TITLE_FONT_SIZE, (0, 0, 0))
        
        """
        Control de preguntas largas. Funciona bien y "relocaliza" las respuestas
        en función de la cantidad de líenas de la pregunta.
        Problema: "corta" la pregunta en un valor hardcodeado el
        cual muchas veces "corta" a una palabra en cualquier lado.
        """               
        if (self.question.rect_in_container.width > self.rect.width - 20):
            q1 = Text(self.rect, 30, 30, 1, question[:43], TITLE_FONT_SIZE, (0, 0, 0))
            q2 = Text(self.rect, 30, 65, 1, question[43:], TITLE_FONT_SIZE, (0, 0, 0))
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
            b = TextButton(self.rect, pygame.Rect((x, y), (1, 1)), 1, ans, TEXT_FONT_SIZE, ANSWER_COLOR, self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)
            self.choices.append(b)
            self.buttons.append(b)
            self.add_child(b)        
    
    def set_image(self, image):
        if (not isinstance(image, pygame.Surface)):
            image = pygame.image.load(image)
        image = Image(self.rect, pygame.Rect(500, 40, 20, 20), 1, image)
        self.add_child(image)
    
    def set_win_points(self, points):
        self.win_points = points
    
    def set_lose_points(self, points):
        self.lose_points = points
    
    def pre_draw(self, screen):
        """
        if FIN_MC:
            self.wait += 1
        
        if self.wait >= 20:
            self.windows_controller.close_active_window()
        """
        if FIN_MC:
            self.windows_controller.close_active_window()
        return []
        
    ######## Callbacks buttons ########
    
    def _cb_button_click_choice(self, button):
        global FIN_MC
        if not FIN_MC:
            if(button == self.choices[self.correct]):
                self.s_correct.play()
                self.windows_controller.game_man.add_points(self.win_points)
                if self.kind == "tf":
                    if self.n_tf:
                        self.n_tf -= 1
                        self.challenges_creator.get_challenge("tf")
                    else:
                        FIN_MC = True # Damos por finalizado el desafío
                        self.n_tf = N_TF
                else:                    
                    FIN_MC = True # Damos por finalizado el desafío
                    self.windows_controller.show_master_challenge_result_good()
            else:
                self.windows_controller.game_man.add_points(-self.lose_points)
                self.s_incorrect.play()
                if self.kind == "mc":
                    FIN_MC = True
                    self.windows_controller.show_master_challenge_result_bad()                
        
    def _cb_button_over_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(MOUSE_OVER_COLOR)
            button.force_update()
            self.s_over.play()        
            
    def _cb_button_out_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(ANSWER_COLOR)
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
        self.widgets = [self.btn_close] #, self.btn_view_answer]
        self.buttons = [self.btn_close] #, self.btn_view_answer]
        self.repaint = True
        self.wait = 0
        global FIN_MC
        FIN_MC = False
        
class InfoMasterChallenge(Window):
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, text_intro, text_result_good, text_result_bad, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "info_master_challenge", bg_color)
             
        self.set_bg_image("assets/windows/window_2.png")
        self.challenges_creator = challenges_creator
        
        self.btn_continue = utilities.get_accept_button(self.rect, pygame.Rect((400, 500), (1, 1)), _("Continue"), self._cb_button_click_continue)
        self.add_button(self.btn_continue)
        
        self.text_intro = utilities.TextBlock(rect, 40, 60, 1, text_intro, 35, pygame.Color("blue"))
        self.text_result_good = utilities.TextBlock(rect, 40, 60, 1, text_result_good, 35, pygame.Color("blue"))
        self.text_result_bad = utilities.TextBlock(rect, 40, 60, 1, text_result_bad, 35, pygame.Color("blue"))
        
        self.add_child(self.text_intro)
        self.add_child(self.text_result_good)
        self.add_child(self.text_result_bad)
        
    def show_intro(self):
        self.text_intro.visible = True
        self.text_result_good.visible = False
        self.text_result_bad.visible = False
        
    def show_result_good(self):
        self.text_intro.visible = False
        self.text_result_good.visible = True
        self.text_result_bad.visible = False
        
    def show_result_bad(self):
        self.text_intro.visible = False
        self.text_result_good.visible = False
        self.text_result_bad.visible = True
        
    def _cb_button_click_continue(self, button):
        self.windows_controller.close_active_window()
                
        if self.text_intro.visible:
            self.challenges_creator.get_challenge("mc")
            self.windows_controller.set_active_window("challenges_window")
        
