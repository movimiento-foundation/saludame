# -*- coding: utf-8 -*-

# This module offers a menu.
# Items are displayed in a circle with an exit button as a center.
# The diameter of the circle will vary with the quantity of items
# Items will be a concatenation of an icon and a name
# When mouse over an item a description will be shown

import pygame
import os
import math

BLACK = pygame.Color("black")

example = [
    ("name", "icon.png", "tooltip", None),
    ("eat", "icon.png", "comer algo", [
        ("apple", "icon.png", "Eat an apple", None),
        ("meat", "icon.png", "Eat meat", None)
    ]),
    ("sport", "icon.png", "Do sports...", [
        ("run", "icon.png", "Run", None),
        ("jump rope", "icon.png", "Jump the rope", None),
        ("footbal", "icon.png", "Play footbal", None)
    ]),
    ("sleep", "icon.png", "Go to sleep", None)
]

class Menu:
    
    def __init__(self, rect, frame_rate):
        self.rect = rect
        self.frame_rate = frame_rate
        self.menu = example
        
        self.path = None        # Path of items selected
        
        # Test
        self.path = ["sport"]
        self.calculate()

    def calculate(self):
        """
        creates a rect list with the coordinates of the menu options to be displayed
        """
        
        menu = self.menu
        for entry in self.path:
            parent = menu
            menu = [item[3] for item in menu if item[0] == entry][0]    # Selects the submenu named entry
        
        qty = len(menu)
        
        angle = (2 * math.pi) / qty     # Angle beetwen options (in radians)
        radius = 100
        width, height = 120, 30
        center = pygame.Rect(200, 250, width, height)
        
        self.rect_list = [center]
        
        current_angle = math.pi / 2
        for item in menu:
            rect = center.copy()
            rect.center = rect.center[0] + math.cos(current_angle)*radius, rect.center[1] + math.sin(current_angle)*radius
            self.rect_list.append(rect)
            current_angle += angle
        
    def draw(self, screen):
        for rect in self.rect_list:
            screen.fill(BLACK, rect)
        return self.rect_list
