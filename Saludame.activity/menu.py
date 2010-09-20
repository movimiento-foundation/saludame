# -*- coding: utf-8 -*-

# This module offers a menu.
# Items are displayed in a circle with an exit button as a center.
# The diameter of the circle will vary with the quantity of items
# Items will be a concatenation of an icon and a name
# When mouse over an item a description will be shown

import pygame
import os
import math
from ibus.lang import __load_lang

class Menu:
    
    def __init__(self, frame_rate, item_list):
        #self.rect = rect
        self.frame_rate = frame_rate
        self.item_list = item_list # item's list that going to be displayed
        self.path = None           # Path of items selected
        self.actual_selection = self.item_list #list of actual subitems selection
        self.salir = Item(" ", "assets/icons/salir.png", " ", [])
        self.salir.rect.center = (190, 140)
        self.radious = 100
        self.on_compression = True #para mostrar la animación al iniciar
        self.on_expansion = False
        
        self.__calculate()
        """
        self.path = ["sport"]
        self.calculate()
        """
    
    def draw(self, screen):
        font = pygame.font.Font(None, 35)
        if(self.on_compression):
            if(self.radious > 0):
                self.radious -= 8
                self.__calculate_items_position((190, 140), self.radious, self.item_list)
            else:
                self.on_compression = False
                self.on_expansion = True
        if(self.on_expansion):
            if(self.radious < 100):
                item = self.item_list[2]
                self.actual_selection = item.subitems_list
                self.radious += 5
                self.__calculate_items_position((190, 140), self.radious, self.actual_selection)
            else:
                self.on_expansion = False
                
        for item in self.actual_selection:
            item.draw_item(screen, font)
        self.salir.draw_item(screen, font)
        pygame.display.update()
        return []
    
    def on_mouse_over(self, coord):
        for item in self.actual_selection:
            if(item.rect.collidepoint(coord)):
                item.on_mouse_over()
                break
    
    def on_mouse_out(self, coord):
        for item in self.actual_selection:
            if(item.rect.collidepoint(coord)):
                item.on_mouse_out()
                break
    
    def on_mouse_click(self, coord):
        for item in self.actual_selection:
            if(item.rect.collidepoint(coord)):
                item.on_mouse_clik()
                break

                
    
    def __calculate(self):
        """
            Calculate the position for each menu's item
        """
        self.__calculate_items_position((170, 140), self.radious, self.item_list)
        
    def __calculate_items_position(self, center, radius, item_list):
        if(len(item_list) > 0):
            angle = (2 * math.pi) / len(item_list)
        else:
            angle = 0
        current_angle = math.pi / 4
        for item in item_list:
            self.__calculate_item_position(item, center, current_angle, radius) #calculate the position for each item
            self.__calculate_items_position(center, radius, item.subitems_list) #calculate the position for each item's subitem
            current_angle += angle
      
    def __calculate_item_position(self, item, center, angle, radius):
        """
        Calculates the position in the display for each menu item.
        """
        
        coord = int(center[0] + math.cos(angle) * radius), int(center[1] + math.sin(angle) * radius)    
        if(coord[0] < center[0]): 
            if(coord[1] > center[1]): #third quadrant
                item.rect.topright = coord
            elif(coord[1] < center[1]): #second quadrant
                item.rect.bottomright = coord
            else:
                item.rect.midright = coord
        elif(coord[0] > center[0]):
            if(coord[1] > center[1]): #fourth quadrant
                item.rect.topleft = coord
            elif(coord[1] < center[1]): #first quadrant
                item.rect.bottomleft = coord
            else:
                item.rect.midleft = coord
        else:
            if(coord[1] > center[1]):
                item.rect.midbottom = coord
            else:
                item.rect.midtop = coord

class Item:
    
    def __init__(self, name, icon_path, tooltip, subitems_list):
        self.name = name
        self.image = pygame.image.load(icon_path)
        self.rect = self.image.get_rect()
        self.tooltip = tooltip
        self.subitems_list = subitems_list
        
    def add_subitem(self, item):
        """
        Append a subitem to the item list
        """
        self.subitems_list.append(item)

    def draw_item(self, screen, font):
        img_font = font.render(self.name, True, (0, 0, 0))
        screen.blit(self.image, self.rect)
        screen.blit(img_font, self.rect.topright)
    
    def on_mouse_over(self):
        return
    
    def on_mouse_out(self):
        return
    
    def on_mouse_click(self):
        return
        
