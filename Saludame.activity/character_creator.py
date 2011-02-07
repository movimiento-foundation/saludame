# -*- coding: utf-8 -*-

# PATH

# PLACES
SCHOOL_WINDY_BACKGROUND_PATH = " "
SCHOOL_BACKGROUND_MUSIC = " "

# CLOTHES
SWEATER_TEXTURE = "  "

# CHARACTER
# estas constantes las definirná el usuario, y se cargaran en otro lado """
SEX = "boy"
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
    
    def __init__(self):
        self.character = self.__load_character(SEX, NAME, LEVEL, SCORE, "school")
        
    def get_character(self):
        return self.character
        
    def __load_character(self, sex, name, level, score, clothes):
        hair_color = [pygame.Color(color) for color in HAIR_COLOR]
        skin_color = [pygame.Color(color) for color in SKIN_COLOR]
        socks_color = [pygame.Color(color) for color in SOCKS_COLOR]
        shoes_color = [pygame.Color(color) for color in SHOES_COLOR]
        
        char = character.Character(sex, name, level, score, hair_color, socks_color, skin_color, shoes_color, clothes)
        return char

