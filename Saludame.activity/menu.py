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
import effects
import random
from gettext import gettext as _

SIZE = 600, 280
EXP_SPEED = 15.0 #expansion speed, in pixels per frame
MAX_ITEMS = 8 #max items quantity per selection
RADIUS = 90.0

#fonts
LARGE_TEXT = 10 #fewer mean small text
#buttons
SMALL_BUTTON = "assets/menu/A.png"
LARGE_BUTTON = "assets/menu/B.png"
CENTER_BUTTON = "assets/menu/center.png"
HELP_BUTTON = "assets/menu/menu_help.png"

CLOSE_MENU = "close_menu"
BACK_MENU = "back_menu"

class Menu(Window):
    
    def __init__(self, frame_rate, container, windows_controller, item_list, center, radius, game_manager, font):
        
        rect = pygame.Rect((0, 0), SIZE)
        rect.center = center
        self.windows_controller = windows_controller
        self.game_manager = game_manager
        Window.__init__(self, container, rect, frame_rate, windows_controller, "menu_window")

        self.depth = 0 #it means we are in the root of the menu, mayor values means we are not.
        
        self.center = center # center of the menu's circle
        
        self.frame_rate = frame_rate
        self.item_list = item_list # item's list that going to be displayed, root items
        self.previous_items = []
        
        self.exit = Item(container, frame_rate, _("exit"), "assets/icons/icon_quit.png", CLOSE_MENU, [], self, font, None, None, True)
        self.exit.rect_in_container.center = center
        self.exit.set_rect_in_container(self.exit.rect_in_container)
        
        self.back = Item(container, frame_rate, _("back"), "assets/icons/icon_quit.png", BACK_MENU, [], self, font, None, None, True)
        self.back.rect_in_container.center = center
        self.back.set_rect_in_container(self.back.rect_in_container)
        
        self.actual_selection = self.item_list  #list of actual subitems selection
        
        self.radius = RADIUS
        self.show = False

        self.on_expansion = False
        self.calculate()
        
    
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
            
            if self.depth == 0:
                self.exit.draw_item(screen)
                changes.append(self.exit.rect_absolute)
            else:
                self.back.draw_item(screen)
                changes.append(self.back.rect_absolute)
        
        return changes
    
    def send_action(self, action_id):
        """
        Send an action to the game_manager. The action was selected
        in one of the sub-items
        """
        if action_id == CLOSE_MENU:
            self.close()
        elif action_id == BACK_MENU:
            self.back()
        else:
            self.game_manager.execute_action(action_id)
            self.close()
    
    def set_actual_selection(self, items_list):
        """
        Set the actual items selection.
        """
        if(not self.on_expansion):
            actual_selection = self.get_allowed_items(items_list) # gets some allowed items, fewer than nine
            if len(actual_selection) > MAX_ITEMS:
                actual_selection = random.sample(actual_selection, MAX_ITEMS)
            
            self.actual_selection = actual_selection
            #
            self.on_expansion = True #if the selection changes, display the animation
            self.radius = 0
    
    def get_allowed_items(self, items_list):
        """
        Verifies wich items are allowed to perform its actions 
        for currently character's properties.  
        """
        allowed_items = []
        for item in items_list:
            #verifies item conditions
            if self.verify_item(item, self.game_manager):
                #verifies item's action conditions
                if item.action_id: #the item hasn't sub items
                    action = self.game_manager.get_action(item.action_id)
                    if self.verify_action(action, self.game_manager):
                        allowed_items.append(item)
                else:
                    allowed_items.append(item)
        return allowed_items
    
    def verify_item(self, item, game_manager):
        #verify place
        if item.allowed_places:
            allowed = False
            current_place = game_manager.get_current_place()
            for place in item.allowed_places:
                if current_place == place:
                    allowed = True
                    break
            if not allowed:
                return False
        #verify hour
        if item.allowed_hours:
            allowed = False
            current_hour = game_manager.get_current_hour()
            for hour in item.allowed_hours:
                if current_hour == hour:
                    allowed = True
                    break
            if not allowed:
                return False

        return True
    
    def verify_action(self, action, game_manager):
        
        #verify place
        allowed = False
        if action.allowed_places:
            current_place = game_manager.get_current_place()
            for place in action.allowed_places:
                if current_place == place:
                    allowed = True
                    break
            if not allowed:
                return False
            
        #verify hour
        if action.allowed_hours:
            allowed = False
            current_hour = game_manager.get_current_hour()
            for hour in action.allowed_hours:
                if current_hour == hour:
                    allowed = True
                    break
            if not allowed:
                return False
            
        #verify event
        if action.allowed_events:
            allowed = False
            active_events = game_manager.get_active_events()
            for evt_name in action.allowed_events:
                for active_evt in active_events:
                    if evt_name == active_evt.name:
                        allowed = True
                        break
            if not allowed:
                return False

        if action.level > self.game_manager.get_level():
            return False
        #verify path
        if not utilities.verify_path(action, self.game_manager):
            return False
              
        return True

        
    def close(self):
        """
        Close the Menu Window
        """
        self.show = False
        self.depth = 0
        self.previous_items = []
        self.actual_selection = []
        self.game_manager.menu_active = False

    def back_to_previous_selection(self):
        """
        comes back to a previous items selection.
        """
        self.depth -= 1
        self.set_actual_selection(self.previous_items[self.depth])
        if self.depth == 0:
            self.previous_items = []

    def show_items(self, subitems_list):
        """
        shows the recive items
        """
        self.previous_items.append(self.actual_selection)
        self.depth += 1
        self.set_actual_selection(subitems_list)

    
    #handlers
    def handle_mouse_down(self, coord):
        if self.show and not self.on_expansion:
            if self.exit.rect_absolute.collidepoint(coord) and self.depth == 0:
                self.close()                
            elif self.exit.rect_absolute.collidepoint(coord) and self.depth > 0: #click on back item, it's in the same position of exit item
                self.back_to_previous_selection()
            else:
                for item in self.actual_selection:
                    if item.rect_absolute.collidepoint(coord):
                        item.on_mouse_click()
                        break

        else:
            self.set_actual_selection(self.item_list)
            self.show = True
            self.game_manager.menu_active = True

    #privates
    
    def calculate(self):
        """
            Calculate the position for each menu's actual selection.
        """
        self.__calculate_items_position(self.actual_selection)
        
    def __calculate_items_position(self, item_list):
        if len(item_list) > 0:
            angle = (2.0 * math.pi) / len(item_list)
        else:
            angle = 0.0
        current_angle = - math.pi / 2.0 - angle / 2.0
        for item in item_list:
            self.__calculate_item_position(item, current_angle) #calculate the position for each item
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
                rect.midbottom = coord[0], coord[1] + 25
            else:
                rect.midtop = coord[0], coord[1] - 25
        item.set_rect_in_container(rect)   # Recalculates the absolute coordinates
        

class Item(Widget):
    """
    Entity that represent an item
    """
    def __init__(self, container, frame_rate, name, icon_path, action_id, subitems_list, menu, font, allowed_places = None, allowed_hours = None,  center_item=False):
        
        self.name = name
        self.subitems_list = subitems_list
        self.action_id = action_id
        self.menu = menu
        self.allowed_places = allowed_places
        self.allowed_hours = allowed_hours
        
        self.help_image = None
        self.bg_image = None
        if center_item:
            self.bg_image = pygame.image.load(CENTER_BUTTON).convert_alpha()
        else:
            if len(self.name) > LARGE_TEXT:
                self.bg_image = pygame.image.load(LARGE_BUTTON).convert_alpha()
            else:
                self.bg_image = pygame.image.load(SMALL_BUTTON).convert_alpha()
        self.bg_rect = self.bg_image.get_rect()
        
        action = self.menu.game_manager.get_action(self.action_id)
        if action:
            if action.link: #has to show help button
                self.help_image = pygame.image.load(HELP_BUTTON).convert_alpha()
                self.help_rect = self.help_image.get_rect()
                
        size_and_surface = self.get_surface(20, self.name, self.bg_image, self.help_image)
        
        self.rect = pygame.Rect((0, 0), size_and_surface[0])
        
        Widget.__init__(self, container, self.rect, frame_rate, size_and_surface[1])

    def get_surface(self, font_size, text, bg_image, help_image):
        font = utilities.get_font(font_size)
        render = font.render(text, True, (255, 255, 255))
        
        if help_image:
            full_size = self.help_rect.width + self.bg_rect.width - 4, self.help_rect.height
            surface = pygame.Surface(full_size)
            surface.fill(bg_image.get_at(bg_image.get_rect().center))
            surface.blit(bg_image, bg_image.get_rect(left=self.bg_image.get_rect().left))
            surface.blit(help_image, help_image.get_rect(left=surface.get_rect().left + self.bg_rect.width - 4))
        else:
            full_size = bg_image.get_rect().size
            surface = bg_image.copy()
        surface.blit(render, render.get_rect(center=self.bg_rect.center))
        return full_size, surface
        
    def add_subitem(self, item):
        """
        Append a subitem to the item list
        """
        self.subitems_list.append(item)
    
    
    def draw_item(self, screen):
        """
        draw the item in the screen
        """
        screen.blit(self.background, self.rect_absolute)
    
    def on_mouse_over(self):
        return
    
    def on_mouse_out(self):
        return
    
    def on_mouse_click(self):
        """
        Handle mouse click
        """
        if len(self.subitems_list) > 0:
            self.menu.show_items(self.subitems_list)
        else:
            if self.action_id != None:
                self.menu.send_action(self.action_id)
            else:
                self.menu.send_action(CLOSE_MENU) # if the item have not children and have not an action_id, close the menu


