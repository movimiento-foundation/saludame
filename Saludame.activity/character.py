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

import pygame
import utilities

# DEFAULT_MAPPINGS are used when creating a new character
DEFAULT_MAPPINGS = {
    "hair": (pygame.Color("#000000"), pygame.Color("#191919")),
    "skin": (pygame.Color("#ffccc7"), pygame.Color("#cba5a0")),
    "sweater": (pygame.Color("#00d69f"), pygame.Color("#00b07e")),
    "pants": (pygame.Color("#ff9900"), pygame.Color("#d37e00"), pygame.Color("#b06800"), pygame.Color("#b06800")),
    "shoes": (pygame.Color("#eeea00"), pygame.Color("#938200"))
}

class Character:
    
    def __init__(self, sex, name, level, score, clothes):
        
        self.sex = sex
        self.name = name
        self.level = level
        self.mood = "normal"
        
        # visuals
        self.convert_mappings(DEFAULT_MAPPINGS.copy())
        
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
        status = {
            "name": self.name,
            "gender": self.sex,
            "clothes": self.clothes,
            "character_colors": self.mappings, # add by CustomizatedKid in module customization.
            "current_place": self.current_place,
            "level": self.level,
            "grade": self.grade,
        }
        return status
    
    def load_properties(self, game_status):
        """
        Load the character properties from previous data
        """
        self.name = game_status["name"]
        self.sex = game_status["gender"]
        self.clothes = game_status["clothes"]
        self.convert_mappings(game_status["character_colors"])
        self.current_place = game_status["current_place"]
        self.level = game_status["level"]
        self.grade = game_status["grade"]
    
    def reset(self, gender=None):
        """
        Restore some character properties to its default values.
        """
        self.level = 1
        self.clothes = 'school'
        self.current_place = 'schoolyard'
        self.convert_mappings(DEFAULT_MAPPINGS.copy())
        if gender:
            self.sex = gender
        
    def convert_mappings(self, maps):
        for key in maps.keys():
            maps[key] = tuple( map(utilities.get_color_tuple, maps[key]) )
        
        self.mappings = maps

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
