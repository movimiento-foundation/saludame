# -*- coding: utf-8 -*-

import os
import pygame
import window
import widget
import utilities
from gettext import gettext as _

class CustomizationWindow(window.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color):
        window.Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        
        kid_rect = pygame.Rect((20, 20), (1,1))
        self.kid = CustomizatedKid(self.rect, kid_rect, 1, pygame.Color("Black"))
        self.add_child(self.kid)
        
        self.btn_close = utilities.TextButton(self.rect, pygame.Rect((770, 5), (30, 30)), 1, "X", 30, (0, 0, 0), self._cb_button_click_close)
        self.btn_hair = utilities.TextButton(self.rect, pygame.Rect((500, 150), (70, 30)), 1, _("Hair"), 30, (0, 0, 0), self._cb_button_hair)
        self.btn_skin = utilities.TextButton(self.rect, pygame.Rect((500, 200), (70, 30)), 1, _("Skin"), 30, (0, 0, 0), self._cb_button_skin)
        self.btn_socks = utilities.TextButton(self.rect, pygame.Rect((500, 250), (70, 30)), 1, _("Socks"), 30, (0, 0, 0), self._cb_button_socks)
        self.btn_shoes = utilities.TextButton(self.rect, pygame.Rect((500, 300), (70, 30)), 1, _("Shoes"), 30, (0, 0, 0), self._cb_button_shoes)
        self.buttons += [self.btn_close, self.btn_hair, self.btn_skin, self.btn_socks, self.btn_shoes]
        self.widgets += [self.btn_close, self.btn_hair, self.btn_skin, self.btn_socks, self.btn_shoes]
        
        self.color_list = [(pygame.Color(c1), pygame.Color(c2)) for (c1, c2) in [
            ("#7f2400", "#6a1e00" ),    #Brown
            ("#030601", "#181917"),     #Black
            ("#1c8500", "#166700"),     #Green
            ("#727272", "#565656"),     #Gray
            ("#001385", "#001385")      #Blue
            ]
        ]
        self.hair_color_index = 0
        self.skin_color_index = 0
        self.socks_color_index = 0
        self.shoes_color_index = 0
    
    def get_windows(self):
        return [self]

    def _cb_button_hair(self, button):
        self.hair_color_index += 1
        self.hair_color_index %= len(self.color_list)
        self.kid.set_mapping("hair", self.color_list[self.hair_color_index])
        
    def _cb_button_skin(self, button):
        self.skin_color_index += 1
        self.skin_color_index %= len(self.color_list)
        self.kid.set_mapping("skin", self.color_list[self.skin_color_index])

    def _cb_button_socks(self, button):
        self.socks_color_index += 1
        self.socks_color_index %= len(self.color_list)
        self.kid.set_mapping("socks", self.color_list[self.socks_color_index])
        
    def _cb_button_shoes(self, button):
        self.shoes_color_index += 1
        self.shoes_color_index %= len(self.color_list)
        self.kid.set_mapping("shoes", self.color_list[self.shoes_color_index])
        
    def _cb_button_click_close(self, button):
        self.windows_controller.close_active_window()
    
MALE_PATH = os.path.normpath("customization/boy.png")
FEMALE_PATH = os.path.normpath("customization/girl.png")

class CustomizatedKid(widget.Widget):
    
    COLOR_MAP = {
        "hair": (pygame.Color("#030601"), pygame.Color("#181917")),
        #"eyes": pygame.Color("#078002"),
        "skin": (pygame.Color("#ffd0c7"), pygame.Color("#ebbdba")),
        "socks": (pygame.Color("#ef8a58"), pygame.Color("#a6a700")),
        "shoes": (pygame.Color("#eee500"), pygame.Color("#ce6d30"))
    }
    
    def __init__(self, container, rect, frame_rate, surface, tooltip=None):
        widget.Widget.__init__(self, container, rect, frame_rate, surface, tooltip)
        
        self.mappings = CustomizatedKid.COLOR_MAP.copy()
        self.set_gender("male")
        
        self.background = self.kid
    
    def set_mapping(self, key, colors):
        self.mappings[key] = colors
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
    