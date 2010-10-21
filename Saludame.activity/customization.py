# -*- coding: utf-8 -*-

import os
import pygame
import window
import widget
import utilities
from gettext import gettext as _

COLORS_HAIR = [
    ("#000000", "#191919"),     # BLACK
    ("#FFFF10", "#DDDD10"),     # YELLOW
    ("#803310", "#552210"),     # BROWN
    ("#A03310", "#852210"),     # Red
]

COLORS_SKIN = [
    ("#ffccc7", "#f3b9b6"),
    ("#f6d04e", "#eeca4c"),
    ("#694321", "#5b3a1c"),
    ("#805030", "#784828"),
]

COLORS_SOCKS = [
    ("#fd8255", "#db601f"),     # Orange
    ("#FFFF00", "#DDDD00" ),    # Yellow
    ("#803300", "#552200")      # Brown
]

COLORS_SHOES = [
    ("#00B000", "#006000"),     # Green
    ("#2222FF", "#5522FF"),     # Blue
    ("#AA00AA", "#AA44AA")      # Violet
]

class CustomizationWindow(window.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, character):
        window.Window.__init__(self, container, rect, frame_rate, windows_controller, pygame.Color("Gray"))
        
        kid_rect = pygame.Rect((20, 20), (1,1))
        self.kid = CustomizatedKid(self.rect, kid_rect, 1, character)
        self.add_child(self.kid)
        
        self.btn_close = utilities.TextButton(self.rect, pygame.Rect((770, 5), (30, 30)), 1, "X", 30, (0, 0, 0), self._cb_button_click_close)
        self.btn_hair = utilities.TextButton(self.rect, pygame.Rect((500, 150), (70, 30)), 1, _("Hair"), 30, (0, 0, 0), self._cb_button_hair)
        self.btn_skin = utilities.TextButton(self.rect, pygame.Rect((500, 200), (70, 30)), 1, _("Skin"), 30, (0, 0, 0), self._cb_button_skin)
        self.btn_socks = utilities.TextButton(self.rect, pygame.Rect((500, 250), (70, 30)), 1, _("Socks"), 30, (0, 0, 0), self._cb_button_socks)
        self.btn_shoes = utilities.TextButton(self.rect, pygame.Rect((500, 300), (70, 30)), 1, _("Shoes"), 30, (0, 0, 0), self._cb_button_shoes)
        self.buttons += [self.btn_close, self.btn_hair, self.btn_skin, self.btn_socks, self.btn_shoes]
        self.widgets += [self.btn_close, self.btn_hair, self.btn_skin, self.btn_socks, self.btn_shoes]
        
        self.hair_color_index = 0
        self.skin_color_index = 0
        self.socks_color_index = 0
        self.shoes_color_index = 0
    
    def get_windows(self):
        return [self]

    def _cb_button_hair(self, button):
        self.hair_color_index += 1
        self.hair_color_index %= len(COLORS_HAIR)
        new_colors = [pygame.Color(color) for color in COLORS_HAIR[self.hair_color_index]]
        self.kid.set_mapping("hair", new_colors)
        print new_colors
        
    def _cb_button_skin(self, button):
        self.skin_color_index += 1
        self.skin_color_index %= len(COLORS_SKIN)
        new_colors = [pygame.Color(color) for color in COLORS_SKIN[self.skin_color_index]]
        self.kid.set_mapping("skin", new_colors)

    def _cb_button_socks(self, button):
        self.socks_color_index += 1
        self.socks_color_index %= len(COLORS_SOCKS)
        new_colors = [pygame.Color(color) for color in COLORS_SOCKS[self.socks_color_index]]
        self.kid.set_mapping("socks", new_colors)
        
    def _cb_button_shoes(self, button):
        self.shoes_color_index += 1
        self.shoes_color_index %= len(COLORS_SHOES)
        new_colors = [pygame.Color(color) for color in COLORS_SHOES[self.shoes_color_index]]
        self.kid.set_mapping("shoes", new_colors)
        
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
    
MALE_PATH = os.path.normpath("customization/boy.png")
FEMALE_PATH = os.path.normpath("customization/girl.png")

class CustomizatedKid(widget.Widget):
    
    COLOR_MAP = {
        "hair": (pygame.Color("#000000"), pygame.Color("#191919")),
        "skin": (pygame.Color("#ffccc7"), pygame.Color("#f3b9b6")),
        "socks": (pygame.Color("#fd8255"), pygame.Color("#db601f")),
        "shoes": (pygame.Color("#eeea00"), pygame.Color("#938200"))
    }
    
    def __init__(self, container, rect, frame_rate, character):
        widget.Widget.__init__(self, container, rect, frame_rate, pygame.Color("Black"))
        
        self.character = character
        
        self.mappings = CustomizatedKid.COLOR_MAP.copy()
        self.character.mappings = self.mappings
        
        self.set_gender("male")
        
        self.background = self.kid
    
    def set_mapping(self, key, colors):
        self.mappings[key] = tuple(colors)
        self.character.mappings = self.mappings
        self.apply_mappings()
        
    def apply_mappings(self):
        self.background = self.kid.copy()
        for key in CustomizatedKid.COLOR_MAP:
            origin_colors = CustomizatedKid.COLOR_MAP[key]
            mapped_colors = self.mappings[key]
            utilities.change_color(self.background, origin_colors[0], mapped_colors[0])
            utilities.change_color(self.background, origin_colors[1], mapped_colors[1])
        
    def set_gender(self, gender):
        path = None
        
        if gender == "male":
            path = MALE_PATH
        
        if gender == "female":
            path = FEMALE_PATH
        
        if path:
            self.kid = pygame.image.load(path)
            self.set_rect_size(self.kid.get_size())
            self.apply_mappings()
    