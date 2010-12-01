# -*- coding: utf-8 -*-

import status_bars
import events

class Action:
    
    def __init__(self, id, appereance_probability, time_span, kid_animation_frame_rate, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect):
        
        self.id = id
        self.appereance_probability = appereance_probability
        self.time_span = time_span
        self.time_left = time_span
        self.effect = effect
        
        """ animations """
        self.kid_animation_path = kid_animation_path
        self.kid_loop_times = kid_animation_loop_times
        self.kid_frame_rate = kid_animation_frame_rate
        
        self.window_animation_path = window_animation_path
        self.window_window_loop_times = window_animation_loop_times
        self.window_frame_rate = window_animation_frame_rate

        self.sound_path = sound_path
        self.sound_loop_times = sound_loop_times
        
    def perform(self):
        if self.time_span == -1:
            # Perpetual
            self.effect.activate()
        else:
            # Checks time left
            if self.time_left > 0:
                self.effect.activate()
                self.time_left -= 1
            else:
                self.time_left = 0
    
    def reset(self):
        self.time_left = self.time_span    
        
class Mood:
    
    def __init__(self, name, rank, kid_animation_path, frame_rate=11):
        self.name = name
        self.rank = rank #hierarchy of moods
        
        self.kid_animation_path = kid_animation_path
        self.kid_frame_rate = frame_rate
