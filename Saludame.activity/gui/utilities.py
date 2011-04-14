# -*- coding: utf-8 -*-

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
        self.set_dirty()
        if self.function_on_mouse_over and self.enable: # if there's a callback setted makes the call
            self.function_on_mouse_over(self)
    
    # Override
    def on_mouse_out(self):
        self.over = False
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
        if self.visible and self.background and self.over:
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
    def __init__(self, container, x, y, frame_rate, text, size, color, type="normal", fill=True):    
            
        Widget.__init__(self, container, pygame.Rect(x, y, 0, 0), frame_rate)
        
        self.type = type
        self.lines = []
        self.font = get_font(size)
        self.color = color
        self.parse_lines(text)
        self.size = size
        
        self.fill = fill
        
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

    def prepare_text_block(self):
        number_of_lines = 0
        for l in self.lines:
            number_of_lines += 1           
            r = self.font.render(l, False, self.color)
            if r.get_rect().width > self.rect_absolute.width:
                self.rect_absolute.width = r.get_rect().width
            self.rect_absolute.height += r.get_rect().height 
        
        if self.type == "tooltip":
            self.rect_absolute.height += 20
            self.rect_absolute.width += 20
        
        # Make it fit in the container
        if self.rect_absolute.right > self.container.right:
            self.rect_absolute.right = self.container.right
        if self.rect_absolute.bottom > self.container.bottom:
            self.rect_absolute.bottom = self.container.bottom
            
        self.rect_in_container.size = self.rect_absolute.size                  
        
    def draw(self, screen):
        if self.visible:
            number_of_lines = 0
            
            if self.fill:
                screen.fill((247, 247, 247), (self.rect_absolute))
                
            if self.type == "tooltip":
                top = self.rect_absolute.top + 10
                left = self.rect_absolute.left + 10
            else:
                top = self.rect_absolute.top
                left = self.rect_absolute.left
                
            for l in self.lines:          
                r = self.font.render(l, False, self.color)
                screen.blit(r, (left, top + r.get_rect().height * number_of_lines))
                number_of_lines += 1
            if self.type == "tooltip":
                pygame.draw.rect(screen, pygame.Color("#7fe115"), self.rect_absolute, 2)
                
    def switch_color_text(self, color):
        self.color = color
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
