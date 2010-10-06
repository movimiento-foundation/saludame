# -*- coding: utf-8 -*-

import actions

class Event:
    
    def __init__(self, picture, appereance_probability, time_span, kind, event_status, effect):
        self.appereance_probability = appereance_probability
        self.time_span = time_span
    
        self.event_status = event_status #instance EventStatusProbability
         
        self.picture = picture
        self.kind = kind
        
        self.effect = effect
        
class EventStatusProbability:
    
    def __init__(self, conditioned_probability, direct_indirect):
        self.conditioned_probability = conditioned_probability
        self.direct_indirect = direct_indirect
