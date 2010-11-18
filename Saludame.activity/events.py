# -*- coding: utf-8 -*-

import actions

class Event:
    
    def __init__(self, picture, kid_animation_path, name, appereance_probability, time_span, kind, event_status, effect, kid_message, preferred_mood=9, message_time_span=5):
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
        
        self.effect = effect
        
    def perform(self):
        if(self.time_left):
            self.effect.activate()
            self.time_left -= 1
    
    def reset(self):
        self.time_left = self.time_span
        
class EventStatusProbability:
    
    def __init__(self, conditioned_probability, direct_indirect):
        self.conditioned_probability = conditioned_probability
        self.direct_indirect = direct_indirect


