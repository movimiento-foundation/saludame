# -*- coding: utf-8 -*-

# Modulo de desafios

import pygame
import window
import os
from utilities import *

S_CORRECT_PATH = os.path.normpath("assets/sound/correct.ogg")
S_OVER_PATH = os.path.normpath("assets/sound/over.ogg")
S_INCORRECT_PATH = os.path.normpath("assets/sound/incorrect.ogg")
I_FRANCIA_PATH = os.path.normpath("assets/challenges/francia.jpg")

class MultipleChoice:
    
    def __init__(self, rect, frame_rate):
        self.rect = rect
        self.frame_rate = frame_rate
        
        self.background = pygame.image.load(I_FRANCIA_PATH).convert()
        
        self.question = Text(self.rect.left + 10, self.rect.top + 5, "Cual es la capital de Francia?")
        
        self.buttons = []
        self.buttons += [Choice(self.rect, 20, 40, 200, 20, "Buenos Aires")]
        self.buttons += [Choice(self.rect, 20, 70, 200, 20, "Oslo")]
        self.buttons += [Choice(self.rect, 20, 100, 200, 20, "Roma")]
        self.buttons += [Choice(self.rect, 20, 130, 200, 20, "Paris")]
        self.buttons += [Choice(self.rect, 20, 160, 200, 20, "Moscu")]   
        
        self.btn_view_answer = ViewAnswer(self.rect, 20, 200, 200, 20, "Me doy por vencido! :(...", self.buttons[3])
        self.buttons += [self.btn_view_answer]               
 
    def draw(self, screen):
        screen.fill((150, 150, 255), self.rect)
        screen.blit(self.background, (self.rect.right - 230, self.rect.top + 30))
        self.question.draw(screen)
        self.btn_view_answer.draw(screen)
        for button in self.buttons:
            button.draw(screen)
        return [self.rect]

class Choice(Button):
    def __init__(self, rect, x, y, w, h, text):
        Button.__init__(self, rect, x, y, w, h, text)
        self.s_correct = pygame.mixer.Sound(S_CORRECT_PATH)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.s_incorrect = pygame.mixer.Sound(S_INCORRECT_PATH)
        self.y = y 
        """
        Temporal para simular una respuesta correcta basandonos en la coordenada
        'y' del rectangulo que la contiene.
        """
        
    def on_mouse_click(self):
        if(self.y == 130):
            self.s_correct.play()
            return True # Damos por finalizada la pregunta
        else:
            self.s_incorrect.play()
        
    def on_mouse_over(self):
        self.s_over.play()
        self.set_background_color((0, 255, 0))
        
    def on_mouse_out(self):
        self.set_background_color((255, 0, 0))
        
class ViewAnswer(Button):
    def __init__(self, rect, x, y, w, h, text, resp):
        Button.__init__(self, rect, x, y, w, h, text)
        self.s_over = pygame.mixer.Sound(S_OVER_PATH)
        self.resp = resp
        self.set_background_color((20, 100, 45))
        
    def on_mouse_click(self):
        self.resp.set_background_color((0, 255, 255))
        return True # Damos por finalizada la pregunta
        
    def on_mouse_over(self):
        self.s_over.play()
        self.set_background_color((45, 255, 100))
        
    def on_mouse_out(self):
        self.set_background_color((20, 100, 45))
