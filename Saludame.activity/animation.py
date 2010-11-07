# -*- coding: utf-8 -*-

import pygame
import os
import utilities
from window import *

KID_PREFIX, KID_SUFIX = "character1_", ".png"

COLORS_HAIR = ("#00ffff", "#009f9f")
COLORS_HAIR_NEW = [("#000000", "#191919"), ("#FFFF10", "#DDDD10"), ("#803310", "#552210")]

COLORS_SKIN = ("#ffccc7", "#cba5a0")
COLORS_SKIN_NEW = [("#ffccc7", "#f3b9b6"), ("#694321", "#5b3a1c"), ("#f6d04e", "#eeca4c")]

COLORS_SOCKS = ("#fd8255", "#db601f")
COLORS_SOCKS_NEW = [("#fd8255", "#db601f"), ("#FFFF00", "#DDDD00"), ("#803300", "#552200")]

COLORS_SHOES = ("#eeea00", "#938200")
COLORS_SHOES_NEW = [("#00B000", "#006000"), ("#2222FF", "#5522FF"), ("#AA00AA", "#AA44AA")]

GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

class Kid(Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, game_man, mood):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "character_window")
        
        self.moods = game_man.moods_list
        
        self.mood = self.moods[9]
        
        self.character = game_man.character
        
        self.moods = game_man.moods_list
        self.mood_index = 9     
        
        self.index = 0      
            
    ##### Moods #####    
    def change_mood(self):
        self.mood_index += 1
        if self.mood_index == len(self.moods):
            self.mood_index = 0
        self.mood = self.moods[self.mood_index]
        self.index = 0
        
    def set_mood(self, mood):
        self.mood_index = self.moods.index(mood) 
        self.mood = self.moods[self.mood_index]
    
    ##### Draw #####
    def pre_draw(self, screen):
        
        dirList = os.listdir(self.mood.kid_animation_path)
        dirList.sort()
        self.file_list = [os.path.join(self.mood.kid_animation_path, fname) for fname in dirList if '.png' in fname]
        
        file = self.file_list[self.index]
        self.sprite = pygame.image.load(file)
        
        maps = self.character.mappings
        self.change_color(COLORS_HAIR + COLORS_SKIN + COLORS_SOCKS + COLORS_SHOES, maps["hair"] + maps["skin"] + maps["socks"] + maps["shoes"])
        
        screen.blit(self.bg_image, self.rect)
        screen.blit(self.sprite, self.rect)
        
        self.index = (self.index + 1) % len(self.file_list)
        
        return [self.rect]
    
    ##### Colors #####    
    def change_color(self, old, new):
        index = 0
        for old_color_text in old:
            old_color = pygame.Color(old_color_text)
            new_color = new[index]
            utilities.change_color(self.sprite, old_color, new_color)
            
            index += 1
            
class ActionAnimation():
    """
    An action animation to show at panel
    """
    def __init__(self, rect, frame_rate, animation_path, sound_path):
        
        self.path = animation_path
        self.rect = rect
        self.frame_rate = frame_rate
        
        dirList = os.listdir(animation_path)
        dirList.sort()
        self.file_list = [os.path.join(animation_path, fname) for fname in dirList if '.png' in fname]
        
        self.index = 0
        
        self.blip = pygame.mixer.Sound(sound_path)
        
    def draw(self, screen):
        file = self.file_list[self.index]
        self.sprite = pygame.image.load(file).convert_alpha()
        
        screen.fill(WHITE, self.rect)
        screen.blit(self.sprite, self.rect)
        
        self.index = (self.index + 1) % len(self.file_list)
        self.blip.play()
        
        return [self.rect]

class FPS:  
    def __init__(self, container, rect, frame_rate, clock):
        self.rect = rect
        self.frame_rate = frame_rate
        self.clock = clock

        self.font = pygame.font.Font(None, 16)
  
    def draw(self, screen, frames):
        screen.fill(BLACK, self.rect)
        text = str(round(self.clock.get_fps()))
        text_surf = self.font.render(text, False, (255, 255, 255))
        screen.blit(text_surf, self.rect)
        return [self.rect]
