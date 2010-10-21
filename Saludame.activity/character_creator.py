# -*- coding: utf-8 -*-

# PATH

# PLACES
SCHOOL_WINDY_BACKGROUND_PATH = " "
SCHOOL_BACKGROUND_MUSIC = " "

# CLOTHES
SWEATER_TEXTURE = "  "

# CHARACTER
# estas constantes las definirná el usuario, y se cargaran en otro lado """
NAME = "José"
SCORE = 0
LEVEL = 1

# CHACTER APPEARENCE
HAIR_COLOR = ("#000000", "#191919")
SKIN_COLOR = ("#ffccc7", "#f3b9b6")
SOCKS_COLOR = ("#fd8255", "#db601f")
SHOES_COLOR = ("#eeea00", "#938200")

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
        return ["a clothes"]
    
    def __load_character(self, name, level, score, actions_dictionary, places_dictionary, status_bar_list, clothes):
        hair_color = [pygame.Color(color) for color in HAIR_COLOR]
        skin_color = [pygame.Color(color) for color in SKIN_COLOR]
        socks_color = [pygame.Color(color) for color in SOCKS_COLOR]
        shoes_color = [pygame.Color(color) for color in SHOES_COLOR]
        
        char = character.Character(name, level, score, hair_color, socks_color, skin_color, shoes_color, status_bar_list, clothes, places_dictionary, actions_dictionary)
        return char
        
    def __load_places(self):
        # school
        
        # home
        None
        
