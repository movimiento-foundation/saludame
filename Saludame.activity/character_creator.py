# -*- coding: utf-8 -*-

""" PATH """

""" PLACES """
SCHOOL_WINDY_BACKGROUND_PATH = " "
SCHOOL_BACKGROUND_MUSIC = " "

""" CLOTHES """
SWEATER_TEXTURE = "  "

""" CHARACTER """
""" estas constantes las definirná el usuario, y se cargaran en otro lado """
NAME = "José"
SCORE = 0
LEVEL = 1

"""  CHACTER APPEARENCE   """
EYES_COLOR = "blue"
HAIR_COLOR = "black"
SKIN_COLOR = "white" 
SHOES_COLOR = "green"
"""      """

import character
import pygame


class CharacterLoader:
    
    def __init__(self, actions_dictionary, status_bar_list):
        self.actions_dictionary = actions_dictionary
        self.status_bar_list = status_bar_list
        self.places_dictionary = self.__load_places()
        self.clothes_list = self.__load_clothes()
        self.character = self.__load_character(NAME, LEVEL, SCORE, self.actions_dictionary, self.places_dictionary, status_bar_list, self.clothes_list[0])
        
        
    def get_character(self):
        return self.character
        
    def get_places_dictionary(self):
        return self.places_dictionary
    
    def __load_clothes(self):
        None
    
    def __load_character(self, name, level, score, actions_dictionary, places_dictionary, status_bar_list, clothes):
        eyes_color = pygame.Color(EYES_COLOR)
        shoes_color = pygame.Color(SHOES_COLOR)
        hair_color = pygame.Color(HAIR_COLOR)
        skin_color = pygame.Color(SKIN_COLOR)
        
        character = character.Character(name, level, score, hair_color, eyes_color, skin_color, shoes_color, status_bar_list, clothes, places_dictionary, actions_dictionary)
        return character
        
    def __load_places(self):
        """ school  """
        
        """ home """
        None
        
        
        


