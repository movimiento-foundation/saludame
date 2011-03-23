# -*- coding: utf-8 -*-

MAX_BAR_VALUE = 100.0 #maximo valor que puede alcanzar una barra
                      #necesario para el calculo de probabilidades

class Event:
    
    def __init__(self, directory_path, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, level, preferred_mood):
        
        if not time_span:
            time_span = 999
        
        self.directory_path = directory_path
        self.name = name
        self.description = description
        
        self.impact = impact
        self.preferred_mood = preferred_mood
        
        self.appereance_probability = appereance_probability
        self.time_span = time_span
        self.time_left = time_span

        self.effect = effect
        
        self.operator = conditioned_bars[0]
        self.condicioned_bars = conditioned_bars[1]
        self.condicioned_probability = 0.0 # starts in 0.0
        self.level = level      # Starting level, in levels prior to this one, the event is not triggered
    
    def update_probability(self, bars_value_dic):
        """
        Updates event probability
        """
        prob = 0.0
        for bar_con in self.condicioned_bars:
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
            self.condicioned_probability = prob
        return int(prob)
    
    def get_probability(self):
        #eventually we just take the conditioned
        #probability
        return int(self.condicioned_probability)
        
        
    def perform(self):
        if self.time_left:
            if self.effect:
                self.effect.activate(1)
            self.time_left -= 1
    
    def reset(self):
        self.time_left = self.time_span
    
    
class PersonalEvent(Event):
    
    def __init__(self, picture, kid_animation_path, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, kid_message, level=1, preferred_mood=9, message_time_span=5):
        Event.__init__(self, picture, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, level, preferred_mood)
        
        self.kid_animation_path = kid_animation_path
    
        # Messages at ballon
        self.kid_message = kid_message
        self.message_time_span = message_time_span
    
    
class SocialEvent(Event):
    
    def __init__(self, picture, person_path, name, description, impact, appereance_probability, time_span, conditioned_bars, message, effect, level=1, preferred_mood=9, message_time_span=5):
        Event.__init__(self, picture, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, level, preferred_mood)
        
        self.time_left = time_span
        
        self.person_path = person_path
        self.person_message = message
        self.message_time_span = message_time_span

