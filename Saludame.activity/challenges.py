# -*- coding: utf-8 -*-

# Modulo de desafios

import pygame
import os
from utilities import *

S_CORRECT_PATH = os.path.normpath("assets/sound/correct.ogg")
S_OVER_PATH = os.path.normpath("assets/sound/over.ogg")
S_INCORRECT_PATH = os.path.normpath("assets/sound/incorrect.ogg")
I_FRANCIA_PATH = os.path.normpath("assets/challenges/francia.jpg")

FIN_MC = False # Toma el valor True cuando finaliza el juego de multiple choice

class MultipleChoice:
    
    def __init__(self, rect, frame_rate):
        self.rect = rect
        self.frame_rate = frame_rate        
        self.background = pygame.image.load(I_FRANCIA_PATH).convert()
        
        self.question = Text(self.rect.left + 10, self.rect.top + 5, "Cual es la capital de Francia?", 20)
        
        # Boton cerrar
        self.btn_close = CloseButton(self.rect, 770, 5, 30, 30, "X")
                
        self.choices = []
        self.choices += [Choice(self.rect, 20, 40, 200, 20, "Buenos Aires")]
        self.choices += [Choice(self.rect, 20, 70, 200, 20, "Oslo")]
        self.choices += [Choice(self.rect, 20, 100, 200, 20, "Roma")]
        self.choices += [Choice(self.rect, 20, 130, 200, 20, "Paris")]
        self.choices += [Choice(self.rect, 20, 160, 200, 20, "Moscu")]   
        
        self.btn_view_answer = ViewAnswer(self.rect, 20, 200, 200, 20, "Me doy por vencido! :(...", self.choices[3])
        self.choices += [self.btn_view_answer]               
 
    def draw(self, screen):
        screen.fill((150, 150, 255), self.rect)
        screen.blit(self.background, (self.rect.right - 230, self.rect.top + 30))
        self.question.draw(screen)
        self.btn_close.draw(screen)
        self.btn_view_answer.draw(screen)
        for button in self.choices:
            button.draw(screen)
        return [self.rect]
    
    def handle_mouse_down(self, (x, y), windows_controller):
        global FIN_MC
        
        if (self.btn_close.contains_point(x, y)):
            self.btn_close.on_mouse_clik(windows_controller)
        
        else:        
            for choice in self.choices:
                if (choice.contains_point(x, y) and not FIN_MC):
                    fin = choice.on_mouse_click() # Fin representa el usuario ya contesto bien o se dio por vencido
                    if(fin): 
                        FIN_MC = fin
                        self.choices = [self.choices[3], self.choices[5]]
                        break # No tiene sentido seguir iterando sobre los botones si ya sabemos cual apreto
                
    def handle_mouse_over(self, (x, y)):
        for choice in self.choices:
            if (choice.contains_point(x, y)):
                if(not choice.over):
                    choice.on_mouse_over()
                    choice.over = True   
            else:
                choice.over = False
                choice.on_mouse_out()
                
    def get_windows(self):
        return [self]

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
