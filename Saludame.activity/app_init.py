# -*- coding: utf-8 -*-
import menu_creator
import status_bars_creator
import actions_creator
import character_creator
import game_manager
import events
import effects


class AppLoader:

    def __init__(self, windows_controller):
        ### loaders
        self.bars_loader = status_bars_creator.BarsLoader()
        
        actions_loader = actions_creator.ActionsLoader(self.bars_loader.get_bar_controller())

        ### actions 
        self.actions_list = actions_loader.get_actions_list() 
        
        ### status bars 
        self.status_bars_controller = self.bars_loader.get_bar_controller()
        self.character_bars = self.bars_loader.get_third_level_bars() #the third level status bars
        
        ### events
        self.events_list = self.__load_events(self.status_bars_controller)
        ### places
        character_loader = character_creator.CharacterLoader(self.actions_list, self.character_bars)
        self.places_dictionary = character_loader.get_places_dictionary()
        
        ### character
        self.character = character_loader.get_character()
        
        ### game manager
        self.game_man = game_manager.GameManager(self.character, self.status_bars_controller, self.actions_list, self.events_list, None, windows_controller)
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
        return self.actions_list
    
    def get_events(self):
        return self.events_list

    
    def __load_events(self, bars_controller):
        #(self, picture, name, appereance_probability, time_span, kind, event_status, effect)
        #temporal para testear eventos
        dec = -1.0
        inc = 1.0
        ef1 = effects.Effect(bars_controller, [("nutrition", dec), ("physica", dec), ("hygiene", dec), ("fun", dec)])
        ef2 = effects.Effect(bars_controller, [("nutrition", inc), ("physica", inc), ("hygiene", inc), ("fun", inc)])
        ef3 = effects.Effect(bars_controller, [("fun", 5.0)])
        ef4 = effects.Effect(bars_controller, [("nutrition", 5.0)])
        
        event_dec = events.Event("picture_path", "decremento", 4, 5, "kind", None, ef1)
        event_inc = events.Event("picture_path", "incremento", 6, 5, "kind", None, ef2)
        event_ill = events.Event("ill.jpg", "ill", 5, 5, "kind", None, ef3)
        event_caries = events.Event("caries.jpg", "caries", 8, 5, "kind", None, ef4)
        
        return [event_ill, event_caries]
    
    