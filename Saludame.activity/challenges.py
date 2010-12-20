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
    
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, register_id, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, register_id, bg_color)     
        
        ###### Sounds ######
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        ####################
        
        self.choices = []
        self.correct = 0
        
        self.opportinities = 1
        
        self.challenges_creator = challenges_creator
        
        # If a question is setted, we have to "erase" the old challenge
        self.question = None
        
        self.win_points = 0
        self.lose_points = 0
        
        # Close Button
        self.btn_close = TextButton(self.rect, pygame.Rect((910, 0), (30, 30)), 1, "X", 32, (0, 0, 0), self._cb_button_click_close)
        self.buttons += [self.btn_close]       
        
        for b in self.buttons:
            self.add_child(b) 
        
        self.wait = 0
        
    ####### Set attributes #######
    def set_question(self, question):
        if (self.question):
            self.erase()
                
        self.question = TextBlock(self.rect, 30, 90, 1, question, TITLE_FONT_SIZE, (0, 0, 0), False)
        self.add_child(self.question)
        
    def set_correct_answer(self, a):
        self.correct = a
        
    def set_answers(self, answers):
        x = 30 
        y = self.question.rect_absolute.top  

        y += 40 * len(self.question.lines)
        
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
        
    ######## Callbacks buttons ########
    
    def _cb_button_click_choice(self, button):
        if(button == self.choices[self.correct]):
            self.s_correct.play()
            self.windows_controller.game_man.add_points(self.win_points)                  
            
            self.windows_controller.close_active_window()
            self.windows_controller.windows["info_challenge_window"].update_content(u"¡Respuesta correcta!", u"Muy bien, \nganaste %s puntos para tu barra %s" % (self.win_points, self.challenges_creator.game_man.get_lowest_bar().label))
            self.windows_controller.set_active_window("info_challenge_window") 
            self.opportinities = 1               
        else:
            self.windows_controller.game_man.add_points(-self.lose_points)
            self.s_incorrect.play()
            self.windows_controller.close_active_window()
                
            if (self.opportinities == 0):
                self.windows_controller.windows["info_challenge_window"].update_content(u"Perdiste", u"Qué lástima, no era correcta, \nperdiste %s puntos en tu barra de %s. \nLee la biblioteca o pregunta al maestro/a." % (self.lose_points, self.challenges_creator.game_man.get_lowest_bar().label))
                self.windows_controller.set_active_window("info_challenge_window")
                self.opportinities = 1
            else:                                            
                self.opportinities -= 1
                self.windows_controller.windows["info_challenge_window"].update_content(u"Respuseta incorrecta", u"La respuesta no esta correcta, intenta otra vez")
                self.windows_controller.set_active_window("mc_challenge_window")
                self.windows_controller.set_active_window("info_challenge_window")

        
    def _cb_button_over_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(MOUSE_OVER_COLOR)
            button.force_update()
            self.s_over.play()        
            
    def _cb_button_out_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(ANSWER_COLOR)
            button.force_update()      

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
        
class TrueOrFalse(MultipleChoice):
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, register_id, bg_color=(0, 0, 0)):
        
        MultipleChoice.__init__(self, container, rect, frame_rate, windows_controller, challenges_creator, register_id, bg_color)
        
        self.n_tf = N_TF 
        self.question_number = 0
        self.answers = ["waiting", "waiting", "waiting", "waiting", "waiting"]
        
        self.kind = "normal"    # normal or master
                                # master challenge is like a TrueOrFalse challenge with mutlitple choice questions 
                                
        self.limit = 3
        self.perdio = False
        
    def pre_draw(self, screen):
        if self.answers[0] == "waiting":
            q0 = pygame.draw.circle(screen, pygame.Color("grey"), (1020, 550), 10)
        elif self.answers[0] == "incorrect":
            q0 = pygame.draw.circle(screen, pygame.Color("red"), (1020, 550), 10)
        elif self.answers[0] == "correct":
            q0 = pygame.draw.circle(screen, pygame.Color("green"), (1020, 550), 10)
            
        if self.answers[1] == "waiting":
            q1 = pygame.draw.circle(screen, pygame.Color("grey"), (1050, 550), 10)
        elif self.answers[1] == "incorrect":
            q1 = pygame.draw.circle(screen, pygame.Color("red"), (1050, 550), 10)
        elif self.answers[1] == "correct":
            q1 = pygame.draw.circle(screen, pygame.Color("green"), (1050, 550), 10)
        
        
        if self.answers[2] == "waiting":
            q2 = pygame.draw.circle(screen, pygame.Color("grey"), (1080, 550), 10)
        elif self.answers[2] == "incorrect":
            q2 = pygame.draw.circle(screen, pygame.Color("red"), (1080, 550), 10)
        elif self.answers[2] == "correct":
            q2 = pygame.draw.circle(screen, pygame.Color("green"), (1080, 550), 10)
        
        
        if self.answers[3] == "waiting":
            q3 = pygame.draw.circle(screen, pygame.Color("grey"), (1110, 550), 10)
        elif self.answers[3] == "incorrect":
            q3 = pygame.draw.circle(screen, pygame.Color("red"), (1110, 550), 10)
        elif self.answers[3] == "correct":
            q3 = pygame.draw.circle(screen, pygame.Color("green"), (1110, 550), 10)
        
        
        if self.answers[4] == "waiting":
            q4 = pygame.draw.circle(screen, pygame.Color("grey"), (1140, 550), 10)
        elif self.answers[4] == "incorrect":
            q4 = pygame.draw.circle(screen, pygame.Color("red"), (1140, 550), 10)
        elif self.answers[4] == "correct":
            q4 = pygame.draw.circle(screen, pygame.Color("green"), (1140, 550), 10)
        
        
        return [q0, q1, q2, q3, q4]
        
    def _cb_button_click_choice(self, button):
        if(button == self.choices[self.correct]):
            self.s_correct.play()
            self.windows_controller.game_man.add_points(self.win_points)
            if self.n_tf:
                # Correct answer
                self.answers[self.question_number] = "correct"
                self.n_tf -= 1
                if self.kind == "master":                    
                    self.challenges_creator.get_challenge("master")
                elif self.kind == "normal":
                    self.challenges_creator.get_challenge("tf")
                self.question_number += 1
            else:
                self.windows_controller.close_active_window()
                self.result_and_reset()
        else:
            self.windows_controller.game_man.add_points(-self.lose_points)
            self.s_incorrect.play()
            if self.n_tf and not self.perdio:
                # Incorrect answer
                self.answers[self.question_number] = "incorrect"
                self.n_tf -= 1
                                
                if self.kind == "master":
                    if self.answers.count("incorrect") == 5 - self.limit:
                        self.perdio = True  
                    self.challenges_creator.get_challenge("master")
                    
                if self.kind == "normal":
                    self.challenges_creator.get_challenge("tf")
                self.question_number += 1
            else:
                self.windows_controller.close_active_window()
                self.result_and_reset()

    def result_and_reset(self):
        if self.kind == "normal":
            self.windows_controller.windows["info_challenge_window"].update_content(u"%s Respuestas correctas" % (self.answers.count("correct") + 1), u"Ganaste %s puntos para tu \nbarra %s" % ("[ver puntos]", self.challenges_creator.game_man.get_lowest_bar().label))
        if self.kind == "master":
            if self.perdio:
                self.windows_controller.windows["info_challenge_window"].update_content(u"Perdiste", u"Quedaste en este nivel. \n¡Hay que aprender más!")
            else:
                self.windows_controller.windows["info_challenge_window"].update_content(u"Ganaste", u"¡Pasaste de nivel! \nBusca las nuevas acciones en tu menú")
        self.windows_controller.set_active_window("info_challenge_window")
        
        self.n_tf = N_TF
        self.question_number = 0
        self.answers = ["waiting", "waiting", "waiting", "waiting", "waiting"]
        self.perdio = False
        
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()   
        self.n_tf = N_TF
        self.question_number = 0
        self.answers = ["waiting", "waiting", "waiting", "waiting", "waiting"]
        self.perdio = False
    
class InfoChallenge(Window):
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, text_intro, text_result_good, text_result_bad, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "info_challenge_window", bg_color)
             
        self.set_bg_image("assets/windows/window_2.png")
        self.challenges_creator = challenges_creator
        
        self.btn_continue = utilities.get_accept_button(self.rect, pygame.Rect((400, 500), (1, 1)), _("Continue"), self._cb_button_click_continue)
        self.add_button(self.btn_continue)
        
        # Texts
        self.title = utilities.Text(rect, 40, 40, 1, "Verdadero o Falso", 45, pygame.Color("blue"))
        self.text = utilities.TextBlock(rect, 40, 120, 1, "Texto de prueba", 35, pygame.Color("black"))
        self.image = utilities.Image(rect, pygame.Rect(640, 240, 80, 80), 1, "challenges/ninio_normal.png")
    
        self.add_child(self.title)
        self.add_child(self.text)
        self.add_child(self.image)
        
    def update_content(self, title="Verdadero o Falso", text="Texto de prueba", image="challenges/ninio_normal.png"):
        self.title.text = title
        self.title.refresh()
        self.text.parse_lines(text)
        self.image = image
        
    def _cb_button_click_continue(self, button):
        self.windows_controller.close_active_window()   
