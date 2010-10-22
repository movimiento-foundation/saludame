# -*- coding: utf-8 -*-

import actions
import pygame

        
class Character:
    
    def __init__(self, name, level, score, hair_color, socks_color, skin_color, shoes_color, status_bar_list, clothes):
        self.name = name
        self.level = level
        self.score = score
        
        # visuals
        self.hair_color = hair_color
        self.socks_color = socks_color
        self.skin_color = skin_color
        self.shoes_color = shoes_color
        self.clothes = clothes

        self.actual_place = None
        self.status_bar_list = status_bar_list #status bars
        self.active_events_list = []

        self.mood_list = [] #Class Mood instance's list
    
    def set_clothes(self, clothes):
        self.clothes = clothes
        
    def set_place(self, place_id):
        self.actual_place = place_id
        
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
            if(id == action_id):
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
        
        
        
        
        
        


