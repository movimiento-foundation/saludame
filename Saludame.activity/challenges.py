# -*- coding: utf-8 -*-

# Copyright (C) 2011 ceibalJAM! - ceibaljam.org
# This file is part of Saludame.
#
# Saludame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Saludame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Saludame. If not, see <http://www.gnu.org/licenses/>.

"""
Challenges module
"""

import pygame
import os
import gui
import utilities
import game_manager
import random
from gettext import gettext as _

S_CORRECT_PATH = os.path.normpath("assets/sound/challenge_win.ogg")
S_OVER_PATH = os.path.normpath("assets/sound/over.ogg")
S_INCORRECT_PATH = os.path.normpath("assets/sound/challenge_lose.ogg")

N_TF = 5

FIN_MC = False # Toma el valor True cuando finaliza el juego de multiple choice

QUESTION_FONT_SIZE = 24
TEXT_FONT_SIZE = 20
TEXT_TRUE_OR_FALSE_SIZE = 24

TITLE_COLOR = pygame.Color("#0f5e65")
TEXT_COLOR = pygame.Color("#0f5e65")
QUESTION_COLOR = pygame.Color("#0f5e65")
ANSWER_COLOR = pygame.Color("#1c9db4")
MOUSE_OVER_COLOR = pygame.Color("#0f5e65")

class MultipleChoice(gui.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, register_id, bg_color=(0, 0, 0)):
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, register_id, bg_color)
        
        self.set_bg_image("assets/windows/window_1.png")
        
        ###### Sounds ######
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        ####################
        
        self.topic = None # The topic is the bar whose we are playing
        
        self.choices = []
        self.correct = None
        self.correct_index = 0
        
        self.tries = 0
        
        self.challenges_creator = challenges_creator
        
        # If a question is setted, we have to "erase" the old challenge
        self.question = None
        
        self.title = gui.Text(self.rect, 30, 35, 1, u"Elije la opción correcta", 24, (255,255,255), bold=True)
        self.add_child(self.title)
        
        # Close Button
        self.btn_close = gui.TextButton(self.rect, pygame.Rect((910, 0), (30, 30)), 1, "X", 32, (0, 0, 0), self._cb_button_click_close)
        #self.add_button(self.btn_close)
        
        self.wait = 0
        
    ####### Set attributes #######
    def set_question(self, question):
        
        self.topic = self.challenges_creator.game_man.get_lowest_bar()
        
        if self.question:
            self.erase()
        
        question = self.prepare(question, 70)
        self.question = gui.TextBlock(self.rect, 30, 90, 1, question, QUESTION_FONT_SIZE, QUESTION_COLOR, "normal", False)
        self.add_child(self.question)
        
    def set_correct_answer(self, a):
        self.correct = a
        
    def set_answers(self, answers):
        x = 30
        y = self.question.rect_absolute.top

        y += 40 * len(self.question.lines)
        
        last_y = 30
        
        if isinstance(self, TrueOrFalse):
            if self.kind == "normal":
                size = TEXT_TRUE_OR_FALSE_SIZE
                
                for ans in answers:
                    ans = self.prepare(ans, 85)
                    y += last_y + 20
                    b = gui.TextBlockButton(self.rect, pygame.Rect((x, y), (1, 1)), 1, ans, size, ANSWER_COLOR, self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)
                    self.choices.append(b)
                    self.add_button(b)
                    last_y = b.rect_in_container.height
                return 
                                                    
            else:
                size = TEXT_FONT_SIZE
        else:
            size = TEXT_FONT_SIZE            
           
        # Choose 3 of the 5 possible incorrect answers
        cant_choose = []
        selected_answers = [answers[0]]
        for _ in range(3):
            
            ans = self.get_random_answer(answers[1:], cant_choose) # The first answer is the correct one
            selected_answers.append(ans)           
        
        random.shuffle(selected_answers)
        self.correct_index = selected_answers.index(self.correct)
        
        for ans in selected_answers:  
            ans = self.prepare(ans, 85)
            y += last_y + 20
            b = gui.TextBlockButton(self.rect, pygame.Rect((x, y), (1, 1)), 1, ans, size, ANSWER_COLOR, self._cb_button_click_choice, self._cb_button_over_choice, self._cb_button_out_choice)
            self.choices.append(b)
            self.add_button(b)
            last_y = b.rect_in_container.height
            
    def prepare(self, text, limit):
        if len(text) > limit:
            space = text[0:limit].rfind(" ")
            text = text[0:space] + "\n" + self.prepare(text[space + 1:], limit)
        return text
            
    def get_random_answer(self, answers, cant_choose):
        while True:
            r = random.randrange(0, 5)
            if not r in cant_choose:
                cant_choose.append(r)
                return answers[r]       
    
    def set_image(self, image):
        if  not isinstance(image, pygame.Surface):
            image = pygame.image.load(image)
        image = gui.Image(self.rect, pygame.Rect(500, 40, 20, 20), 1, image)
        self.add_child(image)
        
    ######## Callbacks buttons ########
    
    def _cb_button_click_choice(self, button):
        if button == self.choices[self.correct_index]:
            self.s_correct.play()
            self.windows_controller.game_man.bars_controller.increase_bar(self.topic.id, self.challenges_creator.game_man.get_current_level_conf()["multiple_choice_vector"][self.tries])
            
            self.windows_controller.close_active_window()
            self.windows_controller.windows["info_challenge_window"].update_content(u"¡Respuesta correcta!", u"Muy bien, \nganaste %s puntos para tu barra %s" % (self.challenges_creator.game_man.get_current_level_conf()["multiple_choice_vector"][self.tries], self.topic.label))
            self.windows_controller.set_active_window("info_challenge_window")
            self.tries = 0
        else:
            self.s_incorrect.play()
            self.windows_controller.close_active_window()
            
            if self.tries == 1:
                self.challenges_creator.game_man.bars_controller.increase_bar(self.topic.id, self.challenges_creator.game_man.get_current_level_conf()["multiple_choice_vector"][2])
                self.windows_controller.windows["info_challenge_window"].update_content(u"Perdiste", u"Qué lástima, no era correcta, \n %s puntos para tu barra de %s. \nLee la biblioteca o pregunta a tu maestro/a." % (self.challenges_creator.game_man.get_current_level_conf()["multiple_choice_vector"][2], self.topic.label), "assets/challenges/boy_sad.png")
                self.windows_controller.set_active_window("info_challenge_window")
                self.tries = 0
            else:
                self.tries += 1
                self.windows_controller.windows["info_challenge_window"].update_content(u"Respuesta incorrecta", u"La respuesta no es correcta, intenta otra vez")
                self.windows_controller.set_active_window("mc_challenge_window")
                self.windows_controller.set_active_window("info_challenge_window")

    def _cb_button_over_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(MOUSE_OVER_COLOR)
            self.s_over.play()
            
    def _cb_button_out_choice(self, button):
        if not FIN_MC:
            button.switch_color_text(ANSWER_COLOR)

    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
    
    ######## Others ########
    
    def erase(self):
        """
        Delete question and answers and repaint. Set FIN_MC false
        """
        self.choices = []
        self.clear_childs()
        #self.add_button(self.btn_close)
        self.add_child(self.title)
        self.set_dirty_background()
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
                                
        self.limit = game_manager.instance.get_current_level_conf()["min_qty_correct_ans"]
        
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
        
        if self.kind == "normal":
            correct = self.correct
        else:
            correct = self.correct_index
        
        if button == self.choices[correct]:
            self.s_correct.play()
            
            # Correct answer
            self.answers[self.question_number] = "correct"
            self.n_tf -= 1
            
            if self.n_tf > 0:
                if self.kind == "master":
                    self.challenges_creator.get_challenge("master")
                elif self.kind == "normal":
                    self.challenges_creator.get_challenge("tf")
                self.question_number += 1
            else:
                self.windows_controller.close_active_window()
                self.result_and_reset()
        else:
            self.s_incorrect.play()
            
            # Incorrect answer
            self.answers[self.question_number] = "incorrect"
            
            if self.kind == "master":
                self.windows_controller.game_man.add_points(-10)        # So it falls back to the previous level
                if self.answers.count("incorrect") == 5 - self.limit + 1:
                    self.perdio = True
            
            if self.perdio:
                self.windows_controller.close_active_window()
                self.result_and_reset()
                return            
            
            self.n_tf -= 1
            
            if self.n_tf > 0:
                                
                if self.kind == "master":
                    self.challenges_creator.get_challenge("master")
                    
                if self.kind == "normal":
                    self.challenges_creator.get_challenge("tf")
                self.question_number += 1
                
            else:
                self.windows_controller.close_active_window()
                self.result_and_reset()

    def result_and_reset(self):

        if self.kind == "normal":
             
            puntos = self.challenges_creator.game_man.get_current_level_conf()["true_or_false_vector"][self.answers.count("correct")]
            
            self.challenges_creator.game_man.bars_controller.increase_bar(self.topic.id, puntos)
            
            if puntos < 0:                
                self.windows_controller.windows["info_challenge_window"].update_content(u"%s Respuestas correctas" % (self.answers.count("correct")), u"Perdiste %s puntos para tu \nbarra %s" % (-puntos, self.topic.label), "assets/challenges/boy_sad.png")
            else:
                self.windows_controller.windows["info_challenge_window"].update_content(u"%s Respuestas correctas" % (self.answers.count("correct")), u"Ganaste %s puntos para tu \nbarra %s" % (puntos, self.topic.label))
            self.windows_controller.set_active_window("info_challenge_window")

            
        if self.kind == "master":
            if self.perdio:
                self.windows_controller.windows["info_challenge_window"].update_content(u"Perdiste", u"Quedaste en este nivel.\nRecuerda que puedes estudiar en la biblioteca.", "assets/challenges/boy_sad.png")
                self.windows_controller.set_active_window("info_challenge_window")
                game_manager.instance.previous_level()
                game_manager.instance.add_points(-9)
            else:                
                if not game_manager.instance.get_current_level_conf()["master_challenge_text"]:
                    if game_manager.instance.get_current_level_conf()["slide"]:
                        self.windows_controller.windows["slide_window"].show_slide(game_manager.instance.get_current_level_conf()["slide"])
                        self.windows_controller.set_active_window("slide_window")
                else:      
                    if game_manager.instance.get_current_level_conf()["slide"]:
                        self.windows_controller.windows["slide_window"].show_slide(game_manager.instance.get_current_level_conf()["slide"])
                        self.windows_controller.set_active_window("slide_window")
                    self.windows_controller.windows["info_challenge_window"].update_content(u"", self.challenges_creator.game_man.get_current_level_conf()["master_challenge_text"])
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
    
class InfoChallenge(gui.Window):
    def __init__(self, container, rect, frame_rate, windows_controller, challenges_creator, text_intro, text_result_good, text_result_bad, slide=None, bg_color=(0, 0, 0)):
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "info_challenge_window", bg_color)
             
        self.set_bg_image("assets/windows/window_2.png")
        self.challenges_creator = challenges_creator
        
        self.rect = rect
        
        self.btn_continue = utilities.get_accept_button(self.rect, pygame.Rect((400, 500), (1, 1)), _("Continue"), self._cb_button_click_continue)
        self.add_button(self.btn_continue)
        
        # Texts
        self.title = gui.Text(rect, 40, 40, 1, "Verdadero o Falso", 45, TITLE_COLOR)
        self.text = gui.TextBlock(rect, 40, 120, 1, "", 35, TEXT_COLOR, "normal", False)
        self.image = gui.Image(rect, pygame.Rect(640, 240, 80, 80), 1, "assets/challenges/ninio_normal.png")
    
        self.add_child(self.title)
        self.add_child(self.text)
        self.add_child(self.image)
        
    def update_content(self, title="Verdadero o Falso", text="", image="assets/challenges/ninio_normal.png"):
        self.title.text = title
        self.title.refresh()
        self.text.parse_lines(text)
        self.text.prepare_text_block()
        
        self.remove_child(self.image)
        self.image = gui.Image(self.rect, pygame.Rect(640, 240, 80, 80), 1, image)
        self.add_child(self.image)
        
    def _cb_button_click_continue(self, button):
        self.windows_controller.close_active_window()
        
class Slide(gui.Window):
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "slide_window")
        
        self.btn_continue = utilities.get_accept_button(self.rect, pygame.Rect((550, 700), (1, 1)), _("Continue"), self._cb_button_click_continue)
        self.add_button(self.btn_continue)        
    
    def show_slide(self, slide_path, close_callback=None):
        self.set_bg_image(slide_path)
        self.close_callback = close_callback
        
    def _cb_button_click_continue(self, button):
        self.windows_controller.close_active_window()
        if self.close_callback:
            self.close_callback()

#class Cooking(gui.Window):
    #def __init__(self, container, rect, frame_rate, windows_controller, register_id, bg_color=(0, 0, 0)):
        #gui.Window.__init__(self, container, rect, frame_rate, windows_controller, register_id, bg_color)
        
        #self.set_bg_image("assets/windows/window_1.png")
        
        ## Close Button
        #self.btn_close = gui.TextButton(self.rect, pygame.Rect((910, 0), (30, 30)), 1, "X", 32, (0, 0, 0), self._cb_button_click_close)
        #self.add_button(self.btn_close)
        
        ## Some widgets to test DnD
        #self.dnd = []
        #self.dnd.append(gui.Image(rect, pygame.Rect(50, 100, 100, 100), 1, "assets/events/ill.jpg"))
        #self.dnd.append(gui.Image(rect, pygame.Rect(50, 250, 100, 100), 1, "assets/events/caries.jpg"))
        #self.dnd.append(gui.Image(rect, pygame.Rect(50, 400, 100, 100), 1, "assets/events/unkown.png"))
        
        #self.trash = gui.Image(rect, pygame.Rect(500, 200, 200, 200), 1, "assets/challenges/trash.png")

        #for w in self.dnd:
            #self.add_child(w)
        #self.add_child(self.trash)
        
        ## Mouse mode (1 - left button pressed)
        #self.mouse_mode = 0
        
        #self.widget_selected = None
        
    #def handle_mouse_down(self, (x, y)):
        #gui.Window.handle_mouse_down(self, (x, y))
        #self.mouse_mode = 1
        
    #def handle_mouse_up(self, pos):
        #gui.Window.handle_mouse_up(self, pos)
        #for widget in self.dnd:
            #if self.trash.contains_point(widget.rect_absolute.centerx, widget.rect_absolute.centery):
                #self.remove_child(widget)
        #self.mouse_mode = 0
        #self.widget_selected = None
    
    #def handle_mouse_motion(self, pos):
        #if pos[0] < self.rect.right - 70 and pos[0] > self.rect.left + 70 and pos[1] < self.rect.bottom - 70 and pos[1] > self.rect.top + 120:
            #if self.mouse_mode == 1 and not self.widget_selected:
                #for widget in self.dnd:
                    #if widget.contains_point(pos[0], pos[1]):
                        #self.widget_selected = widget
                        #widget.rect_absolute.centerx = pos[0]
                        #widget.rect_absolute.centery = pos[1]
                        #self.repaint = True
            #elif self.mouse_mode == 1:
                #self.widget_selected.rect_absolute.centerx = pos[0]
                #self.widget_selected.rect_absolute.centery = pos[1]
                #self.repaint = True
        
    #def _cb_button_click_close(self, button):
        #self.windows_controller.close_active_window()
