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

import character
import pygame

class CharacterLoader:
    
    def __init__(self):
        self.character = self.__load_character(SEX, NAME, LEVEL, SCORE, "school")
        
    def get_character(self):
        return self.character
        
    def __load_character(self, sex, name, level, score, clothes):
        return character.Character(sex, name, level, score, clothes)
