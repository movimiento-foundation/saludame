# -*- coding: utf-8 -*-

import os
import pygame
import window
import utilities
from gettext import gettext as _

class CustomizationWindow(window.Window):
    
    def __init__(self, rect, frame_rate, background, screen):
        window.Window.__init__(self, rect, frame_rate, background, screen)
        
        self.screen = screen
        self.windows = []
        kid_rect = self.rect.move(50, 40)
        self.kid = CustomizatedKid(kid_rect, 1, pygame.Color("Black"), screen)
        self.windows.append(self.kid)
        
        self.btn_close = utilities.CloseButton(self.rect, 770, 5, 30, 30, "X")
        self.btn_eyes = utilities.Button(self.rect, 500, 200, 60, 30, _("Shoes"))
        
        self.color_list = [pygame.Color(color) for color in ["Brown", "Black", "Green", "Gray", "Skyblue", "Blue"]]
        self.eyes_color_index = 0
        
    def draw(self, screen):
        screen.fill(self.background_color)
        self.btn_close.draw(screen)
        self.btn_eyes.draw(screen)
        changes = []
        for win in self.windows:
            changes += win.draw(screen)
        return [self.rect] #changes
        
    def get_windows(self):
        return [self]
    
    def handle_mouse_over(self, (x, y)):
        pass

    def handle_mouse_down(self, (x, y), windows_controller):
        if self.btn_close.contains_point(x, y):
            self.btn_close.on_mouse_click(windows_controller)

        if self.btn_eyes.contains_point(x, y):
            self.eyes_color_index += 1
            self.eyes_color_index %= len(self.color_list)
            self.kid.set_mapping("eyes", self.color_list[self.eyes_color_index])
    
MALE_PATH = os.path.normpath("customization/boy.png")
FEMALE_PATH = os.path.normpath("customization/girl.png")

class CustomizatedKid(window.Window):
    
    COLOR_MAP = {
        "hair": pygame.Color("#803300"),
        "eyes": pygame.Color("#078002"),
        "skin": pygame.Color("#803300")
    }
    
    def __init__(self, rect, frame_rate, background, screen):
        window.Window.__init__(self, rect, frame_rate, background, screen)
         
        self.mappings = CustomizatedKid.COLOR_MAP.copy()
        self.set_gender("male")
         
    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        return [self.rect]
    
    def set_mapping(self, key, color):
        self.mappings[key] = color
        self.apply_mappings()
        
    def apply_mappings(self):
        self.sprite = self.surface.copy()
        for key in CustomizatedKid.COLOR_MAP:
            utilities.change_color(self.sprite, CustomizatedKid.COLOR_MAP[key], self.mappings[key])
        
    def set_gender(self, gender):
        path = None
        
        if gender == "male":
            path = MALE_PATH
        
        if gender == "female":
            path = FEMALE_PATH
        
        if path:
            self.surface = pygame.image.load(path)
            self.rect.size = self.surface.get_size()
            self.apply_mappings()
