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

class Effect:
    """
    Represents effects that affect directly on the status bars.
    """
   
    def __init__(self, effect_satatus_list, consequences=[], change_time=False):
        """
        Los effect_status son tuplas (id_barra, increase_rate)
        """
        self.effect_status_list = effect_satatus_list   # list of tuples (bar_id, increase_rate)
        self.consequences = consequences                # list of event_id that can trigger, only one with probability > 0 will be triggered
        self.change_time = change_time
        
    def activate(self, factor):
        for bar_id, increase_rate in self.effect_status_list:
            self.bars_controller.increase_bar(bar_id, increase_rate * factor)
            
    def set_bar_controller(self, bars_controller):
        self.bars_controller = bars_controller

    def set_change_time(self, change):
        self.change_time = change
    
    def get_change_time(self):
        return self.change_time
    
    def get_consequence(self, events_dict, bars_value_dic, restrictions):
        """ Iterates between the possible consequences and returns the first one with probability > 0 """
        for c in self.consequences:
            if c in events_dict:
                event = events_dict[c]
                event.update_probability(bars_value_dic, restrictions, True)
                if event.get_probability() > 0:
                    return event

    def get_new_place(self):
        return None

    def get_new_clothes(self):
        return None


class LocationEffect(Effect):
    """
    Represents effects that set the character location.
    """
    
    def __init__(self, place_id):
        Effect.__init__(self, [])
        self.place_id = place_id
    
    def get_new_place(self):
        return self.place_id


class ClothesEffect(Effect):
    """
    Represents effects that set the character clothes.
    """
    
    def __init__(self, clothes_id):
        Effect.__init__(self, [])
        self.clothes_id = clothes_id

    def get_new_clothes(self):
        return self.clothes_id
