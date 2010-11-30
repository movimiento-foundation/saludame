# -*- coding: utf-8 -*-

import actions

MAX_BAR_VALUE = 100.0 #maximo valor que puede alcanzar una barra
                      #necesario para el calculo de probabilidades

class Event:
    
    def __init__(self, picture, kid_animation_path, name, description, appereance_probability, time_span, kind, event_status, effect, kid_message, preferred_mood=9, message_time_span=5):
        self.appereance_probability = appereance_probability
        self.time_span = time_span
        self.time_left = time_span
        
        self.kid_animation_path = kid_animation_path
    
        # Messages at ballon
        self.kid_message = kid_message
        self.message_time_span = message_time_span
        
        self.event_status = event_status #instance EventStatusProbability
        
        self.preferred_mood = preferred_mood #set as normal by default
         
        self.picture = picture
        self.kind = kind
        
        self.name = name
        self.description = description
        
        self.effect = effect
        
        self.conditioned_bars = event_status
        
        self.conditioned_probability = 0 #se toma como cero la probabilidad inicial de cada evento
        
    def perform(self):
        if(self.time_left):
            self.effect.activate()
            self.time_left -= 1
    
    def reset(self):
        self.time_left = self.time_span
        
    def get_probability(self):
        #eventually we just take the conditioned
        #probability
        return int(self.conditioned_probability)
    
    def update_probability(self, bars_value_dic):
        """
        Updates event probability
        """
        
        prob = 0.0
        for bar_con in self.conditioned_bars:
            bar_id = bar_con[0]
            threshold = bar_con[2]
            max_prob = bar_con[3]
            
            bar_value = bars_value_dic[bar_id]

            if bar_con[1] == "direct":
                
                if bar_value > threshold:
                    prob += max_prob * ((bar_value - threshold) / (MAX_BAR_VALUE - threshold))
            elif bar_con[1] == "indirect":
                if bar_value < threshold:
                    prob += max_prob * ((threshold - bar_value) / threshold)
            elif bar_con[1] == "constant":
                if bar_value < threshold :
                    prob += max_prob
            self.conditioned_probability = prob
        return int(prob)
        
class EventStatusProbability:
    
    def __init__(self, conditioned_probability, direct_indirect):
        self.conditioned_probability = conditioned_probability
        self.direct_indirect = direct_indirect

