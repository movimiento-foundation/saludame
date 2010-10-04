# -*- coding: utf-8 -*-

import pygame
import os
import utilities
from window import *

KID_PATH = os.path.normpath("assets/kid")
KID_PREFIX, KID_SUFIX = "kid", ".png"

COLORS_HAIR = ("#803300", "#552200")
COLORS_HAIR_NEW = [("#000000", "#101010"), ("#FFFF00", "#DDDD00"), ("#803300", "#552200")]

COLORS_EYES = ("#078002",)
COLORS_EYES_NEW = [("#008000",), ("#2222FF",), ("#000000",)]

GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
BLUE = pygame.Color("blue")

class Kid(Window):
    
    def __init__(self, container, rect, frame_rate, background, screen, windows_controller):
        Window.__init__(self, container, rect, frame_rate, background, screen, windows_controller)
        
        self.index = 1
        self.color_index = 0
        
    def pre_draw(self, screen):
        
        file_nro = str(self.index)
        if len(file_nro) == 1:
            file_nro = "0" + file_nro
            
        file = os.path.join(KID_PATH, KID_PREFIX + file_nro + KID_SUFIX)
        self.sprite = pygame.image.load(file)
        
        self.change_color(COLORS_HAIR + COLORS_EYES, COLORS_HAIR_NEW[self.color_index] + COLORS_EYES_NEW[self.color_index])
        
        screen.blit(self.background, self.rect)
        screen.blit(self.sprite, self.rect)
        
        self.index = (self.index % 11) + 1
        if self.index == 1:
            self.color_index = (self.color_index + 1) % 3               
                
    def change_color(self, old, new):
        # No funciona en pygame 1.8.0
        #image_pixel_array = pygame.PixelArray(self.sprite)
        #image_pixel_array.replace(old_color, new_color)
        
        index = 0
        for old_color_text in old:
            old_color = pygame.Color(old_color_text)
            new_color = pygame.Color(new[index])
            utilities.change_color(self.sprite, old_color, new_color)
            
            index += 1
      
BLIP_PATH = os.path.normpath("assets/sound/blip.ogg")
APPLE_PATH = os.path.normpath("assets/food/apple")

class Food:
    
    def __init__(self, path, rect, frame_rate):
        self.path = path
        self.frame_rate = frame_rate
        self.rect = rect
        
        dirList = os.listdir(path)
        dirList.sort()
        self.file_list = [os.path.join(APPLE_PATH, fname) for fname in dirList if '.png' in fname]
        
        self.index = 0
        
        self.blip = pygame.mixer.Sound(BLIP_PATH)
        
        
    def draw(self, screen, frames):
        file = self.file_list[self.index]
        self.sprite = pygame.image.load(file).convert_alpha()
        
        screen.fill(BLUE, self.rect)
        screen.blit(self.sprite, self.rect)
        
        self.index = (self.index + 1) % len(self.file_list)
        self.blip.play()
        return [self.rect]

class Apple(Food):
  
    def __init__(self, rect, frame_rate):
        Food.__init__(self, APPLE_PATH, rect, frame_rate)

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
