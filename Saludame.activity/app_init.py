# -*- coding: utf-8 -*-
import menu_creator
import status_bars_creator
import actions_creator
import character_creator

class AppLoader:

    def __init__(self):
        """ loaders """
        actions_loader = actions_creator.ActionsLoader()
        bars_loader = status_bars_creator.BarsLoader()
        character_loader = character_creator.CharacterLoader()
        """          """
        """ actions """
        self.actions_dictionary = actions_loader.get_actions_dictionary() #diccionario {id_actions: Action}
        
        """ status bars """
        self.character_bars = bars_loader.get_third_level_bars() #the third level status bars
        
        """ places """
        self.places_dictionary = character_loader.get_places_dictionary()
        
        """ character """
        self.character = character_loader.get_character(self.actions_dictionary, self.character_bars)
        
        """ menu """
        self.menu = menu_creator.load_menu(self.character_manager)
        """ visuals """
    
        
    def get_character(self):
        return self.character
    
    def get_menu(self):
        return self.menu
    
    def get_actions(self):
        return self.actions_dictionary
    

    
    
    

