# -*- coding: utf-8 -*-

class Effect:
   
    def __init__(self, bars_controller, effect_satatus_list):
        """
        Los effect_status son tuplas (id_barra, increase_rate)
        """
        self.bars_controller = bars_controller
        self.effect_status_list = effect_satatus_list #list of tuples (bar_id, increase_rate)
    
    def add_effect(self, effect_status):
        self.effect_status_list.append(effect_status)
        
    def activate(self):
        for effect_status in self.effect_status_list:
            self.bars_controller.increase_bar(effect_status[0], effect_status[1])
            
    def set_bar_controller(self, bars_controller):
        self.bars_controller = bars_controller

        
        



