# -*- coding: utf-8 -*-

import pygame

DEFAULT_MAPPINGS = {
    "hair": (pygame.Color("#000000"), pygame.Color("#191919")),
    "skin": (pygame.Color("#ffccc7"), pygame.Color("#cba5a0")),
    "socks": (pygame.Color("#fd8255"), pygame.Color("#db601f")),
    "shoes": (pygame.Color("#eeea00"), pygame.Color("#938200"))
}

class Character:
    
    def __init__(self, sex, name, level, score, hair_color, socks_color, skin_color, shoes_color, clothes):
        
        self.sex = sex
        self.name = name
        self.level = level
        self.mood = "normal"
        
        # visuals
        self.mappings = DEFAULT_MAPPINGS.copy()
        
        self.clothes = 'school'
        self.grade = 5

        self.current_place = 'schoolyard' #default place
    
    def set_clothes(self, clothes):
        self.clothes = clothes
        
    def set_place(self, place_id):
        self.current_place = place_id

    def get_status(self):
        """
        Get the character current status, and returns
        a dictionary.
        """
        status = {"character_colors" : self.mappings, # add by CustomizatedKid in module customization.
                  "current_place" : self.current_place,
                  "name" : self.name,
                  "level" : self.level,
                  "grade" : self.grade,
                  "clothes" : self.clothes
                  }
        return status
    
    def load_properties(self, game_status):
        """
        Load the character properties from previous data
        """
        #self.hair_color = game_status["hair_color"]
        #self.socks_color = game_status["socks_color"]
        #self.skin_color = game_status["skin_color"]
        #self.shoes_color = game_status["shoes_color"]
        self.mappings = game_status["character_colors"]
        self.name = game_status["name"]
        self.clothes = game_status["clothes"]
        self.grade = game_status["grade"]
        self.current_place = game_status["current_place"]
        self.level = game_status["level"]
    
    def reset(self):
        """
        Restore some character properties to its default values.
        """
        self.level = 1
        self.clothes = 'school'
        self.current_place = 'schoolyard'
        self.mappings = DEFAULT_MAPPINGS.copy()

class Environment:
    
    def __init__(self, background_path, background_music):
        self.background_path = background_path
        self.background_music = background_music
    
    def get_background_path(self):
        return self.background_path
    
    def get_background_music(self):
        return self.background_music
        
class Place:
    
    def __init__(self, place_id, background_path, background_music):
        self.id = place_id
        self.background_path = background_path
        self.background_music = background_music
        self.allowed_actions_list = [] #actions's ids
        
    def set_actions(self, actions_list):
        self.allowed_actions_list = actions_list
    
    def allowed_action(self, action_id):
        """
        Verify if the action is allowed in this place
        """
        for id in self.allowed_actions_list:
            if id == action_id:
                return True
        return False

class Weather:
    
    def __init__(self, weather_id, background_path, background_sound):
        self.weather_id = weather_id
        self.background_path = background_path
        self.background_sound = background_sound
        

class Clothes:
    
    def __init__(self, clothes_id, texture_path, weather_effects_list):
        self.clothes_id = clothes_id
        self.texture_path = texture_path
        self.weather_effects_list = weather_effects_list #list of tuples (id_weather, effect_indoor, effect_outdoor)
