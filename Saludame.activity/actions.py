# -*- coding: utf-8 -*-

import status_bars
import events

class Action:
    
    def __init__(self, icon, picture, appereance_probability, time_span, kid_animation, window_animation, sound, effect):
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
        
    def performance(self):
        self.effect.activate()
        
class Character:
    
    def __init__(self, name, level, score, hair_color, eyes_color, skin_color, shoes_color, status_bar_dictionary):
        self.name = name
        self.level = level
        self.score = score
        """ visuals """
        self.hair_color = hair_color
        self.eyes_color = eyes_color
        self.skin_color = skin_color
        self.shoes_color = shoes_color
        """ """
        self.status_bar_dictionary = status_bar_dictionary #status bars {string id: Bar bar}
        self.active_events_list = []

        self.mood_list = [] #Class Mood instance's list
        
class Mood:
    
    def _init__(self, name, kid_animation):
        self.kid_animation_path = kid_animation.path
        self.kid_frame_rate = kid_animation.frame_rate

class Effect:
   
    def __init__(self, effect_status_list):
        self.effect_status_list = effect_status_list
    
    def add_effect(self, effect_status):
        self.effect_status_list.append(effect_status)
        
    def activate(self):
        for effect in self.effect_status_list:
            effect.activate()

class EffectStatus:
    """
    Abstract class ?
    """
    def __init__(self, increase_rate):
        self.increase_rate = increase_rate
        
    def activate(self, status_bar):
        status_bar.increase(self.increase_rate)
    
