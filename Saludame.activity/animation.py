# -*- coding: utf-8 -*-

import pygame
import os
import utilities
from window import *

KID_PATH = os.path.normpath("assets/kid/animation/")
KID_PREFIX, KID_SUFIX = "character1_", ".png"

COLORS_HAIR = ("#000000", "#191919")
COLORS_HAIR_NEW = [("#000000", "#191919"), ("#FFFF10", "#DDDD10"), ("#803310", "#552210")]

COLORS_SKIN = ("#ffccc7", "#f3b9b6")
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
    
    def __init__(self, container, rect, frame_rate, windows_controller, game_man):
        Window.__init__(self, container, rect, frame_rate, windows_controller, "character_window")
        
        self.index = 1
        
        self.character = game_man.character
        
    def pre_draw(self, screen):
        file_nro = str(self.index)
        file_nro = "0" * (4 - len(file_nro)) + file_nro
        
        file = os.path.join(KID_PATH, KID_PREFIX + file_nro + KID_SUFIX)
        self.sprite = pygame.image.load(file)
        
        maps = self.character.mappings
        self.change_color(COLORS_HAIR + COLORS_SKIN + COLORS_SOCKS + COLORS_SHOES, maps["hair"] + maps["skin"] + maps["socks"] + maps["shoes"])
        
        screen.blit(self.bg_image, self.rect)
        screen.blit(self.sprite, self.rect)
        
        self.index %= 150
        self.index += 1
        
        return [self.rect]
        
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
