# -*- coding: utf-8 -*-

# Copyright (C) 2011 ceibalJAM! - ceibaljam.org
# This file is part of Saludame.
#
# Saludame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Saludame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Saludame. If not, see <http://www.gnu.org/licenses/>.

import pygame

class Widget:
    
    """ A widget represents anything drawable on the screen """
    
    def __init__(self, container, rect_in_container, frame_rate, surface=None, tooltip=None):
        self.container = container # Rect, containing the widget
        self.set_rect_in_container(rect_in_container)
        self.frame_rate = frame_rate
        self.background = surface
        self.parent = None
        
        self.center_in_rect = False
        
        # Tooltip
        self.tooltip = tooltip
        self.super_tooltip = None
        self.showing_tooltip = False
        
        # Click Sound
        self.click_sound_path = None
        
        self.visible = True
        
        self.over = False
        
        # A widget it's dirty when it changes somehow, for example an animation will be dirty after every new sprite
        # A widget should change in the update method (before draw)
        self.dirty = True
        
        # When this flag it's on, the widget it's always dirty, unless the update method is overriden
        self.keep_dirty = False
    
    def update(self, frames):
        """ Abstract. This method is called before draw, the purpose is to override it to alter the widget and let
            know the application that the widget became dirty, for example when an animation changes its image or its position."""
        if self.keep_dirty:
            self.set_dirty()
    
    def draw(self, screen):
        self.dirty = False
        if self.visible:
            if self.background:
                if self.center_in_rect:
                    x, y = self.background.get_size()
                    x = self.rect_absolute.size[0] - x
                    y = self.rect_absolute.size[1] - y
                    coords = self.rect_absolute.left + x / 2, self.rect_absolute.top + y / 2
                    screen.blit(self.background, coords)
                    return self.rect_absolute
                else:
                    screen.blit(self.background, self.rect_absolute)
                    return self.rect_absolute
    
    def set_image(self, image):
        self.background = image
    
    def get_image(self):
        return self.background
    
    def set_rect_in_container(self, rect):
        # Rect del widget (relativo al container)
        self.rect_in_container = rect
        
        # Rect del widget (absoluto al screen)
        self.rect_absolute = pygame.Rect((self.container.left + self.rect_in_container.left, self.container.top + self.rect_in_container.top), (self.rect_in_container.size))
  
    def set_rect_size(self, size):
        # Rect del widget (relativo al container)
        self.rect_in_container.size = size
        
        # Rect del widget (absoluto al screen)
        self.rect_absolute.size = size
    
    def set_click_sound_path(self, path):
        self.click_sound_path = path
    
    def set_tooltip(self, text):
        self.tooltip = text
        
    def set_super_tooltip(self, text):
        self.super_tooltip = text
        
    def handle_mouse_down(self, (x, y)):
        self.on_mouse_click()
        
    def on_mouse_click(self):
        if self.click_sound_path:
            sound = pygame.mixer.Sound(self.click_sound_path)
            sound.play()
    
    def on_mouse_over(self):
        self.over = True
    
    def on_mouse_out(self):
        self.over = False
    
    def set_dirty(self):
        self.dirty = True
        if self.parent:
            self.parent.set_dirty()
            
    def get_background_and_owner(self):
        if self.background:
            return (self.background, self)
        elif self.parent:
            return self.parent.get_background_and_owner()
        else:
            return (None, None)

    def get_background(self):
        return self.get_background_and_owner()[0]
    
    def get_background_rect(self):
        background, owner = self.get_background_and_owner()
        if background:
            if self is owner:
                return background.copy()
            else:
                parents_relative_pos = self.rect_absolute.x - owner.rect.x, self.rect_absolute.y - owner.rect.y
                rect = pygame.Rect(parents_relative_pos, self.rect_absolute.size)
                return background.subsurface(rect)
        return pygame.Surface(self.rect_absolute.size)
    
    def contains_point(self, x, y):
        return self.rect_absolute.collidepoint(x, y)
    