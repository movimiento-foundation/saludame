# -*- coding: utf-8 -*-

import status_bars
import events

class Action:
    
    def __init__(self, id, icon, picture, appereance_probability, time_span, kid_animation, window_animation, sound, effect):
        
        self.id = id
        self.appereance_probability = appereance_probability
        self.time_span = time_span
        self.effect = effect
        
        """ animations """
        self.icon = icon
        self.picture = picture
        
        self.kid_animation_path = kid_animation.path
        self.kid_loop_times = kid_animation.loop_times
        self.kid_frame_rate = kid_animation.frame_rate
        
        self.window_animation_path = window_animation.path
        self.window_window_loop_times = window_animation.loop_times
        self.window_frame_rate = window_animation.frame_rate

        self.sound_path = sound.path
        self.sound_loop_times = sound.loop_times
        
    def perform(self):
        self.effect.activate()
        
class Mood:
    
    def _init__(self, name, kid_animation):
        self.kid_animation_path = kid_animation.path
        self.kid_frame_rate = kid_animation.frame_rate
    


