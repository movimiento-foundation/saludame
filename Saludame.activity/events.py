# -*- coding: utf-8 -*-

MAX_BAR_VALUE = 100.0 #maximo valor que puede alcanzar una barra
                      #necesario para el calculo de probabilidades

class Event:
    
    def __init__(self, directory_path, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, library_link, level, preferred_mood):
        
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

        self.library_link = library_link
        
        self.restrictions = {}
    
    def check_restrictions(self, restrictions):
        for restriction_id, values in self.restrictions.items():
            value = restrictions[restriction_id]
            if not value in values:
                return False
        return True
        
    def update_probability(self, bars_value_dic, restrictions, triggered = False):
        """
        Updates event probability
        """
        
        self.condicioned_probability = 0.0
        
        if not self.check_restrictions(restrictions):
            return 0.0
            
        probs = []
        
        if self.condicioned_bars:
            
            for bar_con in self.condicioned_bars:
                bar_id, probability_type, threshold, max_prob = bar_con
                
                bar_value = bars_value_dic[bar_id]
                
                prob = 0.0
                if probability_type == "direct":
                    if bar_value >= threshold:
                        prob = max_prob * ((bar_value - threshold) / (MAX_BAR_VALUE - threshold))
                    
                elif probability_type == "indirect":
                    if bar_value <= threshold:
                        prob = max_prob * ((threshold - bar_value) / threshold)
                    
                elif probability_type == "constant":
                    if bar_value <= threshold :
                        prob = float(max_prob)
                        
                elif probability_type == "range":
                    rMin, rMax = threshold
                    pMin, pMax = max_prob
                    if rMin <= bar_value and bar_value <= rMax:
                        prob = pMin + (bar_value-rMin)*(pMax-pMin)/(rMax-rMin)
                    
                elif probability_type == "triggered" and triggered:
                    print "triggered"
                    prob = 1.0
            
                if self.operator == "all" and prob == 0.0:
                    return 0.0
                    
                probs.append(prob)
        
        if probs:
            self.condicioned_probability = sum(probs) / len(probs)
        
        return self.condicioned_probability
    
    def get_probability(self):
        #eventually we just take the conditioned
        #probability
        return int(self.condicioned_probability)
        
        
    def perform(self):
        if self.time_left is None or self.time_left:
            if self.effect:
                self.effect.activate(1)
                
            if not self.time_left is None:
                self.time_left -= 1
    
    def reset(self):
        self.time_left = self.time_span
    
    def add_restriction(self, restriction_id, values):
        """ Adds a restriction for this event to be triggered
            place: []
            weather: []
            time: []
            clothes: []
        """
        self.restrictions[restriction_id] = values
        
class PersonalEvent(Event):
    def __init__(self, picture, kid_animation_path, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, kid_message, library_link, level=1, preferred_mood=9):
        Event.__init__(self, picture, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, library_link, level, preferred_mood)
        
        self.kid_animation_path = kid_animation_path
    
        # Messages at ballon
        self.kid_message = kid_message
        self.message_time_span = 250
    
    
class SocialEvent(Event):
    
    def __init__(self, picture, person_path, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, message, library_link, level=1, preferred_mood=9):
        Event.__init__(self, picture, name, description, impact, appereance_probability, time_span, conditioned_bars, effect, library_link, level, preferred_mood)
        
        self.time_left = time_span
        
        self.person_path = person_path
        self.person_message = message
        self.message_time_span = 250
