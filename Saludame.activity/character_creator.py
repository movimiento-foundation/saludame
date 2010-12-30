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
        self.environments_dictionary = self.__load_environments()
        self.places = self.__load_places()
        self.weather_effects = self.__load_weather_effects()
        
    def get_character(self):
        return self.character
    
    def get_environments_dictionary(self):
        return self.environments_dictionary
    
    def get_places(self):
        return self.places
    
    def get_weather_effects(self):
        return self.weather_effects
    
    def __load_character(self, sex, name, level, score, clothes):
        hair_color = [pygame.Color(color) for color in HAIR_COLOR]
        skin_color = [pygame.Color(color) for color in SKIN_COLOR]
        socks_color = [pygame.Color(color) for color in SOCKS_COLOR]
        shoes_color = [pygame.Color(color) for color in SHOES_COLOR]
        
        char = character.Character(sex, name, level, score, hair_color, socks_color, skin_color, shoes_color, clothes)
        return char
    
    def __load_weather_effects(self):
        weather_effects = {
                    # (clothes_id, weather_id, boolean indoor outdoor) : list of tuples [(id_bar, rate)]
                    #school clothes
                   ("school", "sunny", True) : [("fun", 1.0)],
                   ("school", "sunny", False) : [("physica", 1.0)],
                   ("school", "rainy", True) : [("physica", 1.0)],
                   ("school", "rainy", False) : [("physica", 1.0)],
                   ("school", "normal", True) : [("physica", 1.0)],
                   ("school", "normal", False) : [("physica", 1.0)],
                   ("school", "cold", True) : [("physica", 1.0)],
                   ("school", "cold", False) : [("physica", 1.0)],
                   #sunny clothes
                   ("sunny", "sunny", True) : [("physica", 1.0)],
                   ("sunny", "sunny", False) : [("physica", 1.0)],
                   ("sunny", "rainy", True) : [("physica", 1.0)],
                   ("sunny", "rainy", False) : [("physica", 1.0)],
                   ("sunny", "normal", True) : [("physica", 1.0)],
                   ("sunny", "normal", False) : [("physica", 1.0)],
                   ("sunny", "cold", True) : [("physica", 1.0)],
                   ("sunny", "cold", False) : [("physica", 1.0)],
                   #rainy clothes
                   ("rainy", "sunny", True) : [("physica", 1.0)],
                   ("rainy", "sunny", False) : [("physica", 1.0)],
                   ("rainy", "rainy", True) : [("physica", 1.0)],
                   ("rainy", "rainy", False) : [("physica", 1.0)],
                   ("rainy", "normal", True) : [("physica", 1.0)],
                   ("rainy", "normal", False) : [("physica", 1.0)],
                   ("rainy", "cold", True) : [("physica", 1.0)],
                   ("rainy", "cold", False) : [("physica", 1.0)],
                   }
        return weather_effects
    
    def __load_places(self):
        places = {  #schoolyard
                    "schoolyard" : {"outdoor": True},
                    #square
                    "square" : {"outdoor": True},
                    #classroom
                    "classroom" : {"outdoor": False},
                    #home
                    "home": {"outdoor": False},
                    #country
                    "country": {"outdoor": True}
                 }
        return places
    
    def __load_environments(self):
        environments = {#schoolyard
                        "schoolyard_sunny" : character.Environment("assets/background/schoolyard_sunny.png", "music_path"),
                        "schoolyard_rainy" : character.Environment("assets/background/schoolyard_rainy.png", "music_path"),
                        "schoolyard_normal" : character.Environment("assets/background/schoolyard_normal.png", "music_path"),
                        "schoolyard_cold" : character.Environment("assets/background/schoolyard_cold.png", "music_path"),
                        #square
                        "square_sunny" : character.Environment("assets/background/square_sunny.png", "music_path"),
                        "square_rainy" : character.Environment("assets/background/square_rainy.png", "music_path"),
                        "square_normal" : character.Environment("assets/background/square_normal.png", "music_path"),
                        "square_cold" : character.Environment("assets/background/square_cold.png", "music_path"),
                        #classroom
                        "classroom_sunny" : character.Environment("assets/background/classroom_sunny.png", "music_path"),
                        "classroom_rainy" : character.Environment("assets/background/classroom_rainy.png", "music_path"),
                        "classroom_normal" : character.Environment("assets/background/classroom_normal.png", "music_path"),
                        "classroom_cold" : character.Environment("assets/background/classroom_cold.png", "music_path"),
                        #home
                        "home_sunny" : character.Environment("assets/background/home_sunny.png", "music_path"),
                        "home_rainy" : character.Environment("assets/background/home_rainy.png", "music_path"),
                        "home_normal" : character.Environment("assets/background/home_normal.png", "music_path"),
                        "home_cold" : character.Environment("assets/background/home_cold.png", "music_path"),
                        #country
                        "country_sunny" : character.Environment("assets/background/country_sunny.png", "music_path"),
                        "country_rainy" : character.Environment("assets/background/country_rainy.png", "music_path"),
                        "country_normal" : character.Environment("assets/background/country_normal.png", "music_path"),
                        "country_cold" : character.Environment("assets/background/country_cold.png", "music_path"),
                        }
        
        return environments
