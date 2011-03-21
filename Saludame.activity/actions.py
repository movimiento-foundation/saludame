# -*- coding: utf-8 -*-

import game_manager
import effects
import pygame

class Action:
    

    def __init__(self, action_id, appereance_probability, time_span_in_frames, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect, allowed_places, allowed_hours, allowed_events, level=1, link=None, background=None):        
        self.id = action_id
        self.appereance_probability = appereance_probability
        self.time_span = time_span_in_frames
        self.time_left = time_span_in_frames
        self.effect = effect
        
        self.link = link
        
        # conditions
        self.allowed_places = allowed_places
        self.allowed_hours = allowed_hours
        self.allowed_events = allowed_events
        self.level = level
        
        # animations
        self.kid_animation_path = kid_animation_path
        self.kid_loop_times = kid_animation_loop_times
        
        self.window_animation_path = window_animation_path
        self.window_window_loop_times = window_animation_loop_times
        self.window_frame_rate = window_animation_frame_rate

        self.sound_path = sound_path
        self.sound_loop_times = sound_loop_times
        
        self.background = background
        
    def perform(self, cicles):
        if self.background:
            game_manager.instance.set_character_location(self.background)
        
        if self.time_span == -1:
            # Perpetual
            self.effect.activate(1)
        else:
            # Checks time left
            if self.time_left > 0:
                factor = float(cicles) / self.time_span
                self.effect.activate(factor)
    
    def decrease_frames_left(self):
        self.time_left -= 1
    
    def reset(self):
        self.time_left = self.time_span
    
class Mood:
    
    def __init__(self, name, rank, kid_animation_path, music, frame_rate=11):
        self.name = name
        self.rank = rank #hierarchy of moods
        self.music = music
        
        self.kid_animation_path = kid_animation_path
        self.kid_frame_rate = frame_rate
