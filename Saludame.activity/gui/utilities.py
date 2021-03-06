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

# Utilitarios: Text, Button (abstract), ImageButton, TextButton

import pygame
from widget import *
import os

class Text(Widget):
    
    ALIGN_LEFT = 0
    ALIGN_RIGHT = 1
    ALIGN_CENTER = 2
    
    def __init__(self, container_rect, x, y, frame_rate, text, size, color, type="normal", alignment=ALIGN_LEFT, bold=False, italic=False):
        self.font = get_font(size, bold, italic)
        self.text = unicode(text)
        self.color = color
        
        self.type = type
        
        # Render the text and calculate the size
        render = self.font.render(self.text, False, color)
        if alignment == Text.ALIGN_LEFT:
            rect = render.get_rect(topleft=(x, y))
        elif alignment == Text.ALIGN_RIGHT:
            rect = render.get_rect(topright=(x, y))
        else:
            rect = render.get_rect(center=(x, y))           
                    
        # Make it fit in the container
        if rect.right > container_rect.right:
            rect.right = container_rect.right
        if rect.bottom > container_rect.bottom:
            rect.bottom = container_rect.bottom    
            
        Widget.__init__(self, container_rect, rect, frame_rate)  

        self.refresh()
    
    def refresh(self):
        self.background = self.font.render(self.text, False, self.color)
        self.set_dirty()
        
    def switch_color_text(self, color):
        self.color = color
        self.refresh()
        return (self)
    
class Image(Widget):
    def __init__(self, container, rect, frame_rate, image, keep_format=False):
        
        if not isinstance(image, pygame.Surface):
            image = pygame.image.load(image)
            if keep_format:
                self.background = image
            else:
                if image.get_bitsize() == 8:
                    self.background = image.convert()
                else:
                    self.background = image.convert_alpha()
        else:
            self.background = image
        Widget.__init__(self, container, pygame.Rect((rect.left, rect.top), self.background.get_rect().size), frame_rate, self.background)                

class Button(Widget):
    
    # Clase abstracta que representa un boton
    
    def __init__(self, container, rect, frame_rate, surface, cb_click=None, cb_over=None, cb_out=None):
        
        Widget.__init__(self, container, rect, frame_rate, surface)
        
        self.function_on_mouse_click = cb_click
        self.function_on_mouse_over = cb_over
        self.function_on_mouse_out = cb_out
        
        self.highlight = True   # Highlight it when mouse over
        
        self.enable = True
        
        self.set_click_sound_path("assets/sound/click.ogg")
    
    # Override
    def on_mouse_click(self):
        Widget.on_mouse_click(self)    # Super
        
        if self.function_on_mouse_click and self.enable: # if there's a callback setted makes the call
            self.function_on_mouse_click(self)
    
    # Override
    def on_mouse_over(self):
        self.over = True
        if self.highlight:
            self.set_dirty()
        if self.function_on_mouse_over and self.enable: # if there's a callback setted makes the call
            self.function_on_mouse_over(self)
    
    # Override
    def on_mouse_out(self):
        self.over = False
        if self.highlight:
            self.set_dirty()
        if self.function_on_mouse_out and self.enable: # if there's a callback setted makes the call
            self.function_on_mouse_out(self)
    
    def set_on_mouse_click(self, fn):
        self.function_on_mouse_click = fn
   
    def set_on_mouse_over(self, fn):
        self.function_on_mouse_over = fn

    def set_on_mouse_out(self, fn):
        self.function_on_mouse_out = fn
    
    def draw(self, screen):
        updates = Widget.draw(self, screen)
        if self.visible and self.background and self.over and self.highlight:
            copy = self.background.convert_alpha()
            copy.fill((40, 40, 40), None, pygame.BLEND_ADD)       # Makes the widget brighter
            screen.blit(copy, self.rect_absolute)
        return updates
        
class ImageButton(Button):
    
    def __init__(self, container, rect, frame_rate, image, cb_click=None, cb_over=None, cb_out=None):
        
        if not isinstance(image, pygame.Surface):
            image = pygame.image.load(image)
            if image.get_bitsize() == 8:
                self.image = image.convert()
            else:
                self.image = image.convert_alpha()
        
        rect.size = image.get_rect().size

        self.text_intro = None
        self.text_result = None

        Button.__init__(self, container, rect, frame_rate, image, cb_click, cb_over, cb_out)
    
    def switch_image_background(self, image):
        if not isinstance(image, pygame.Surface):
            image = pygame.image.load(image).convert_alpha()
            if image.get_bitsize() == 8:
                image = image.convert()
            else:
                image = image.convert_alpha()

            if self.text_intro:
                self.text_intro.visible = True
        
        if self.text_result:    
            self.text_result.visible = False
        self.background = image
        self.set_dirty()
        
class TextButton(ImageButton):     
    def __init__(self, container, rect, frame_rate, text, size, color, cb_click=None, cb_over=None, cb_out=None):
        self.text = Text(container, rect.x, rect.y, frame_rate, text, size, color)
        ImageButton.__init__(self, container, self.text.rect_in_container, frame_rate, self.text.background, cb_click, cb_over, cb_out)
        
    def switch_color_text(self, color):
        self.background = self.text.switch_color_text(color).background
        self.set_dirty()
        
class TextBlockButton(Button):     
    def __init__(self, container, rect, frame_rate, text, size, color, cb_click=None, cb_over=None, cb_out=None):
        self.text = TextBlock(container, rect.x, rect.y, frame_rate, text, size, color, "normal", False)
        Button.__init__(self, container, self.text.rect_in_container, frame_rate, self.text.background, cb_click, cb_over, cb_out)
        
    def switch_color_text(self, color):
        self.text.switch_color_text(color)
        self.set_dirty()
        
    def draw(self, screen):
        self.text.draw(screen)
        self.parent.set_dirty_background()
    
class TextButton2(ImageButton):
    
    def __init__(self, container, rect, frame_rate, text, size, color, background, cb_click=None, cb_over=None, cb_out=None):
        self.back = background
        self.text = text
        self.size = size
        self.color = color
        
        rect.size = self.back.get_size()
        surface = self.get_surface()
        ImageButton.__init__(self, container, rect, frame_rate, surface, cb_click, cb_over, cb_out)
        
    def switch_color_text(self, color):
        self.color = color
        self.background = self.get_surface()
        self.set_dirty()
    
    def get_surface(self):
        font = get_font(self.size)
        render = font.render(self.text, True, self.color)
        
        surface = self.back.copy()
        surface.blit(render, render.get_rect(center=surface.get_rect().center))
        return surface
    
class TextBlock(Widget):
    def __init__(self, container, x, y, frame_rate, text, size, color, type="normal", fill=True, anchor_type="topleft"):    
        
        Widget.__init__(self, container, pygame.Rect(x, y, 0, 0), frame_rate)
        
        self.type = type
        self.lines = []
        self.font = get_font(size)
        self.color = color
        self.parse_lines(text)
        self.size = size
        
        self.fill = fill
        self.anchor = (container[0] + x, container[1] + y)
        self.anchor_type = anchor_type
        
        if type == "tooltip":
            self.rect_absolute.bottomleft = (x, y)
        
        self.prepare_text_block()
        
    def parse_lines(self, text):
        self.lines = []
        if isinstance(text, unicode):
            eol = u"\n"
        else:
            eol = "\n"            
        (b, _, a) = text.partition(eol)
        self.lines.append(b)
        while(a != ''):
            (b, _, a) = a.partition(eol)
            self.lines.append(b)

    def render_lines(self):
        self.rect_absolute.width = 0
        self.rect_absolute.height = 0
        self.rendered_lines = []
        for l in self.lines:          
            r = self.font.render(l, False, self.color)
            if r.get_rect().width > self.rect_absolute.width:
                self.rect_absolute.width = r.get_rect().width
            self.rect_absolute.height += r.get_rect().height 
            self.rendered_lines.append(r)
            
    def prepare_text_block(self):
        self.render_lines()
            
        if self.type == "tooltip":
            self.rect_absolute.height += 20
            self.rect_absolute.width += 20
        
        if self.anchor_type == "center":
            # Center the rectangle in the given coordinates
            #self.rect_absolute.center = self.rect_absolute.topleft
            self.rect_absolute.center = self.anchor
            
        # Make it fit in the container
        if self.rect_absolute.right > self.container.right:
            self.rect_absolute.right = self.container.right
        if self.rect_absolute.bottom > self.container.bottom:
            self.rect_absolute.bottom = self.container.bottom
            
        self.rect_in_container.size = self.rect_absolute.size
        self.rect_in_container.left = self.rect_absolute.left - self.container.left
        self.rect_in_container.top = self.rect_absolute.top - self.container.top
        
    def draw(self, screen):
        if self.visible:
            if self.fill:
                screen.fill((247, 247, 247), self.rect_absolute)
                
            if self.type == "tooltip":
                top = self.rect_absolute.top + 10
                left = self.rect_absolute.left + 10
            else:
                top = self.rect_absolute.top
                left = self.rect_absolute.left
            
            if self.anchor_type == "center":
                number_of_lines = 0
                for r in self.rendered_lines:
                    x = left + (self.rect_absolute.width - r.get_width())/2
                    y = top + r.get_rect().height * number_of_lines
                    screen.blit(r, (x, y))
                    number_of_lines += 1
            else:
                number_of_lines = 0
                for r in self.rendered_lines:
                    screen.blit(r, (left, top + r.get_rect().height * number_of_lines))
                    number_of_lines += 1
            
            if self.type == "tooltip":
                pygame.draw.rect(screen, pygame.Color("#7fe115"), self.rect_absolute, 2)
                
    def switch_color_text(self, color):
        self.color = color
        self.render_lines()
        self.set_dirty()

font_dict = {}  # Chaches created font instances
def get_font(size, bold=False, italic=False):
    key = (size, bold, italic)
    if key in font_dict:
        return font_dict[key]
    
    if bold:
        font = pygame.font.Font("assets/fonts/DroidSans-Bold.ttf", size)
    else:
        font = pygame.font.Font("assets/fonts/DroidSans.ttf", size)
    
    if italic:
        font.set_italic(True)
    
    font_dict[key] = font
    
    return font
