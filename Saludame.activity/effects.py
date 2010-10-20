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
        for effect in self.effect_status_list:
            effect.activate()

class EffectStatus:
    """
    Abstract class ?
    """
    def __init__(self, increase_rate, bar_id, bar_controller):
        self.bar_id = bar_id
        self.increase_rate = increase_rate
        self.bar_controller = bar_controller
        
    def activate(self, status_bar):
        self.bar_controller.increase(self.bar_id, self.increase_rate) 
        
        
        
        

