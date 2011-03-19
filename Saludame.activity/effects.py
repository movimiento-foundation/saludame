# -*- coding: utf-8 -*-

class Effect:
    """
    Represents effects that affect directly on the status bars.
    """
   
    def __init__(self, bars_controller, effect_satatus_list, consequences=[]):
        """
        Los effect_status son tuplas (id_barra, increase_rate)
        """
        self.bars_controller = bars_controller
        self.effect_status_list = effect_satatus_list   # list of tuples (bar_id, increase_rate)
        self.consequences = consequences                # list of event_id that can trigger, only one with probability > 0 will be triggered
        
    def activate(self):
        for effect_status in self.effect_status_list:
            self.bars_controller.increase_bar(effect_status[0], effect_status[1])
            
    def set_bar_controller(self, bars_controller):
        self.bars_controller = bars_controller

    def get_consequence(self, events_dict, bars_value_dic):
        """ Iterates between the possible consequences and returns the first one with probability > 0 """
        for c in self.consequences:
            if c in events_dict:
                event = events_dict[c]
                event.update_probability(bars_value_dic)
                if event.get_probability() > 0:
                    return event
        
class LocationEffect:
    """
    Represents effects that set the character location.
    """
    
    def __init__(self, game_manager, place_id):
        self.game_manager = game_manager
        self.place_id = place_id
    
    def activate(self):
        self.game_manager.set_character_location(self.place_id)
    
    def set_game_manager(self, game_manager):
        self.game_manager = game_manager
        
    def get_consequence(self):
        return
        
class ClothesEffect:
    """
    Represents effects that set the character clothes.
    """
    
    def __init__(self, game_manager, clothes_id):
        self.game_manager = game_manager
        self.clothes_id = clothes_id
    
    def activate(self):
        self.game_manager.set_character_clothes(self.clothes_id)
    
    def set_game_manager(self, game_manager):
        self.game_manager = game_manager

    def get_consequence(self):
        return
