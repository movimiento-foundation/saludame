# -*- coding: utf-8 -*-

import os
import pygame
import window
import widget
import utilities
from gettext import gettext as _

class CustomizationWindow(window.Window):
    
    def __init__(self, container, rect, frame_rate, background, screen, windows_controller):
        window.Window.__init__(self, container, rect, frame_rate, background, screen, windows_controller)
        
        kid_rect = pygame.Rect((200, 100), (1,1))
        self.kid = CustomizatedKid(self.rect, kid_rect, 1, pygame.Color("Black"), screen)
        self.widgets.append(self.kid)
        
        self.btn_close = utilities.TextButton(self.rect, pygame.Rect((770, 5), (30, 30)), 1, "X", 30, (0, 0, 0), self._cb_button_click_close)
        self.btn_eyes = utilities.TextButton(self.rect, pygame.Rect((500, 200), (70, 30)), 1, _("Shoes"), 30, (0, 0, 0), self._cb_button_shoes)
        self.buttons += [self.btn_close, self.btn_eyes]
        self.widgets += [self.btn_close, self.btn_eyes]
        
        self.color_list = [pygame.Color(color) for color in ["Brown", "Black", "Green", "Gray", "Skyblue", "Blue"]]
        self.eyes_color_index = 0
    
    def get_windows(self):
        return [self]
    
    def handle_mouse_over(self, (x, y)):
        pass

    def _cb_button_shoes(self, button):
        self.eyes_color_index += 1
        self.eyes_color_index %= len(self.color_list)
        self.kid.set_mapping("eyes", self.color_list[self.eyes_color_index])
    
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
    
MALE_PATH = os.path.normpath("customization/boy.png")
FEMALE_PATH = os.path.normpath("customization/girl.png")

class CustomizatedKid(widget.Widget):
    
    COLOR_MAP = {
        "hair": pygame.Color("#803300"),
        "eyes": pygame.Color("#078002"),
        "skin": pygame.Color("#803300")
    }
    
    def __init__(self, container, rect, frame_rate, surface, tooltip=None):
        widget.Widget.__init__(self, container, rect, frame_rate, surface, tooltip)
        
        self.mappings = CustomizatedKid.COLOR_MAP.copy()
        self.set_gender("male")
        
    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        return [self.rect]
    
    def set_mapping(self, key, color):
        self.mappings[key] = color
        self.apply_mappings()
        
    def apply_mappings(self):
        self.sprite = self.background.copy()
        for key in CustomizatedKid.COLOR_MAP:
            utilities.change_color(self.sprite, CustomizatedKid.COLOR_MAP[key], self.mappings[key])
        
    def set_gender(self, gender):
        path = None
        
        if gender == "male":
            path = MALE_PATH
        
        if gender == "female":
            path = FEMALE_PATH
        
        if path:
            self.background = pygame.image.load(path)
            self.rect.size = self.background.get_size()
            self.apply_mappings()
    
