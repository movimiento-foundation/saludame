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
    ("#eab484", "#d89f6c"),
    ("#b8773d", "#754b28"),
    ("#754b28", "#3e2009"),
]

COLORS_CLOTHES = [
    ("#ff9900", "#d37e00", "#b06800", "#b06800"),  # orange
    ("#00d69f", "#00b07e", "#008c64", "#008c64"),  # green
    ("#00dcff", "#00b7d3", "#0099b0", "#0099b0"),  # skyblue
    ("#d61ccb", "#a60e9d", "#6f0269", "#6f0269"),  # violet
    ("#ff0083", "#d3006e", "#b0005c", "#b0005c"),  # lila
    ("#0090d6", "#007ab0", "#00628c", "#00628c"),  # blue
    ("#d0dd49", "#c8d539", "#bfcb37", "#bfcb37"),  # yellow
    ("#ab7013", "#784c07", "#3d2602", "#3d2602"),  # brown
    ("#4b4b4b", "#282828", "#000000", "#000000"),  # black
    ("#ab7013", "#784c07", "#3d2602", "#3d2602"),  # brown
]

COLORS_SWEATER = COLORS_CLOTHES
COLORS_PANTS = COLORS_CLOTHES
COLORS_SHOES = COLORS_CLOTHES

class CustomizationWindow(gui.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, character):
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "customization_window")
        self.set_bg_image("assets/windows/window_2.png")
        
        kid_rect = pygame.Rect((20, 10), (1, 1))
        self.kid = CustomizatedKid(self.rect, kid_rect, 1, character)
        self.add_child(self.kid)
        
        title = gui.Text(self.rect, 590, 60, 1, _("Creá tu personaje"), 32, pygame.Color("#0f5e65"), alignment=gui.Text.ALIGN_CENTER, bold=True)
        self.add_child(title)
        
        btn_close = utilities.get_accept_button(self.rect, pygame.Rect((400, 500), (1, 1)), _("Continue"), self._cb_button_click_close)
        
        button_back = pygame.image.load("customization/customization_button.png").convert()
        btn_hair = gui.TextButton2(self.rect, pygame.Rect((500, 100), (70, 30)), 1, _("Hair"), 28, (255, 255, 255), button_back, self._cb_button_hair)
        btn_skin = gui.TextButton2(self.rect, pygame.Rect((500, 170), (70, 30)), 1, _("Skin"), 28, (255, 255, 255), button_back, self._cb_button_skin)
        btn_sweater = gui.TextButton2(self.rect, pygame.Rect((500, 240), (70, 30)), 1, _("Sweater"), 28, (255, 255, 255), button_back, self._cb_button_sweater)
        btn_pants = gui.TextButton2(self.rect, pygame.Rect((500, 310), (70, 30)), 1, _("Pants"), 28, (255, 255, 255), button_back, self._cb_button_pants)
        btn_shoes = gui.TextButton2(self.rect, pygame.Rect((500, 380), (70, 30)), 1, _("Shoes"), 28, (255, 255, 255), button_back, self._cb_button_shoes)
        map(self.add_button, [btn_close, btn_hair, btn_skin, btn_sweater, btn_pants, btn_shoes])
        
        self.hair_color_index = 0
        self.skin_color_index = 0
        self.sweater_color_index = 0
        self.pants_color_index = 0
        self.shoes_color_index = 0
    
    def get_windows(self):
        return [self]

    def reload(self):
        """ called when the game is reseted, and posibly the character gender changed """
        self.kid.reload()
        
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
    
    def _cb_button_sweater(self, button):
        self.sweater_color_index += 1
        self.sweater_color_index %= len(COLORS_SWEATER)
        new_colors = [pygame.Color(color) for color in COLORS_SWEATER[self.sweater_color_index]]
        self.kid.set_mapping("sweater", new_colors)
    
    def _cb_button_pants(self, button):
        self.pants_color_index += 1
        self.pants_color_index %= len(COLORS_PANTS)
        new_colors = [pygame.Color(color) for color in COLORS_PANTS[self.pants_color_index]]
        self.kid.set_mapping("pants", new_colors)
        
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
        self.set_gender(character.sex) # Sets the correct picture and applies color mappings
        
        self.dirty_mappings = True      # Only for the first update
    
    def reload(self):
        self.set_gender(self.character.sex)
        self.dirty_mappings = True      # Only for the first update
        
    def set_mapping(self, key, colors):
        mapping = self.character.mappings[key]
        self.character.mappings[key] = tuple(colors[0:len(mapping)])
        self.apply_mappings()
        
    def apply_mappings(self):
        self.background = self.kid.copy()
        maps = self.character.mappings
        self.change_color(animation.COLORS_TO_MAP, maps["hair"] + maps["skin"] + maps["sweater"] + maps["pants"] + maps["shoes"])
        self.set_dirty()
        
    def change_color(self, old, new):
        index = 0
        for old_color in old:
            new_color = new[index]
            utilities.change_color(self.background, old_color, new_color)
            index += 1
            
    def set_gender(self, gender):
        path = None
        
        if gender == "boy":
            path = MALE_PATH
        
        if gender == "girl":
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
    