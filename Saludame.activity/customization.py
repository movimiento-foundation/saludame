# -*- coding: utf-8 -*-

import os
import pygame
import utilities
import animation
import gui

from gettext import gettext as _

COLORS_HAIR = [
    ("#000000", "#191919"), # BLACK
    ("#fce94f", "#edd400"), # YELLOW
    ("#803310", "#552210"), # BROWN
    ("#A03310", "#852210"), # Red
]

COLORS_SKIN = [
    ("#ffccc7", "#cba5a0"),
    ("#ffca90", "#eab484"),
    ("#eab484", "#d89f6c"),
    ("#d89f6c", "#c78c56"),
    ("#c78c56", "#b8773d"),
    ("#b8773d", "#8f5f33"),
    ("#8f5f33", "#784b23"),
    ("#784b23", "#593d24"),
    ("#593d24", "#593d24"),
    ("#4a311b", "#3b2614"),
]

TANGO_PALETTE = [
    ("#edd400", "#c4a000"), # Yellow
    ("#f57700", "#ce5c00"), # Orange
    ("#c17d11", "#8f5902"), # Brown
    ("#73d216", "#4e9a06"), # Green
    ("#3465a4", "#204a87"), # Blue
    ("#75507b", "#5c3566"), # Plum
    ("#cc0000", "#a40000"), # Red
    ("#ffffff", "#d3d7cf"), # White
    ("#d3d7cf", "#babdb6"), # Aluminium light
    ("#555753", "#2e3436"), # Aluminium dark
    ("#000000", "#2e3436"), # Black
    
    # Original design (not tango)
    ("#fd8255", "#db601f"), # Orange
    ("#eeea00", "#938200")  # Yellow
]

COLORS_SOCKS = TANGO_PALETTE
COLORS_SHOES = TANGO_PALETTE

class CustomizationWindow(gui.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, character):
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "customization_window")
        self.set_bg_image("assets/windows/window_2.png")
        
        kid_rect = pygame.Rect((20, 20), (1, 1))
        self.kid = CustomizatedKid(self.rect, kid_rect, 1, character)
        self.add_child(self.kid)
        
        self.btn_close = utilities.get_accept_button(self.rect, pygame.Rect((400, 500), (1, 1)), _("Continue"), self._cb_button_click_close)
        
        button_back = pygame.image.load("customization/customization_button.png").convert()
        self.btn_hair = gui.TextButton2(self.rect, pygame.Rect((500, 120), (70, 30)), 1, _("Hair"), 30, (255, 255, 255), button_back, self._cb_button_hair)
        self.btn_skin = gui.TextButton2(self.rect, pygame.Rect((500, 200), (70, 30)), 1, _("Skin"), 30, (255, 255, 255), button_back, self._cb_button_skin)
        self.btn_socks = gui.TextButton2(self.rect, pygame.Rect((500, 280), (70, 30)), 1, _("Socks"), 30, (255, 255, 255), button_back, self._cb_button_socks)
        self.btn_shoes = gui.TextButton2(self.rect, pygame.Rect((500, 360), (70, 30)), 1, _("Shoes"), 30, (255, 255, 255), button_back, self._cb_button_shoes)
        map(self.add_button, [self.btn_close, self.btn_hair, self.btn_skin, self.btn_socks, self.btn_shoes])
        
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

class CustomizatedKid(gui.Widget):
    
    def __init__(self, container, rect, frame_rate, character):
        gui.Widget.__init__(self, container, rect, frame_rate)
        
        self.character = character
        self.set_gender("male") # Sets the correct picture and applies color mappings
        
        self.dirty_mappings = True      # Only for the first update
    
    def set_mapping(self, key, colors):
        self.character.mappings[key] = tuple(colors)
        self.apply_mappings()
        
    def apply_mappings(self):
        self.background = self.kid.copy()
        maps = self.character.mappings
        self.change_color(animation.COLORS_TO_MAP, maps["hair"] + maps["skin"] + maps["socks"] + maps["shoes"])
        self.set_dirty()
        
    def change_color(self, old, new):
        index = 0
        for old_color in old:
            new_color = new[index]
            utilities.change_color(self.background, old_color, new_color)
            index += 1
            
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
    
    def update(self, frames):
        if self.dirty_mappings:
            self.dirty_mappings = False
            self.apply_mappings()
            self.set_dirty()
    