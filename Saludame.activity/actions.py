# -*- coding: utf-8 -*-

import game_manager
import effects
import status_bars
import events
import pygame

class Action:
    
    def __init__(self, action_id, appereance_probability, time_span, kid_animation_frames, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect, allowed_places, allowed_hours, allowed_events, level=1, link=None, background=None):
        
        self.id = action_id
        self.appereance_probability = appereance_probability
        self.time_span = time_span
        self.time_left = time_span
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
        self.kid_frames = kid_animation_frames
        self.kid_frames_left = kid_animation_frames
        
        self.window_animation_path = window_animation_path
        self.window_window_loop_times = window_animation_loop_times
        self.window_frame_rate = window_animation_frame_rate

        self.sound_path = sound_path
        self.sound_loop_times = sound_loop_times
        
        self.background = background
        
    def perform(self):
        if self.sound_path:
            pygame.mixer.Sound(self.sound_path).play()
            
        if self.background:
            game_manager.instance.set_character_location(self.background)
            
        if self.time_span == -1:
            # Perpetual
            if isinstance(self.effect, effects.Effect): #this action affects status bars
                for effect_status in self.effect.effect_status_list:
                    game_manager.instance.bars_controller.increase_bar(effect_status[0], effect_status[1] / self.time_span)
            else:
                self.effect.activate()
        else:
            # Checks time left
            if self.time_left > 0:
                if isinstance(self.effect, effects.Effect): #this action affects status bars
                    for effect_status in self.effect.effect_status_list:
                        game_manager.instance.bars_controller.increase_bar(effect_status[0], effect_status[1] / self.time_span)
                else:                
                    self.effect.activate()
                self.time_left -= 1
            else:
                self.time_left = 0
    
    def decrease_frames_left(self):
        self.kid_frames_left -= 1
    
    def reset(self):
        self.time_left = self.time_span
        self.kid_frames_left = self.kid_frames
        
class Mood:
    
    def __init__(self, name, rank, kid_animation_path, music, frame_rate=11):
        self.name = name
        self.rank = rank #hierarchy of moods
        self.music = music
        
        self.kid_animation_path = kid_animation_path
        self.kid_frame_rate = frame_rate
