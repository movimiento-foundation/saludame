# -*- coding: utf-8 -*-

import actions

class CharacterManager:
    
    def __init__(self, character, actions_dictionary, places_dictionary):
        self.character = character
        self.actions_dictionary = actions_dictionary
        self.places_dictionary = places_dictionary
    
    def set_character_place(self, place_id):
        self.character.set_place(place_id)
    
    def action_perform(self, action_id):
        place = self.places_dictionary[self.character.actual_place] #lugar donde se ecuentra el kid actualmente
        if(place.allowed_action(action_id)):#continúa con la acción, solo si es permitida en el lugar
            action = self.actions_dictionary[action_id]
            action.perform()
        
class Character:
    
    def __init__(self, name, level, score, hair_color, eyes_color, skin_color, shoes_color, status_bar_list):
        self.name = name
        self.level = level
        self.score = score
        
        """ visuals """
        self.hair_color = hair_color
        self.eyes_color = eyes_color
        self.skin_color = skin_color
        self.shoes_color = shoes_color
        """ """
        
        self.actual_place = None
        self.status_bar_list = status_bar_list #status bars
        self.active_events_list = []

        self.mood_list = [] #Class Mood instance's list
        
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
