# -*- coding: utf-8 -*-

# This module offers a menu.
# Items are displayed in a circle with an exit button as a center.
# The diameter of the circle will vary with the quantity of items
# Items will be a concatenation of an icon and a name
# When mouse over an item a description will be shown

import pygame
import os
import math
from widget import Widget
from window import Window
import utilities

SIZE = 600, 280
EXP_SPEED = 10 #expansion speed, in pixels per frame

class Menu(Window):
    
    def __init__(self, frame_rate, container, windows_controller, item_list, center, radius, game_manager, font):
        
        rect = pygame.Rect((0, 0), SIZE)
        rect.center = center
        self.windows_controller = windows_controller
        Window.__init__(self, container, rect, frame_rate, windows_controller, "menu_window")
        
        self.center = center # center of the menu's circle
        
        self.frame_rate = frame_rate
        self.item_list = item_list # item's list that going to be displayed
        
        self.exit = Item(container, frame_rate, "salir", "assets/icons/icon_quit.png", "close_menu", [], self, font)
        self.exit.rect_in_container.center = center
        self.exit.set_rect_in_container(self.exit.rect_in_container)
        
        self.actual_selection = self.item_list  #list of actual subitems selection
        
        self.radius = radius
        self.show = False
        #self.on_compression = True #para mostrar la animación al iniciar
        self.on_expansion = False
        self.calculate()
        
        self.game_manager = game_manager
        
    
    def add_item(self, item):
        self.item_list.append(item)
    
    def set_items(self, items_list):
        self.item_list = items_list
    
    
    def pre_draw(self, screen):
        changes = []
        if self.show:
            if self.on_expansion:
                if self.radius < 90:
                    self.radius += EXP_SPEED
                    self.__calculate_items_position(self.actual_selection)
                else:
                    self.on_expansion = False
    
            for item in self.actual_selection:
                item.draw_item(screen)
                changes.append(item.rect_absolute)
                
            self.exit.draw_item(screen)
            changes.append(self.exit.rect_absolute)
        
        return changes
    
    def send_action(self, action_id):
        """
        Send an action to the game_manager. The action was selected
        in one of the sub-items
        """
        self.game_manager.set_active_action(action_id)
    
    def set_actual_selection(self, actual_selection):
        """
        Set the actual items selection.
        """
        if(not self.on_expansion):
            self.actual_selection = actual_selection
            self.on_expansion = True #if the selection changes, display the animation
            self.radius = 0
        
    def close(self):
        """
        Close the Menu Window
        """
        self.show = False
        self.set_actual_selection(self.item_list)    
    
    def handle_mouse_down(self, coord):
        if self.show:
            if not self.exit.rect_absolute.collidepoint(coord):
                for item in self.actual_selection:
                    if item.rect_absolute.collidepoint(coord):
                        item.on_mouse_click()
                        break
            else:
                self.close()
        else:
            self.show = True

    #privates
    
    def calculate(self):
        """
            Calculate the position for each menu's actual selection.
        """
        self.__calculate_items_position(self.actual_selection)
        
    def __calculate_items_position(self, item_list):
        if(len(item_list) > 0):
            angle = (2 * math.pi) / len(item_list)
        else:
            angle = 0
        current_angle = math.pi / 4
        for item in item_list:
            self.__calculate_item_position(item, current_angle) #calculate the position for each item
            #self.__calculate_items_position(center, radius, item.subitems_list) #calculate the position for each item's subitem
            current_angle += angle
      
    def __calculate_item_position(self, item, angle):
        """
        Calculates the position in the display for each menu item.
        """
        coord = int(self.center[0] + math.cos(angle) * self.radius), int(self.center[1] + math.sin(angle) * self.radius)
        rect = item.rect_in_container
        if coord[0] < self.center[0]: 
            if coord[1] > self.center[1]: #third quadrant
                rect.topright = coord
            elif coord[1] < self.center[1]: #second quadrant
                rect.bottomright = coord
            else:
                rect.midright = coord
        elif coord[0] > self.center[0]:
            if coord[1] > self.center[1]: #fourth quadrant
                rect.topleft = coord
            elif coord[1] < self.center[1]: #first quadrant
                rect.bottomleft = coord
            else:
                rect.midleft = coord
        else:
            if coord[1] > self.center[1]:
                rect.midbottom = coord
            else:
                rect.midtop = coord
        item.set_rect_in_container(rect)   # Recalculates the absolute coordinates

class Item(Widget):
    """
    Entity that represent an item
    """
    def __init__(self, container, frame_rate, name, icon_path, action_id, subitems_list, menu, font):
        
        self.name = name
        self.subitems_list = subitems_list
        self.action_id = action_id
        self.menu = menu
        
        # visuals
        path = os.path.normpath(icon_path)
        icon = pygame.image.load(path).convert_alpha()
        text = font.render(self.name, True, (255, 255, 255))
        
        x_size = icon.get_size()[0] + text.get_size()[0] + 2
        y_size = max([icon.get_size()[1], text.get_size()[1]])
        
        surface = pygame.Surface((x_size, y_size))
        surface.blit(icon, (0,0))
        surface.blit(text, (icon.get_size()[0] + 2,0))
        rect = surface.get_rect()
        
        Widget.__init__(self, container, rect, frame_rate, surface)
        
    def add_subitem(self, item):
        """
        Append a subitem to the item list
        """
        self.subitems_list.append(item)
    
    
    def draw_item(self, screen):
        #draw the item in the screen
        screen.blit(self.background, self.rect_absolute)
    
    def on_mouse_over(self):
        return
    
    def on_mouse_out(self):
        return
    
    def on_mouse_click(self):
        """
        Handle mouse click
        """
        if(len(self.subitems_list) > 0):
            self.menu.set_actual_selection(self.subitems_list)
        else:
            self.menu.close()
            if(self.action_id != None):
                self.menu.send_action(self.action_id)
