# -*- coding: utf-8 -*-
import menu_creator
import status_bars_creator
import actions_creator
import character_creator
import game_manager


class AppLoader:

    def __init__(self):
        ### loaders
        self.bars_loader = status_bars_creator.BarsLoader()
        
        actions_loader = actions_creator.ActionsLoader(self.bars_loader.get_bar_controller())

        ### actions 
        self.actions_list = actions_loader.get_actions_list() 
        
        ### status bars 
        self.status_bars_controller = self.bars_loader.get_bar_controller()
        self.character_bars = self.bars_loader.get_third_level_bars() #the third level status bars
             
        ### places
        character_loader = character_creator.CharacterLoader(self.actions_list, self.character_bars)
        self.places_dictionary = character_loader.get_places_dictionary()
        
        ### character
        self.character = character_loader.get_character()
        
        ### game manager
        self.game_man = game_manager.GameManager(self.character, self.status_bars_controller, self.actions_list, None)
        self.game_man.add_background_action("BARS_DEC") #acción de decrementar las barras
        
        ### menu
        #self.menu = menu_creator.load_menu(self.character, (100, 100))
        ### visuals
        
    
    def get_game_manager(self):
        return self.game_man
        
    def get_character(self):
        return self.character
    
    def get_status_bars_controller(self):
        return self.status_bars_controller
    
    def get_status_bars_loader(self):
        return self.bars_loader
    
    def get_menu(self):
        return self.menu
    
    def get_actions(self):
        return self.actions_dictionary



    
    
    






