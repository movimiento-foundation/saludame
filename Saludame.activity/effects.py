# -*- coding: utf-8 -*-

class Effect:
   
    def __init__(self):
        """
        Los effect_status son tuplas (id_barra, increase_rate)
        """
        self.effect_status_list = []
    
    def add_effect(self, effect_status):
        self.effect_status_list.append(effect_status)
        
    def activate(self):
        for effect_status in self.effect_status_list:
            effect_status.activate()
            
    def set_bar_controller(self, bar_controller):
        for effect_status in self.effect_status_list:
            effect_status.set_bar_controller(bar_controller)
        
        

class EffectStatus:
    """
    Abstract class ?
    """
    def __init__(self, increase_rate, bar_id, bar_controller):
        self.bar_id = bar_id
        self.increase_rate = increase_rate
        self.bar_controller = bar_controller
        
    def activate(self):
        self.bar_controller.increase_bar(self.bar_id, self.increase_rate) 
        
    def set_bar_controller(self, bar_controller):
        self.bar_controller = bar_controller
        
        
        


